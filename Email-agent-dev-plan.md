# 立创商城（LCSC Electronics）邮件客服智能体系统开发规划

## 项目概述
开发一个基于Python、Gradio和Strands Agent SDK的智能邮件客服系统，用于自动化处理立创商城的客户邮件，识别意图并执行相应的业务操作。

## 技术栈
- **前端界面**: Gradio 5.16+ (现代化Web UI框架)
- **AI Agent**: Strands Agent SDK 0.1.3+ (AWS开源的代码优先Agent框架)
- **Agent工具包**: strands-agents-tools 0.1.2+ (内置工具集)
- **语言模型**: Claude 3.7 Sonnet (Amazon Bedrock) / Claude 3.5 Sonnet
- **编程语言**: Python 3.10+
- **邮件处理**: 自定义邮件解析器
- **异步处理**: asyncio + FastAPI (Gradio 5.x内置)
- **云服务**: Amazon Bedrock (默认模型提供商)

## 系统架构

### 1. 核心模块设计

#### 1.1 邮件管理模块 (`email_manager.py`)
- **功能**: 枚举和解析emails目录下的邮件文件
- **主要类**: `EmailManager`
- **方法**:
  - `load_emails()`: 加载所有邮件文件
  - `parse_email(file_path)`: 解析单个邮件文件
  - `get_email_list()`: 返回邮件列表数据

#### 1.2 AI Agent模块 (`ai_agent.py`)
- **功能**: 使用Strands SDK 0.1.3定义智能代理
- **主要类**: `LCSCEmailAgent`
- **核心功能**:
  - 邮件意图识别
  - 业务规则判断
  - 工具调用协调
- **Strands特性**:
  - 代码优先的Agent定义
  - 内置工具集成
  - 自动工具选择和执行
  - 完整的可观测性和追踪

#### 1.3 业务工具模块 (`business_tools.py`)
- **功能**: 定义Agent使用的业务工具
- **工具列表**:
  - `query_order_by_id(order_id)`: 根据订单号查询订单信息
  - `query_customer_by_email(email)`: 根据邮箱查询客户信息
  - `query_orders_by_customer(customer_info)`: 根据客户信息查询订单
  - `query_product_by_id(product_id)`: 根据产品ID查询产品信息
  - `query_inventory_status(product_id)`: 查询库存状态（现货/订货）
  - `intercept_order_shipping(order_id, reason)`: 拦截订单发货

#### 1.4 Gradio界面模块 (`gradio_interface.py`)
- **功能**: 构建Web用户界面
- **主要组件**:
  - 邮件列表展示
  - 配置面板（LLM选择、System Prompt）
  - 邮件详情弹窗
  - AI处理结果展示

### 2. 界面设计规划

#### 2.1 主界面布局
```
┌─────────────────┬─────────────────────────────────────┐
│   配置面板      │           邮件处理区域               │
│                 │                                     │
│ LLM选择:        │  ┌─────────────────────────────────┐ │
│ □ Claude 3.5    │  │        邮件列表                 │ │
│ □ Claude 3.7    │  │ 发件人 | 收件人 | 发送时间      │ │
│                 │  │ ─────────────────────────────── │ │
│ System Prompt:  │  │ user1@... | lcsc@... | 2024... │ │
│ ┌─────────────┐ │  │ user2@... | lcsc@... | 2024... │ │
│ │             │ │  └─────────────────────────────────┘ │
│ │             │ │                                     │
│ │             │ │  [查看邮件信息] [AI Copilot]     │
│ └─────────────┘ │                                     │
│                 │  ┌─────────────────────────────────┐ │
│                 │  │      AI处理结果展示区           │ │
│                 │  │     (可折叠组件)                │ │
│                 │  └─────────────────────────────────┘ │
└─────────────────┴─────────────────────────────────────┘
```

#### 2.2 邮件详情弹窗
- 模态对话框形式
- 显示完整邮件信息：发件人、收件人、发送时间、详细内容
- 支持关闭和滚动

### 3. AI Agent工作流程

#### 3.1 意图识别规则
基于邮件内容关键词和上下文识别以下意图：
- **订单修改**: 修改发货地址、增删产品
- **订单取消**: 取消订单请求
- **订单合并**: 合并多个订单
- **价格查询**: 询问产品价格
- **库存查询**: 询问产品库存
- **物流查询**: 查询订单物流状态
- **一般咨询**: 其他咨询类问题

#### 3.2 业务动作映射
```python
INTENT_ACTION_MAPPING = {
    "订单修改": "intercept_shipping",
    "订单取消": "intercept_shipping", 
    "订单合并": "intercept_shipping",
    "价格查询": "query_product_info",
    "库存查询": "query_inventory",
    "物流查询": "query_logistics",
    "一般咨询": "general_response"
}
```

### 4. 数据结构设计

#### 4.1 邮件数据结构
```python
@dataclass
class EmailData:
    file_name: str
    subject: str
    sender: str
    recipient: str
    send_time: str
    content: str
    parsed_info: dict
```

#### 4.2 处理结果数据结构
```python
@dataclass
class ProcessingResult:
    email_id: str
    intent: str
    confidence: float
    actions_taken: List[str]
    tools_used: List[str]
    results: dict
    timestamp: str
```

### 5. 开发阶段规划

#### 阶段1: 基础框架搭建 (1-2天)
- [x] 项目结构创建
- [ ] 邮件解析模块开发
- [ ] Gradio基础界面搭建
- [ ] 基本的邮件列表展示

#### 阶段2: AI Agent集成 (2-3天)
- [ ] Strands SDK集成
- [ ] 意图识别模型配置
- [ ] 基础工具函数实现
- [ ] Agent工作流程实现

#### 阶段3: 业务工具开发 (2-3天)
- [ ] 订单查询工具
- [ ] 客户信息查询工具
- [ ] 产品和库存查询工具
- [ ] 订单拦截工具
- [ ] 模拟数据库/API接口

#### 阶段4: 界面完善 (1-2天)
- [ ] 邮件详情弹窗
- [ ] AI处理结果展示
- [ ] 配置面板功能
- [ ] 界面美化和交互优化

#### 阶段5: 测试和优化 (1-2天)
- [ ] 功能测试
- [ ] 性能优化
- [ ] 错误处理完善
- [ ] 文档编写

### 6. Gradio 5.x 现代化特性应用

#### 6.1 界面组件升级
```python
# Gradio 5.x 现代化界面示例
with gr.Blocks(theme=gr.themes.Soft(), title="LCSC邮件智能客服") as demo:
    with gr.Row():
        with gr.Column(scale=1):
            # 配置面板 - 使用新的组件特性
            llm_choice = gr.Dropdown(
                choices=["Claude 3.5 Sonnet", "Claude 3.7"],
                value="Claude 3.5 Sonnet",
                label="选择LLM模型",
                interactive=True
            )
            system_prompt = gr.Textbox(
                label="System Prompt",
                lines=10,
                placeholder="输入系统提示词...",
                show_copy_button=True  # 5.x新特性
            )
        
        with gr.Column(scale=3):
            # 邮件列表 - 使用改进的Dataframe
            email_list = gr.Dataframe(
                headers=["发件人", "收件人", "发送时间", "主题"],
                datatype=["str", "str", "str", "str"],
                interactive=True,
                wrap=True,
                row_count=(5, "dynamic")  # 5.x新特性
            )
            
            with gr.Row():
                view_btn = gr.Button("查看邮件信息", variant="secondary")
                process_btn = gr.Button("AI Copilot", variant="primary")
            
            # AI处理结果 - 使用Accordion和Progress
            with gr.Accordion("AI处理结果", open=False):
                progress = gr.Progress()  # 5.x改进的进度条
                result_chatbot = gr.Chatbot(
                    label="处理过程",
                    height=400,
                    show_copy_button=True,
                    bubble_full_width=False  # 5.x新特性
                )
```

#### 6.2 Modal弹窗实现
```python
# Gradio 5.x 原生Modal支持
@gr.render(inputs=[email_list])
def show_email_detail(selected_email):
    if selected_email is not None:
        with gr.Modal(visible=True) as modal:
            gr.Markdown(f"## 邮件详情")
            gr.Textbox(label="发件人", value=selected_email["sender"], interactive=False)
            gr.Textbox(label="收件人", value=selected_email["recipient"], interactive=False)
            gr.Textbox(label="发送时间", value=selected_email["time"], interactive=False)
            gr.Textbox(
                label="邮件内容", 
                value=selected_email["content"], 
                lines=15, 
                interactive=False,
                show_copy_button=True
            )
            gr.Button("关闭", variant="secondary")
```

#### 6.3 流式处理展示
```python
# 利用Gradio 5.x的流式输出特性
async def process_email_stream(email_data, llm_choice, system_prompt):
    """流式处理邮件并实时更新界面"""
    yield gr.update(visible=True), "开始处理邮件..."
    
    # 意图识别阶段
    yield gr.update(), "🔍 正在识别邮件意图..."
    intent = await identify_intent(email_data, llm_choice)
    yield gr.update(), f"✅ 识别到意图: {intent}"
    
    # 工具调用阶段
    yield gr.update(), "🔧 正在调用相关工具..."
    results = await call_business_tools(intent, email_data)
    yield gr.update(), f"✅ 工具调用完成: {results}"
    
    # 最终结果
    yield gr.update(visible=False), "处理完成！"
```

### 7. 技术实现要点

#### 6.1 邮件解析策略
- 支持多种邮件格式（纯文本、结构化）
- 提取关键信息：主题、发件人、时间、内容
- 处理中英文混合内容

#### 6.2 Strands Agent SDK 0.1.3 实现方案

**基础Agent配置**:
```python
from strands import Agent, tool
from strands_tools import current_time

# 定义LCSC业务工具
@tool
def query_order_by_id(order_id: str) -> dict:
    """
    根据订单号查询订单信息
    
    Args:
        order_id (str): 订单号
        
    Returns:
        dict: 订单详细信息
    """
    # 实现订单查询逻辑
    pass

@tool
def query_customer_by_email(email: str) -> dict:
    """
    根据邮箱查询客户信息
    
    Args:
        email (str): 客户邮箱地址
        
    Returns:
        dict: 客户详细信息
    """
    # 实现客户查询逻辑
    pass

@tool
def intercept_order_shipping(order_id: str, reason: str) -> bool:
    """
    拦截订单发货
    
    Args:
        order_id (str): 订单号
        reason (str): 拦截原因
        
    Returns:
        bool: 拦截是否成功
    """
    # 实现订单拦截逻辑
    pass

# 创建LCSC邮件客服Agent
class LCSCEmailAgent:
    def __init__(self, model_provider="bedrock", model_name="claude-3-7-sonnet"):
        self.agent = Agent(
            tools=[
                query_order_by_id,
                query_customer_by_email, 
                intercept_order_shipping,
                current_time  # 使用内置工具
            ],
            model_provider=model_provider,
            model_name=model_name,
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self) -> str:
        return """
        你是立创商城(LCSC Electronics)的智能客服助手。
        
        你的主要职责：
        1. 分析客户邮件内容，识别客户意图
        2. 根据意图调用相应的业务工具
        3. 对于涉及订单修改、取消、合并的请求，执行订单拦截
        4. 提供准确、专业的客服回复
        
        可用工具：
        - query_order_by_id: 查询订单信息
        - query_customer_by_email: 查询客户信息
        - intercept_order_shipping: 拦截订单发货
        - current_time: 获取当前时间
        
        请始终保持专业、友好的服务态度。
        """
    
    async def process_email(self, email_content: str, sender_email: str) -> dict:
        """处理邮件并返回结果"""
        prompt = f"""
        请分析以下客户邮件：
        
        发件人: {sender_email}
        邮件内容: {email_content}
        
        请识别客户意图并执行相应操作。
        """
        
        # 使用Strands Agent处理
        response = await self.agent.arun(prompt)
        
        return {
            "intent": self._extract_intent(response),
            "actions": self._extract_actions(response),
            "response": response,
            "timestamp": current_time()
        }
```

**Strands Agent的优势**:
1. **代码优先**: 使用Python装饰器定义工具，简单直观
2. **自动工具选择**: Agent自动决定何时使用哪个工具
3. **内置可观测性**: 完整的执行追踪和日志
4. **模型无关**: 支持多种模型提供商（Bedrock、OpenAI等）
5. **生产就绪**: 内置安全性和扩展性考虑

#### 6.3 Gradio 5.x 组件选择和新特性
- `gr.Dataframe`: 邮件列表展示（支持选择、排序、过滤）
- `gr.Button`: 操作按钮（支持变体样式）
- `gr.Modal`: 邮件详情弹窗（Gradio 5.x原生支持）
- `gr.Accordion`: 可折叠的结果展示
- `gr.Dropdown`: LLM选择（支持搜索和多选）
- `gr.Textbox`: System Prompt配置（支持代码高亮）
- `gr.Progress`: 处理进度显示
- `gr.Chatbot`: AI对话展示（支持富文本和流式输出）
- `gr.Row/gr.Column`: 响应式布局
- `gr.Tabs`: 多标签页组织

**Gradio 5.x 新特性应用**:
- **原生Modal支持**: 无需自定义弹窗组件
- **改进的Dataframe**: 更好的交互性和性能
- **流式输出**: AI处理过程实时展示
- **主题系统**: 支持自定义主题和暗色模式
- **更好的移动端支持**: 响应式设计
- **组件状态管理**: 更精确的状态控制

### 7. 安全和性能考虑

#### 7.1 安全措施
- 输入验证和清理
- 敏感信息脱敏
- API调用频率限制
- 错误信息安全处理

#### 7.2 性能优化
- 邮件数据缓存
- 异步处理长时间任务
- 分页加载大量邮件
- 结果缓存机制

### 8. 部署和维护

#### 8.1 依赖管理
```txt
# 核心框架
gradio>=5.16.0
strands-agents>=0.1.3
strands-agents-tools>=0.1.2

# AI和云服务
boto3>=1.34.0
anthropic>=0.25.0

# 数据处理
pandas>=2.0.0
pydantic>=2.0.0

# 异步和工具
asyncio
aiofiles
python-dotenv
typing-extensions

# 可观测性（Strands内置）
opentelemetry-api
opentelemetry-sdk
```

**环境配置要求**:
```bash
# AWS凭证配置（用于Bedrock）
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-west-2

# 或使用aws configure命令配置
aws configure
```

#### 8.2 配置文件
- 环境变量配置
- LLM API密钥管理
- 业务规则配置文件

### 9. 扩展性考虑

#### 9.1 未来功能扩展
- 多语言支持
- 邮件自动回复
- 客户满意度评估
- 数据分析和报表
- 与LCSC现有系统集成

#### 9.2 模块化设计
- 插件化工具系统
- 可配置的意图识别规则
- 可扩展的业务流程

## 风险评估

### 技术风险
- Strands SDK文档可能不完整，需要实验和调试
- 邮件格式多样性可能影响解析准确性
- LLM API调用稳定性和成本控制

### 业务风险
- 意图识别准确性需要大量测试
- 订单拦截等关键操作需要严格验证
- 客户数据隐私保护

## 成功标准

1. **功能完整性**: 所有核心功能正常工作
2. **准确性**: 意图识别准确率 > 85%
3. **性能**: 单邮件处理时间 < 10秒
4. **用户体验**: 界面友好，操作流畅
5. **稳定性**: 系统运行稳定，错误处理完善

---

**开发团队**: AI Assistant
**预计完成时间**: 7-10个工作日
**最后更新**: 2025-07-03
