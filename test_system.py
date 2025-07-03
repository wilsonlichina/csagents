#!/usr/bin/env python3
"""
LCSC邮件客服系统测试脚本
"""

import sys
import traceback

def test_email_manager():
    """测试邮件管理模块"""
    print("🧪 测试邮件管理模块...")
    try:
        from email_manager import email_manager
        emails = email_manager.load_emails()
        df = email_manager.get_email_list()
        
        print(f"✅ 成功加载 {len(emails)} 封邮件")
        print(f"✅ 邮件列表DataFrame形状: {df.shape}")
        
        if len(emails) > 0:
            sample_email = emails[0]
            print(f"✅ 示例邮件: {sample_email.subject}")
            print(f"   意图: {sample_email.parsed_info.get('intent', '未知')}")
            print(f"   类型: {sample_email.parsed_info.get('email_type', '未知')}")
        
        return True
    except Exception as e:
        print(f"❌ 邮件管理模块测试失败: {e}")
        traceback.print_exc()
        return False

def test_business_tools():
    """测试业务工具模块"""
    print("\n🧪 测试业务工具模块...")
    try:
        from business_tools import (
            query_order_by_id, 
            query_customer_by_email,
            query_inventory_status,
            intercept_order_shipping
        )
        
        # 测试订单查询
        result = query_order_by_id("LC123456")
        assert result["success"], "订单查询失败"
        print("✅ 订单查询工具测试通过")
        
        # 测试客户查询
        result = query_customer_by_email("customer1@example.com")
        assert result["success"], "客户查询失败"
        print("✅ 客户查询工具测试通过")
        
        # 测试库存查询
        result = query_inventory_status("08-50-0113")
        assert result["success"], "库存查询失败"
        print("✅ 库存查询工具测试通过")
        
        # 测试订单拦截
        result = intercept_order_shipping("LC123456", "客户要求修改地址")
        assert result["success"], "订单拦截失败"
        print("✅ 订单拦截工具测试通过")
        
        return True
    except Exception as e:
        print(f"❌ 业务工具模块测试失败: {e}")
        traceback.print_exc()
        return False

def test_ai_agent():
    """测试AI Agent模块"""
    print("\n🧪 测试AI Agent模块...")
    try:
        from ai_agent import get_agent
        
        # 创建Agent实例（不实际调用模型）
        agent = get_agent()
        print("✅ AI Agent创建成功")
        print(f"   模型提供商: {agent.model_provider}")
        print(f"   模型名称: {agent.model_name}")
        
        return True
    except Exception as e:
        print(f"❌ AI Agent模块测试失败: {e}")
        traceback.print_exc()
        return False

def test_gradio_interface():
    """测试Gradio界面模块"""
    print("\n🧪 测试Gradio界面模块...")
    try:
        from gradio_interface import create_interface
        
        # 创建界面（不启动服务器）
        demo = create_interface()
        print("✅ Gradio界面创建成功")
        print(f"   界面类型: {type(demo)}")
        
        return True
    except Exception as e:
        print(f"❌ Gradio界面模块测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 LCSC邮件客服系统 - 系统测试")
    print("=" * 50)
    
    tests = [
        test_email_manager,
        test_business_tools,
        test_ai_agent,
        test_gradio_interface
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统准备就绪。")
        print("\n🚀 启动系统:")
        print("   ./run.sh")
        print("   或")
        print("   python3 main.py")
        return 0
    else:
        print("❌ 部分测试失败，请检查错误信息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
