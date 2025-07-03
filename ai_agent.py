"""
AI Agent模块
使用Strands SDK定义LCSC邮件客服智能代理
"""

import asyncio
from typing import Dict, List, Optional, AsyncGenerator
from dataclasses import dataclass
from datetime import datetime

from strands import Agent
from strands_tools import current_time
from business_tools import BUSINESS_TOOLS
from email_manager import EmailData

@dataclass
class ProcessingResult:
    """处理结果数据结构"""
    email_id: str
    intent: str
    confidence: float
    actions_taken: List[str]
    tools_used: List[str]
    results: Dict
    response: str
    timestamp: str

class LCSCEmailAgent:
    """LCSC邮件客服智能代理"""
    
    def __init__(self, model_provider: str = "bedrock", model_name: str = "claude-3-7-sonnet"):
        """
        初始化Agent
        
        Args:
            model_provider: 模型提供商 (bedrock, openai等)
            model_name: 模型名称
        """
        self.model_provider = model_provider
        self.model_name = model_name
        
        # 创建Strands Agent
        self.agent = Agent(
            tools=BUSINESS_TOOLS + [current_time],
            system_prompt=self._get_system_prompt()
        )
        
        print(f"🤖 LCSC邮件客服Agent初始化完成")
        print(f"   模型: {model_provider}/{model_name}")
        print(f"   工具数量: {len(BUSINESS_TOOLS) + 1}")
    
    def _get_system_prompt(self) -> str:
        """Get system prompt"""
        return """
You are a professional intelligent customer service assistant for LCSC Electronics.

## Your Responsibilities
1. Analyze customer email content and accurately identify customer intent
2. Call appropriate business tools to retrieve information based on intent
3. For requests involving order modifications, cancellations, or mergers, proactively execute order interception
4. Provide accurate, professional, and friendly customer service responses

## Available Tools
- query_order_by_id: Query detailed order information by order ID
- query_customer_by_email: Query customer information by email address
- query_orders_by_customer: Query all orders for a customer
- query_product_by_id: Query product information by product ID
- query_inventory_status: Query product inventory status (in stock/on order)
- intercept_order_shipping: Intercept order shipping (critical operation)
- query_logistics_status: Query order logistics status
- current_time: Get current time

## Important Business Rules
1. **Order Interception Trigger Conditions**:
   - Customer requests to modify shipping address
   - Customer requests to add or remove products
   - Customer requests to cancel order
   - Customer requests to merge orders
   
2. **Processing Workflow**:
   - First identify customer and related orders from email content
   - Query relevant information (customer, orders, products, etc.)
   - If order changes are involved, immediately execute interception operation
   - Provide detailed processing results and follow-up guidance

3. **Response Requirements**:
   - Use professional and friendly tone
   - Provide specific order numbers and product information
   - Clearly state operations that have been executed
   - Give follow-up processing recommendations

## Example Scenarios
- Price inquiries: Query product information and inventory status
- Order inquiries: Query order status and logistics information
- Address changes: Intercept shipping and explain follow-up process
- Product changes: Intercept shipping and confirm change details
- Order cancellations: Intercept shipping and handle refund process

Please always maintain professional, accurate, and efficient service standards.
"""
    
    async def process_email(self, email_data: EmailData, progress_callback=None) -> ProcessingResult:
        """
        处理邮件并返回结果
        
        Args:
            email_data: 邮件数据
            progress_callback: 进度回调函数
            
        Returns:
            ProcessingResult: 处理结果
        """
        try:
            if progress_callback:
                progress_callback("🔍 开始分析邮件内容...")
            
            # 构建处理提示
            prompt = self._build_processing_prompt(email_data)
            
            if progress_callback:
                progress_callback("🤖 AI Agent正在处理...")
            
            # 使用Agent处理
            response = await self._run_agent_async(prompt)
            
            if progress_callback:
                progress_callback("📊 分析处理结果...")
            
            # 分析结果
            result = ProcessingResult(
                email_id=email_data.file_name,
                intent=email_data.parsed_info.get('intent', '未知'),
                confidence=0.85,  # 模拟置信度
                actions_taken=self._extract_actions(response),
                tools_used=self._extract_tools_used(response),
                results=self._extract_results(response),
                response=response,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            if progress_callback:
                progress_callback("✅ 处理完成！")
            
            return result
            
        except Exception as e:
            error_msg = f"处理邮件时发生错误: {str(e)}"
            print(f"❌ {error_msg}")
            
            return ProcessingResult(
                email_id=email_data.file_name,
                intent="处理失败",
                confidence=0.0,
                actions_taken=["错误处理"],
                tools_used=[],
                results={"error": error_msg},
                response=error_msg,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
    
    def _build_processing_prompt(self, email_data: EmailData) -> str:
        """构建处理提示"""
        return f"""
请分析并处理以下客户邮件：

## 邮件信息
- 文件名: {email_data.file_name}
- 主题: {email_data.subject}
- 发件人: {email_data.sender}
- 发送时间: {email_data.send_time}
- 邮件类型: {email_data.parsed_info.get('email_type', '未知')}
- 识别意图: {email_data.parsed_info.get('intent', '未知')}

## 邮件内容
{email_data.content}

## 提取的产品信息
{email_data.parsed_info.get('products', [])}

## 处理要求
1. 根据邮件内容和发件人信息，查询相关的客户和订单信息
2. 如果涉及订单变更（修改地址、增删产品、取消订单、合并订单），请立即执行订单拦截
3. 提供专业的客服回复，包括：
   - 确认收到客户的请求
   - 说明已执行的操作
   - 提供相关的订单/产品信息
   - 给出后续处理建议

请开始处理这封邮件。
"""
    
    async def _run_agent_async(self, prompt: str) -> str:
        """异步运行Agent"""
        try:
            # 由于Strands Agent可能不支持异步，我们在线程池中运行
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self.agent, prompt)
            return str(response)
        except Exception as e:
            print(f"Agent运行错误: {str(e)}")
            return f"Agent处理失败: {str(e)}"
    
    def _extract_actions(self, response: str) -> List[str]:
        """从响应中提取执行的动作"""
        actions = []
        
        # 简单的关键词匹配来识别动作
        if "查询订单" in response or "query_order_by_id" in response:
            actions.append("查询订单信息")
        if "查询客户" in response or "query_customer_by_email" in response:
            actions.append("查询客户信息")
        if "拦截发货" in response or "intercept_order_shipping" in response:
            actions.append("拦截订单发货")
        if "查询库存" in response or "query_inventory_status" in response:
            actions.append("查询库存状态")
        if "查询物流" in response or "query_logistics_status" in response:
            actions.append("查询物流状态")
        if "查询产品" in response or "query_product_by_id" in response:
            actions.append("查询产品信息")
            
        return actions if actions else ["分析邮件内容"]
    
    def _extract_tools_used(self, response: str) -> List[str]:
        """从响应中提取使用的工具"""
        tools = []
        
        tool_keywords = {
            "query_order_by_id": "订单查询工具",
            "query_customer_by_email": "客户查询工具", 
            "intercept_order_shipping": "订单拦截工具",
            "query_inventory_status": "库存查询工具",
            "query_logistics_status": "物流查询工具",
            "query_product_by_id": "产品查询工具",
            "current_time": "时间工具"
        }
        
        for tool_name, tool_desc in tool_keywords.items():
            if tool_name in response:
                tools.append(tool_desc)
                
        return tools
    
    def _extract_results(self, response: str) -> Dict:
        """从响应中提取结果数据"""
        return {
            "response_length": len(response),
            "processing_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "completed"
        }
    
    async def process_email_stream(self, email_data: EmailData) -> AsyncGenerator[str, None]:
        """流式处理邮件，实时返回进度"""
        yield "🔍 开始分析邮件内容..."
        await asyncio.sleep(0.5)
        
        yield f"📧 邮件主题: {email_data.subject}"
        yield f"👤 发件人: {email_data.sender}"
        yield f"🎯 识别意图: {email_data.parsed_info.get('intent', '未知')}"
        await asyncio.sleep(0.5)
        
        yield "🤖 启动AI Agent处理..."
        await asyncio.sleep(1)
        
        try:
            # 构建提示并处理
            prompt = self._build_processing_prompt(email_data)
            yield "⚙️  正在调用业务工具..."
            
            response = await self._run_agent_async(prompt)
            
            yield "✅ AI处理完成！"
            yield f"📝 处理结果:\n{response}"
            
        except Exception as e:
            yield f"❌ 处理失败: {str(e)}"

# 全局Agent实例
lcsc_agent = None

def get_agent(model_provider: str = "bedrock", model_name: str = "claude-3-7-sonnet") -> LCSCEmailAgent:
    """获取Agent实例（单例模式）"""
    global lcsc_agent
    
    if lcsc_agent is None:
        lcsc_agent = LCSCEmailAgent(model_provider, model_name)
    
    return lcsc_agent
