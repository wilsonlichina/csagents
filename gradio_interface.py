"""
Gradio界面模块
构建LCSC邮件客服系统的Web用户界面
"""

import gradio as gr
import pandas as pd
import asyncio
from typing import Optional, List, Tuple
import json

from email_manager import email_manager, EmailData
from ai_agent import get_agent, ProcessingResult

# 全局变量
current_selected_email: Optional[EmailData] = None
processing_results: List[ProcessingResult] = []

def load_emails() -> pd.DataFrame:
    """加载邮件列表"""
    try:
        print("📧 正在加载邮件...")
        emails = email_manager.load_emails()
        df = email_manager.get_email_list()
        print(f"✅ 成功加载 {len(emails)} 封邮件")
        return df
    except Exception as e:
        print(f"❌ 加载邮件失败: {str(e)}")
        return pd.DataFrame(columns=['发件人', '收件人', '发送时间', '主题', '类型'])

def on_email_select(evt: gr.SelectData) -> Tuple[str, bool]:
    """邮件选择事件处理"""
    global current_selected_email
    
    try:
        if evt.index is not None and len(evt.index) >= 1:
            row_index = evt.index[0]
            current_selected_email = email_manager.get_email_by_index(row_index)
            
            if current_selected_email:
                print(f"📧 选中邮件: {current_selected_email.file_name}")
                return f"已选中邮件: {current_selected_email.subject}", True
            else:
                return "选择的邮件无效", False
        else:
            return "请选择一封邮件", False
    except Exception as e:
        print(f"❌ 邮件选择错误: {str(e)}")
        return f"选择邮件时发生错误: {str(e)}", False

def show_email_detail() -> Tuple[str, str, str, str, str, bool]:
    """显示邮件详情"""
    global current_selected_email
    
    if current_selected_email is None:
        return "", "", "", "", "请先选择一封邮件", False
    
    try:
        # 格式化邮件内容
        content_display = f"""
## 邮件详细信息

**文件名**: {current_selected_email.file_name}

**解析信息**:
- 邮件类型: {current_selected_email.parsed_info.get('email_type', '未知')}
- 识别意图: {current_selected_email.parsed_info.get('intent', '未知')}
- 发件人姓名: {current_selected_email.parsed_info.get('sender_name', '未提供')}
- 电话: {current_selected_email.parsed_info.get('phone', '未提供')}
- 公司: {current_selected_email.parsed_info.get('company', '未提供')}
- 国家: {current_selected_email.parsed_info.get('country', '未提供')}

**提取的产品信息**:
{json.dumps(current_selected_email.parsed_info.get('products', []), indent=2, ensure_ascii=False)}

---

**原始邮件内容**:
```
{current_selected_email.content}
```
"""
        
        return (
            current_selected_email.sender,
            current_selected_email.recipient, 
            current_selected_email.send_time,
            current_selected_email.subject,
            content_display,
            True  # 显示详情面板
        )
    except Exception as e:
        error_msg = f"显示邮件详情时发生错误: {str(e)}"
        print(f"❌ {error_msg}")
        return "", "", "", "", error_msg, False

def close_email_detail() -> bool:
    """关闭邮件详情"""
    return False

async def process_email_with_agent(llm_choice: str, system_prompt: str, progress=gr.Progress()) -> Tuple[str, str, bool]:
    """使用AI Agent处理邮件"""
    global current_selected_email
    
    if current_selected_email is None:
        return "请先选择一封邮件", "", False
    
    try:
        progress(0, desc="初始化AI Agent...")
        
        # 根据选择获取Agent
        model_mapping = {
            "Claude 3.5 Sonnet": ("bedrock", "claude-3-5-sonnet"),
            "Claude 3.7 Sonnet": ("bedrock", "claude-3-7-sonnet")
        }
        
        model_provider, model_name = model_mapping.get(llm_choice, ("bedrock", "claude-3-7-sonnet"))
        agent = get_agent(model_provider, model_name)
        
        # 如果提供了自定义system prompt，更新Agent
        if system_prompt.strip():
            agent.agent.system_prompt = system_prompt
        
        progress(0.2, desc="开始处理邮件...")
        
        # 处理邮件
        def progress_callback(msg: str):
            print(f"📊 {msg}")
        
        result = await agent.process_email(current_selected_email, progress_callback)
        
        progress(0.8, desc="格式化结果...")
        
        # 格式化结果显示
        result_display = f"""
## AI处理结果

### 基本信息
- **邮件**: {result.email_id}
- **识别意图**: {result.intent}
- **置信度**: {result.confidence:.2%}
- **处理时间**: {result.timestamp}

### 执行的操作
{chr(10).join([f"- {action}" for action in result.actions_taken])}

### 使用的工具
{chr(10).join([f"- {tool}" for tool in result.tools_used])}

### 处理结果
```json
{json.dumps(result.results, indent=2, ensure_ascii=False)}
```

### AI回复内容
```
{result.response}
```
"""
        
        # 保存结果
        processing_results.append(result)
        
        progress(1.0, desc="处理完成！")
        
        return "✅ AI处理完成！", result_display, True
        
    except Exception as e:
        error_msg = f"AI处理失败: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg, f"处理过程中发生错误:\n{error_msg}", True

def create_interface() -> gr.Blocks:
    """创建Gradio界面"""
    
    # 自定义CSS样式
    custom_css = """
    .email-container {
        max-height: 400px;
        overflow-y: auto;
    }
    .result-container {
        max-height: 500px;
        overflow-y: auto;
    }
    .config-panel {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
    }
    """
    
    with gr.Blocks(
        theme=gr.themes.Soft(),
        title="LCSC邮件智能客服系统",
        css=custom_css
    ) as demo:
        
        # 标题
        gr.Markdown("""
        # 🏢 LCSC Electronics 邮件智能客服系统
        
        基于Gradio + Strands Agent SDK构建的智能邮件处理系统
        """)
        
        with gr.Row():
            # 左侧配置面板
            with gr.Column(scale=1, elem_classes=["config-panel"]):
                gr.Markdown("## ⚙️ 系统配置")
                
                # LLM选择
                llm_choice = gr.Dropdown(
                    choices=["Claude 3.5 Sonnet", "Claude 3.7 Sonnet"],
                    value="Claude 3.7 Sonnet",
                    label="🤖 选择LLM模型",
                    info="选择用于处理邮件的AI模型"
                )
                
                # System Prompt配置
                system_prompt = gr.Textbox(
                    label="📝 System Prompt",
                    placeholder="输入自定义系统提示词（可选）...",
                    lines=8,
                    info="留空使用默认提示词"
                )
                
                # 状态显示
                gr.Markdown("## 📊 系统状态")
                status_display = gr.Textbox(
                    label="状态",
                    value="系统就绪",
                    interactive=False
                )
            
            # 右侧邮件处理区域
            with gr.Column(scale=3):
                gr.Markdown("## 📧 邮件处理区域")
                
                # 邮件列表
                email_list = gr.Dataframe(
                    label="邮件列表",
                    headers=["发件人", "收件人", "发送时间", "主题", "类型"],
                    datatype=["str", "str", "str", "str", "str"],
                    interactive=False,
                    wrap=True,
                    elem_classes=["email-container"],
                    row_count=(8, "dynamic")
                )
                
                # 操作按钮
                with gr.Row():
                    refresh_btn = gr.Button("🔄 刷新邮件", variant="secondary")
                    view_btn = gr.Button("👁️ 查看邮件信息", variant="secondary")
                    process_btn = gr.Button("🤖 AI Agent Loop", variant="primary")
                
                # AI处理结果展示区域
                with gr.Accordion("🔍 AI处理结果", open=False) as result_accordion:
                    processing_status = gr.Textbox(
                        label="处理状态",
                        value="等待处理...",
                        interactive=False
                    )
                    
                    result_display = gr.Markdown(
                        value="暂无处理结果",
                        elem_classes=["result-container"]
                    )
        
        # 邮件详情弹窗 - 使用Accordion替代Modal（Gradio 5.x兼容性）
        with gr.Accordion("📧 邮件详细信息", open=False, visible=False) as email_detail_accordion:
            gr.Markdown("## 📧 邮件详细信息")
            
            with gr.Row():
                sender_display = gr.Textbox(label="发件人", interactive=False)
                recipient_display = gr.Textbox(label="收件人", interactive=False)
            
            with gr.Row():
                time_display = gr.Textbox(label="发送时间", interactive=False)
                subject_display = gr.Textbox(label="主题", interactive=False)
            
            content_display = gr.Markdown(label="邮件内容")
            
            close_btn = gr.Button("关闭", variant="secondary")
        
        # 事件绑定
        
        # 加载邮件
        demo.load(
            fn=load_emails,
            outputs=[email_list]
        )
        
        # 刷新邮件
        refresh_btn.click(
            fn=load_emails,
            outputs=[email_list]
        )
        
        # 邮件选择
        email_list.select(
            fn=on_email_select,
            outputs=[status_display, view_btn]
        )
        
        # 查看邮件详情
        view_btn.click(
            fn=show_email_detail,
            outputs=[
                sender_display,
                recipient_display, 
                time_display,
                subject_display,
                content_display,
                email_detail_accordion
            ]
        )
        
        # 关闭邮件详情
        close_btn.click(
            fn=close_email_detail,
            outputs=[email_detail_accordion]
        )
        
        # AI处理
        process_btn.click(
            fn=process_email_with_agent,
            inputs=[llm_choice, system_prompt],
            outputs=[processing_status, result_display, result_accordion]
        )
    
    return demo

if __name__ == "__main__":
    # 测试界面
    demo = create_interface()
    demo.launch(debug=True)
