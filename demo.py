#!/usr/bin/env python3
"""
LCSC邮件客服系统演示脚本
展示系统的核心功能
"""

import asyncio
from email_manager import email_manager
from ai_agent import get_agent
from business_tools import query_order_by_id, intercept_order_shipping

async def demo_email_processing():
    """演示邮件处理流程"""
    print("🎬 LCSC邮件客服系统功能演示")
    print("=" * 60)
    
    # 1. 加载邮件
    print("\n📧 步骤1: 加载邮件")
    emails = email_manager.load_emails()
    print(f"✅ 成功加载 {len(emails)} 封邮件")
    
    # 2. 展示邮件列表
    print("\n📋 步骤2: 邮件列表概览")
    for i, email in enumerate(emails[:3]):  # 只显示前3封
        print(f"   {i+1}. {email.subject}")
        print(f"      发件人: {email.sender}")
        print(f"      意图: {email.parsed_info.get('intent', '未知')}")
        print(f"      类型: {email.parsed_info.get('email_type', '未知')}")
        print()
    
    # 3. 演示业务工具
    print("🛠️  步骤3: 业务工具演示")
    
    print("\n   3.1 订单查询工具")
    result = query_order_by_id("LC123456")
    if result["success"]:
        order = result["data"]
        print(f"   ✅ 订单 {order['order_id']}")
        print(f"      状态: {order['status']}")
        print(f"      金额: {order['total_amount']} {order['currency']}")
        print(f"      发货状态: {order['shipping_status']}")
    
    print("\n   3.2 订单拦截工具")
    result = intercept_order_shipping("LC123456", "演示：客户要求修改发货地址")
    if result["success"]:
        print(f"   ✅ 订单拦截成功")
        print(f"      拦截时间: {result['data']['intercept_time']}")
        print(f"      拦截原因: {result['data']['reason']}")
    
    # 4. AI Agent处理演示（模拟）
    print("\n🤖 步骤4: AI Agent处理演示")
    
    if len(emails) > 0:
        sample_email = emails[0]
        print(f"   处理邮件: {sample_email.subject}")
        print(f"   发件人: {sample_email.sender}")
        print(f"   识别意图: {sample_email.parsed_info.get('intent', '未知')}")
        
        # 模拟AI处理结果
        print("\n   🔍 AI分析结果:")
        print("   - 邮件类型: 产品询问")
        print("   - 客户意图: 查询产品信息和价格")
        print("   - 建议操作: 查询产品库存和价格信息")
        print("   - 回复模板: 专业产品咨询回复")
    
    print("\n" + "=" * 60)
    print("🎉 演示完成！")
    print("\n📝 系统功能总结:")
    print("✅ 邮件自动解析和分类")
    print("✅ 智能意图识别")
    print("✅ 业务工具自动调用")
    print("✅ 订单拦截和处理")
    print("✅ 现代化Web界面")
    print("✅ AI驱动的客服回复")
    
    print("\n🚀 启动完整系统:")
    print("   ./run.sh")
    print("   然后访问: http://localhost:7860")

if __name__ == "__main__":
    asyncio.run(demo_email_processing())
