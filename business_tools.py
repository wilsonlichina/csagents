"""
业务工具模块
定义Agent使用的LCSC业务工具
"""

from strands import tool
from typing import Dict, List, Optional
import random
import time
from datetime import datetime, timedelta

# 模拟数据库
MOCK_CUSTOMERS = {
    "customer1@example.com": {
        "customer_id": "CUST001",
        "name": "张三",
        "email": "customer1@example.com",
        "phone": "+86-138-0000-0001",
        "company": "深圳科技有限公司",
        "country": "China",
        "registration_date": "2023-01-15",
        "vip_level": "Gold"
    },
    "customer2@example.com": {
        "customer_id": "CUST002", 
        "name": "John Smith",
        "email": "customer2@example.com",
        "phone": "+1-555-0123",
        "company": "Tech Solutions Inc",
        "country": "United States",
        "registration_date": "2023-03-20",
        "vip_level": "Silver"
    }
}

MOCK_ORDERS = {
    "LC123456": {
        "order_id": "LC123456",
        "customer_id": "CUST001",
        "customer_email": "customer1@example.com",
        "status": "已确认",
        "create_time": "2024-07-01 10:30:00",
        "total_amount": 1580.50,
        "currency": "CNY",
        "shipping_address": "深圳市南山区科技园南区",
        "products": [
            {"product_id": "08-50-0113", "name": "连接器", "quantity": 20000, "unit_price": 0.05},
            {"product_id": "22-01-1042", "name": "电阻", "quantity": 5000, "unit_price": 0.02}
        ],
        "shipping_status": "待发货"
    },
    "LC789012": {
        "order_id": "LC789012",
        "customer_id": "CUST002",
        "customer_email": "customer2@example.com", 
        "status": "已发货",
        "create_time": "2024-06-28 14:20:00",
        "total_amount": 2350.00,
        "currency": "USD",
        "shipping_address": "123 Tech Street, San Francisco, CA 94105",
        "products": [
            {"product_id": "42816-0212", "name": "芯片", "quantity": 200, "unit_price": 11.75}
        ],
        "shipping_status": "运输中",
        "tracking_number": "SF1234567890"
    }
}

MOCK_PRODUCTS = {
    "08-50-0113": {
        "product_id": "08-50-0113",
        "name": "Molex 连接器",
        "category": "连接器",
        "unit_price": 0.05,
        "currency": "CNY",
        "stock_status": "现货",
        "stock_quantity": 500000,
        "min_order_qty": 1000,
        "lead_time": "1-3天"
    },
    "22-01-1042": {
        "product_id": "22-01-1042", 
        "name": "1K欧姆电阻",
        "category": "电阻",
        "unit_price": 0.02,
        "currency": "CNY", 
        "stock_status": "现货",
        "stock_quantity": 1000000,
        "min_order_qty": 100,
        "lead_time": "1-3天"
    },
    "42816-0212": {
        "product_id": "42816-0212",
        "name": "STM32 微控制器",
        "category": "芯片",
        "unit_price": 11.75,
        "currency": "USD",
        "stock_status": "订货",
        "stock_quantity": 0,
        "min_order_qty": 10,
        "lead_time": "4-6周"
    }
}

@tool
def query_order_by_id(order_id: str) -> Dict:
    """
    根据订单号查询订单信息
    
    Args:
        order_id (str): 订单号，如 LC123456
        
    Returns:
        Dict: 订单详细信息，包括状态、产品、金额等
    """
    print(f"🔍 查询订单: {order_id}")
    
    if order_id in MOCK_ORDERS:
        order = MOCK_ORDERS[order_id].copy()
        print(f"✅ 找到订单: {order_id}, 状态: {order['status']}")
        return {
            "success": True,
            "data": order,
            "message": f"成功查询到订单 {order_id}"
        }
    else:
        print(f"❌ 订单不存在: {order_id}")
        return {
            "success": False,
            "data": None,
            "message": f"订单 {order_id} 不存在"
        }

@tool
def query_customer_by_email(email: str) -> Dict:
    """
    根据邮箱查询客户信息
    
    Args:
        email (str): 客户邮箱地址
        
    Returns:
        Dict: 客户详细信息
    """
    print(f"🔍 查询客户: {email}")
    
    if email in MOCK_CUSTOMERS:
        customer = MOCK_CUSTOMERS[email].copy()
        print(f"✅ 找到客户: {customer['name']} ({customer['customer_id']})")
        return {
            "success": True,
            "data": customer,
            "message": f"成功查询到客户 {email}"
        }
    else:
        print(f"❌ 客户不存在: {email}")
        return {
            "success": False,
            "data": None,
            "message": f"客户 {email} 不存在"
        }

@tool
def query_orders_by_customer(customer_email: str) -> Dict:
    """
    根据客户邮箱查询该客户的所有订单
    
    Args:
        customer_email (str): 客户邮箱地址
        
    Returns:
        Dict: 客户的订单列表
    """
    print(f"🔍 查询客户订单: {customer_email}")
    
    customer_orders = []
    for order_id, order in MOCK_ORDERS.items():
        if order.get("customer_email") == customer_email:
            customer_orders.append(order)
    
    if customer_orders:
        print(f"✅ 找到 {len(customer_orders)} 个订单")
        return {
            "success": True,
            "data": customer_orders,
            "message": f"客户 {customer_email} 共有 {len(customer_orders)} 个订单"
        }
    else:
        print(f"❌ 未找到订单")
        return {
            "success": False,
            "data": [],
            "message": f"客户 {customer_email} 暂无订单"
        }

@tool
def query_product_by_id(product_id: str) -> Dict:
    """
    根据产品ID查询产品信息
    
    Args:
        product_id (str): 产品ID，如 08-50-0113
        
    Returns:
        Dict: 产品详细信息
    """
    print(f"🔍 查询产品: {product_id}")
    
    if product_id in MOCK_PRODUCTS:
        product = MOCK_PRODUCTS[product_id].copy()
        print(f"✅ 找到产品: {product['name']}")
        return {
            "success": True,
            "data": product,
            "message": f"成功查询到产品 {product_id}"
        }
    else:
        print(f"❌ 产品不存在: {product_id}")
        return {
            "success": False,
            "data": None,
            "message": f"产品 {product_id} 不存在"
        }

@tool
def query_inventory_status(product_id: str) -> Dict:
    """
    查询产品库存状态
    
    Args:
        product_id (str): 产品ID
        
    Returns:
        Dict: 库存状态信息（现货/订货）
    """
    print(f"🔍 查询库存: {product_id}")
    
    if product_id in MOCK_PRODUCTS:
        product = MOCK_PRODUCTS[product_id]
        inventory_info = {
            "product_id": product_id,
            "product_name": product["name"],
            "stock_status": product["stock_status"],
            "stock_quantity": product["stock_quantity"],
            "min_order_qty": product["min_order_qty"],
            "lead_time": product["lead_time"],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print(f"✅ 库存状态: {product['stock_status']}, 数量: {product['stock_quantity']}")
        return {
            "success": True,
            "data": inventory_info,
            "message": f"产品 {product_id} 库存状态: {product['stock_status']}"
        }
    else:
        print(f"❌ 产品不存在: {product_id}")
        return {
            "success": False,
            "data": None,
            "message": f"产品 {product_id} 不存在"
        }

@tool
def intercept_order_shipping(order_id: str, reason: str) -> Dict:
    """
    拦截订单发货
    
    Args:
        order_id (str): 订单号
        reason (str): 拦截原因
        
    Returns:
        Dict: 拦截操作结果
    """
    print(f"🛑 拦截订单发货: {order_id}, 原因: {reason}")
    
    if order_id in MOCK_ORDERS:
        order = MOCK_ORDERS[order_id]
        
        if order["shipping_status"] == "已发货":
            print(f"❌ 订单已发货，无法拦截")
            return {
                "success": False,
                "data": None,
                "message": f"订单 {order_id} 已发货，无法拦截"
            }
        elif order["shipping_status"] == "已拦截":
            print(f"⚠️  订单已被拦截")
            return {
                "success": True,
                "data": {"status": "已拦截", "reason": reason},
                "message": f"订单 {order_id} 已处于拦截状态"
            }
        else:
            # 执行拦截操作
            MOCK_ORDERS[order_id]["shipping_status"] = "已拦截"
            MOCK_ORDERS[order_id]["intercept_reason"] = reason
            MOCK_ORDERS[order_id]["intercept_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"✅ 订单拦截成功")
            return {
                "success": True,
                "data": {
                    "order_id": order_id,
                    "status": "已拦截",
                    "reason": reason,
                    "intercept_time": MOCK_ORDERS[order_id]["intercept_time"]
                },
                "message": f"订单 {order_id} 拦截成功"
            }
    else:
        print(f"❌ 订单不存在: {order_id}")
        return {
            "success": False,
            "data": None,
            "message": f"订单 {order_id} 不存在"
        }

@tool
def query_logistics_status(order_id: str) -> Dict:
    """
    查询订单物流状态
    
    Args:
        order_id (str): 订单号
        
    Returns:
        Dict: 物流状态信息
    """
    print(f"🚚 查询物流状态: {order_id}")
    
    if order_id in MOCK_ORDERS:
        order = MOCK_ORDERS[order_id]
        
        logistics_info = {
            "order_id": order_id,
            "shipping_status": order["shipping_status"],
            "tracking_number": order.get("tracking_number", ""),
            "shipping_address": order["shipping_address"],
            "estimated_delivery": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        }
        
        # 模拟物流轨迹
        if order["shipping_status"] == "运输中":
            logistics_info["tracking_history"] = [
                {"time": "2024-07-01 10:00", "status": "已发货", "location": "深圳仓库"},
                {"time": "2024-07-01 18:00", "status": "运输中", "location": "深圳转运中心"},
                {"time": "2024-07-02 08:00", "status": "运输中", "location": "广州转运中心"}
            ]
        
        print(f"✅ 物流状态: {order['shipping_status']}")
        return {
            "success": True,
            "data": logistics_info,
            "message": f"订单 {order_id} 物流状态: {order['shipping_status']}"
        }
    else:
        print(f"❌ 订单不存在: {order_id}")
        return {
            "success": False,
            "data": None,
            "message": f"订单 {order_id} 不存在"
        }

# 工具列表，供Agent使用
BUSINESS_TOOLS = [
    query_order_by_id,
    query_customer_by_email,
    query_orders_by_customer,
    query_product_by_id,
    query_inventory_status,
    intercept_order_shipping,
    query_logistics_status
]
