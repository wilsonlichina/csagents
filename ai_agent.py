"""
AI Agent Module
Using Strands SDK to define LCSC Email Customer Service Intelligent Agent
"""

import asyncio
from typing import Dict, List, Optional, AsyncGenerator, Tuple
from dataclasses import dataclass
from datetime import datetime

from strands import Agent
from strands_tools import current_time
from strands.models import BedrockModel
from business_tools import BUSINESS_TOOLS
from email_manager import EmailData

@dataclass
class ProcessingResult:
    """Processing result data structure"""
    email_id: str
    intent: str
    confidence: float
    actions_taken: List[str]
    tools_used: List[str]
    results: Dict
    response: str
    timestamp: str

class LCSCEmailAgent:
    """LCSC Email Customer Service Intelligent Agent"""
    
    # Model name to model ID mapping
    MODEL_MAPPING = {
        "claude-3-5-sonnet": "us.anthropic.claude-3-5-sonnet-20240620-v1:0",
        "claude-3-7-sonnet": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    }
    
    def __init__(self, model_provider: str = "bedrock", model_name: str = "claude-3-7-sonnet"):
        """
        Initialize Agent
        
        Args:
            model_provider: Model provider (bedrock, openai, etc.)
            model_name: Model name (claude-3-5-sonnet, claude-3-7-sonnet)
        """
        self.model_provider = model_provider
        self.model_name = model_name
        
        # Get corresponding model ID
        model_id = self._get_model_id(model_name)
        
        print(f"🔧 Model mapping: {model_name} -> {model_id}")

        # Create a BedrockModel
        bedrock_model = BedrockModel(
            model_id=model_id,
            region_name='us-west-2',
            temperature=0.3,
            )
        
        # Create Strands Agent
        self.agent = Agent(
            model=bedrock_model,
            tools=BUSINESS_TOOLS + [current_time],
            system_prompt=self._get_system_prompt()
        )
        
        print(f"🤖 LCSC Email Customer Service Agent initialized successfully")
        print(f"   Model: {model_provider}/{model_name}")
        print(f"   Model ID: {model_id}")
        print(f"   Number of tools: {len(BUSINESS_TOOLS) + 1}")
    
    def _get_model_id(self, model_name: str) -> str:
        """
        Get corresponding model ID based on model name
        
        Args:
            model_name: Model name
            
        Returns:
            str: Corresponding model ID
            
        Raises:
            ValueError: If model name is not supported
        """
        if model_name in self.MODEL_MAPPING:
            return self.MODEL_MAPPING[model_name]
        else:
            # If no mapping found, list supported models
            supported_models = list(self.MODEL_MAPPING.keys())
            raise ValueError(
                f"Unsupported model name: {model_name}\n"
                f"Supported models: {', '.join(supported_models)}"
            )
    
    @classmethod
    def get_supported_models(cls) -> List[str]:
        """Get list of supported models"""
        return list(cls.MODEL_MAPPING.keys())
    
    @classmethod
    def get_model_id_by_name(cls, model_name: str) -> str:
        """Get model ID by model name (class method)"""
        if model_name in cls.MODEL_MAPPING:
            return cls.MODEL_MAPPING[model_name]
        else:
            supported_models = list(cls.MODEL_MAPPING.keys())
            raise ValueError(
                f"Unsupported model name: {model_name}\n"
                f"Supported models: {', '.join(supported_models)}"
            )
    
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
        Process email and return results
        
        Args:
            email_data: Email data
            progress_callback: Progress callback function
            
        Returns:
            ProcessingResult: Processing results
        """
        try:
            if progress_callback:
                progress_callback("🔍 Starting email content analysis...")
            
            # Build processing prompt
            prompt = self._build_processing_prompt(email_data)
            
            if progress_callback:
                progress_callback("🤖 AI Agent is processing...")
            
            # Process with Agent
            response = await self._run_agent_async(prompt)
            
            if progress_callback:
                progress_callback("📊 Analyzing processing results...")
            
            # Analyze results
            result = ProcessingResult(
                email_id=email_data.file_name,
                intent=email_data.parsed_info.get('intent', 'Unknown'),
                confidence=0.85,  # Simulated confidence
                actions_taken=self._extract_actions(response),
                tools_used=self._extract_tools_used(response),
                results=self._extract_results(response),
                response=response,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            if progress_callback:
                progress_callback("✅ Processing completed!")
            
            return result
            
        except Exception as e:
            error_msg = f"Error occurred while processing email: {str(e)}"
            print(f"❌ {error_msg}")
            
            return ProcessingResult(
                email_id=email_data.file_name,
                intent="Processing failed",
                confidence=0.0,
                actions_taken=["Error handling"],
                tools_used=[],
                results={"error": error_msg},
                response=error_msg,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
    
    def _build_processing_prompt(self, email_data: EmailData) -> str:
        """Build processing prompt"""
        return f"""
Please analyze and process the following customer email:

## Email Information
- File name: {email_data.file_name}
- Subject: {email_data.subject}
- Sender: {email_data.sender}
- Send time: {email_data.send_time}
- Email type: {email_data.parsed_info.get('email_type', 'Unknown')}
- Identified intent: {email_data.parsed_info.get('intent', 'Unknown')}

## Email Content
{email_data.content}

## Extracted Product Information
{email_data.parsed_info.get('products', [])}

## Processing Requirements
1. Based on email content and sender information, query relevant customer and order information
2. If order changes are involved (address modification, product addition/removal, order cancellation, order merging), immediately execute order interception
3. Provide professional customer service response, including:
   - Confirm receipt of customer request
   - Explain operations that have been executed
   - Provide relevant order/product information
   - Give follow-up processing recommendations

Please start processing this email.
"""
    
    async def _run_agent_async(self, prompt: str) -> str:
        """Run Agent asynchronously"""
        try:
            # Since Strands Agent may not support async, we run it in thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self.agent, prompt)
            return str(response)
        except Exception as e:
            print(f"Agent execution error: {str(e)}")
            return f"Agent processing failed: {str(e)}"
    
    def _extract_actions(self, response: str) -> List[str]:
        """Extract executed actions from response"""
        actions = []
        
        # Simple keyword matching to identify actions
        if "query order" in response.lower() or "query_order_by_id" in response:
            actions.append("Query order information")
        if "query customer" in response.lower() or "query_customer_by_email" in response:
            actions.append("Query customer information")
        if "intercept shipping" in response.lower() or "intercept_order_shipping" in response:
            actions.append("Intercept order shipping")
        if "query inventory" in response.lower() or "query_inventory_status" in response:
            actions.append("Query inventory status")
        if "query logistics" in response.lower() or "query_logistics_status" in response:
            actions.append("Query logistics status")
        if "query product" in response.lower() or "query_product_by_id" in response:
            actions.append("Query product information")
            
        return actions if actions else ["Analyze email content"]
    
    def _extract_tools_used(self, response: str) -> List[str]:
        """Extract tools used from response"""
        tools = []
        
        tool_keywords = {
            "query_order_by_id": "Order Query Tool",
            "query_customer_by_email": "Customer Query Tool", 
            "intercept_order_shipping": "Order Interception Tool",
            "query_inventory_status": "Inventory Query Tool",
            "query_logistics_status": "Logistics Query Tool",
            "query_product_by_id": "Product Query Tool",
            "current_time": "Time Tool"
        }
        
        for tool_name, tool_desc in tool_keywords.items():
            if tool_name in response:
                tools.append(tool_desc)
                
        return tools
    
    def _extract_results(self, response: str) -> Dict:
        """Extract result data from response"""
        return {
            "response_length": len(response),
            "processing_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "completed"
        }
    
    async def process_email_stream(self, email_data: EmailData) -> AsyncGenerator[str, None]:
        """Stream process email, return progress in real-time"""
        yield "🔍 Starting email content analysis..."
        await asyncio.sleep(0.5)
        
        yield f"📧 Email subject: {email_data.subject}"
        yield f"👤 Sender: {email_data.sender}"
        yield f"🎯 Identified intent: {email_data.parsed_info.get('intent', 'Unknown')}"
        await asyncio.sleep(0.5)
        
        yield "🤖 Starting AI Agent processing..."
        await asyncio.sleep(1)
        
        try:
            # Build prompt and process
            prompt = self._build_processing_prompt(email_data)
            yield "⚙️  Calling business tools..."
            
            response = await self._run_agent_async(prompt)
            
            yield "✅ AI processing completed!"
            yield f"📝 Processing results:\n{response}"
            
        except Exception as e:
            yield f"❌ Processing failed: {str(e)}"

# Global Agent instance
lcsc_agent = None
current_model_config = None

def get_agent(model_provider: str = "bedrock", model_name: str = "claude-3-7-sonnet") -> LCSCEmailAgent:
    """
    Get Agent instance (singleton pattern, supports model switching)
    
    Args:
        model_provider: Model provider
        model_name: Model name
        
    Returns:
        LCSCEmailAgent: Agent instance
    """
    global lcsc_agent, current_model_config
    
    new_config = (model_provider, model_name)
    
    # If configuration changes or Agent doesn't exist, recreate
    if lcsc_agent is None or current_model_config != new_config:
        print(f"🔄 Creating new Agent instance: {model_provider}/{model_name}")
        lcsc_agent = LCSCEmailAgent(model_provider, model_name)
        current_model_config = new_config
    
    return lcsc_agent

def reset_agent():
    """Reset Agent instance"""
    global lcsc_agent, current_model_config
    lcsc_agent = None
    current_model_config = None
    print("🔄 Agent instance has been reset")

def get_available_models() -> Dict[str, str]:
    """
    Get list of available models
    
    Returns:
        Dict[str, str]: Model name to model ID mapping
    """
    return LCSCEmailAgent.MODEL_MAPPING.copy()

def validate_model_name(model_name: str) -> bool:
    """
    Validate if model name is supported
    
    Args:
        model_name: Model name to validate
        
    Returns:
        bool: Whether the model is supported
    """
    return model_name in LCSCEmailAgent.MODEL_MAPPING

def get_model_info(model_name: str) -> Dict[str, str]:
    """
    Get model information
    
    Args:
        model_name: Model name
        
    Returns:
        Dict[str, str]: Dictionary containing model name and ID
    """
    if validate_model_name(model_name):
        return {
            "model_name": model_name,
            "model_id": LCSCEmailAgent.MODEL_MAPPING[model_name],
            "provider": "bedrock"
        }
    else:
        raise ValueError(f"Unsupported model name: {model_name}")

# Convenience function: print all supported models
def print_supported_models():
    """Print all supported models"""
    print("🤖 Supported models list:")
    for model_name, model_id in LCSCEmailAgent.MODEL_MAPPING.items():
        print(f"   {model_name} -> {model_id}")
    print(f"   Total: {len(LCSCEmailAgent.MODEL_MAPPING)} models")
