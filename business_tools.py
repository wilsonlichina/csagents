"""
Business Tools Module
Defines LCSC business tools used by the Agent
"""

from strands import tool
from typing import Dict, List, Optional
import random
import time
from datetime import datetime, timedelta

# Mock Database for Global Users
MOCK_CUSTOMERS = {
    "customer1@example.com": {
        "customer_id": "CUST001",
        "name": "Zhang San",
        "email": "customer1@example.com",
        "phone": "+86-138-0000-0001",
        "company": "Shenzhen Technology Co., Ltd.",
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
    },
    "customer3@example.com": {
        "customer_id": "CUST003",
        "name": "Maria Garcia",
        "email": "customer3@example.com",
        "phone": "+34-600-123-456",
        "company": "European Electronics Ltd",
        "country": "Spain",
        "registration_date": "2023-05-10",
        "vip_level": "Bronze"
    }
}

MOCK_ORDERS = {
    "LC123456": {
        "order_id": "LC123456",
        "customer_id": "CUST001",
        "customer_email": "customer1@example.com",
        "status": "Confirmed",
        "create_time": "2024-07-01 10:30:00",
        "total_amount": 1580.50,
        "currency": "CNY",
        "shipping_address": "Nanshan District, Shenzhen Technology Park, China",
        "products": [
            {"product_id": "08-50-0113", "name": "Connector", "quantity": 20000, "unit_price": 0.05},
            {"product_id": "22-01-1042", "name": "Resistor", "quantity": 5000, "unit_price": 0.02}
        ],
        "shipping_status": "Pending Shipment"
    },
    "LC789012": {
        "order_id": "LC789012",
        "customer_id": "CUST002",
        "customer_email": "customer2@example.com", 
        "status": "Shipped",
        "create_time": "2024-06-28 14:20:00",
        "total_amount": 2350.00,
        "currency": "USD",
        "shipping_address": "123 Tech Street, San Francisco, CA 94105, USA",
        "products": [
            {"product_id": "42816-0212", "name": "Microcontroller Chip", "quantity": 200, "unit_price": 11.75}
        ],
        "shipping_status": "In Transit",
        "tracking_number": "SF1234567890"
    },
    "LC345678": {
        "order_id": "LC345678",
        "customer_id": "CUST003",
        "customer_email": "customer3@example.com",
        "status": "Processing",
        "create_time": "2024-07-02 09:15:00",
        "total_amount": 890.25,
        "currency": "EUR",
        "shipping_address": "Calle Mayor 45, Madrid 28013, Spain",
        "products": [
            {"product_id": "08-50-0113", "name": "Connector", "quantity": 5000, "unit_price": 0.05},
            {"product_id": "22-01-1042", "name": "Resistor", "quantity": 10000, "unit_price": 0.02}
        ],
        "shipping_status": "Preparing"
    }
}

MOCK_PRODUCTS = {
    "08-50-0113": {
        "product_id": "08-50-0113",
        "name": "Molex Connector",
        "category": "Connectors",
        "unit_price": 0.05,
        "currency": "CNY",
        "stock_status": "In Stock",
        "stock_quantity": 500000,
        "min_order_qty": 1000,
        "lead_time": "1-3 days"
    },
    "22-01-1042": {
        "product_id": "22-01-1042", 
        "name": "1K Ohm Resistor",
        "category": "Resistors",
        "unit_price": 0.02,
        "currency": "CNY", 
        "stock_status": "In Stock",
        "stock_quantity": 1000000,
        "min_order_qty": 100,
        "lead_time": "1-3 days"
    },
    "42816-0212": {
        "product_id": "42816-0212",
        "name": "STM32 Microcontroller",
        "category": "Microcontrollers",
        "unit_price": 11.75,
        "currency": "USD",
        "stock_status": "On Order",
        "stock_quantity": 0,
        "min_order_qty": 10,
        "lead_time": "4-6 weeks"
    },
    "75-12-3456": {
        "product_id": "75-12-3456",
        "name": "Ceramic Capacitor 10uF",
        "category": "Capacitors",
        "unit_price": 0.08,
        "currency": "USD",
        "stock_status": "In Stock",
        "stock_quantity": 250000,
        "min_order_qty": 500,
        "lead_time": "1-2 days"
    }
}

@tool
def query_order_by_id(order_id: str) -> Dict:
    """
    Query order information by order ID
    
    Args:
        order_id (str): Order ID, e.g. LC123456
        
    Returns:
        Dict: Detailed order information including status, products, amount, etc.
    """
    print(f"🔍 Querying order: {order_id}")
    
    if order_id in MOCK_ORDERS:
        order = MOCK_ORDERS[order_id].copy()
        print(f"✅ Order found: {order_id}, Status: {order['status']}")
        return {
            "success": True,
            "data": order,
            "message": f"Successfully retrieved order {order_id}"
        }
    else:
        print(f"❌ Order not found: {order_id}")
        return {
            "success": False,
            "data": None,
            "message": f"Order {order_id} does not exist"
        }

@tool
def query_customer_by_email(email: str) -> Dict:
    """
    Query customer information by email address
    
    Args:
        email (str): Customer email address
        
    Returns:
        Dict: Detailed customer information
    """
    print(f"🔍 Querying customer: {email}")
    
    if email in MOCK_CUSTOMERS:
        customer = MOCK_CUSTOMERS[email].copy()
        print(f"✅ Customer found: {customer['name']} ({customer['customer_id']})")
        return {
            "success": True,
            "data": customer,
            "message": f"Successfully retrieved customer {email}"
        }
    else:
        print(f"❌ Customer not found: {email}")
        return {
            "success": False,
            "data": None,
            "message": f"Customer {email} does not exist"
        }

@tool
def query_orders_by_customer(customer_email: str) -> Dict:
    """
    Query all orders for a customer by email address
    
    Args:
        customer_email (str): Customer email address
        
    Returns:
        Dict: List of customer orders
    """
    print(f"🔍 Querying customer orders: {customer_email}")
    
    customer_orders = []
    for order_id, order in MOCK_ORDERS.items():
        if order.get("customer_email") == customer_email:
            customer_orders.append(order)
    
    if customer_orders:
        print(f"✅ Found {len(customer_orders)} orders")
        return {
            "success": True,
            "data": customer_orders,
            "message": f"Customer {customer_email} has {len(customer_orders)} orders"
        }
    else:
        print(f"❌ No orders found")
        return {
            "success": False,
            "data": [],
            "message": f"Customer {customer_email} has no orders"
        }

@tool
def query_product_by_id(product_id: str) -> Dict:
    """
    Query product information by product ID
    
    Args:
        product_id (str): Product ID, e.g. 08-50-0113
        
    Returns:
        Dict: Detailed product information
    """
    print(f"🔍 Querying product: {product_id}")
    
    if product_id in MOCK_PRODUCTS:
        product = MOCK_PRODUCTS[product_id].copy()
        print(f"✅ Product found: {product['name']}")
        return {
            "success": True,
            "data": product,
            "message": f"Successfully retrieved product {product_id}"
        }
    else:
        print(f"❌ Product not found: {product_id}")
        return {
            "success": False,
            "data": None,
            "message": f"Product {product_id} does not exist"
        }

@tool
def query_inventory_status(product_id: str) -> Dict:
    """
    Query product inventory status
    
    Args:
        product_id (str): Product ID
        
    Returns:
        Dict: Inventory status information (in stock/on order)
    """
    print(f"🔍 Querying inventory: {product_id}")
    
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
        
        print(f"✅ Stock status: {product['stock_status']}, Quantity: {product['stock_quantity']}")
        return {
            "success": True,
            "data": inventory_info,
            "message": f"Product {product_id} stock status: {product['stock_status']}"
        }
    else:
        print(f"❌ Product not found: {product_id}")
        return {
            "success": False,
            "data": None,
            "message": f"Product {product_id} does not exist"
        }

@tool
def intercept_order_shipping(order_id: str, reason: str) -> Dict:
    """
    Intercept order shipping - Critical business operation
    
    Args:
        order_id (str): Order ID
        reason (str): Reason for interception
        
    Returns:
        Dict: Interception operation result
    """
    print(f"🛑 Intercepting order shipment: {order_id}, Reason: {reason}")
    
    if order_id in MOCK_ORDERS:
        order = MOCK_ORDERS[order_id]
        
        if order["shipping_status"] in ["Shipped", "In Transit", "Delivered"]:
            print(f"❌ Order already shipped, cannot intercept")
            return {
                "success": False,
                "data": None,
                "message": f"Order {order_id} has already been shipped and cannot be intercepted"
            }
        elif order["shipping_status"] == "Intercepted":
            print(f"⚠️  Order already intercepted")
            return {
                "success": True,
                "data": {"status": "Intercepted", "reason": reason},
                "message": f"Order {order_id} is already intercepted"
            }
        else:
            # Execute interception
            MOCK_ORDERS[order_id]["shipping_status"] = "Intercepted"
            MOCK_ORDERS[order_id]["intercept_reason"] = reason
            MOCK_ORDERS[order_id]["intercept_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"✅ Order interception successful")
            return {
                "success": True,
                "data": {
                    "order_id": order_id,
                    "status": "Intercepted",
                    "reason": reason,
                    "intercept_time": MOCK_ORDERS[order_id]["intercept_time"]
                },
                "message": f"Order {order_id} has been successfully intercepted"
            }
    else:
        print(f"❌ Order not found: {order_id}")
        return {
            "success": False,
            "data": None,
            "message": f"Order {order_id} does not exist"
        }

@tool
def query_logistics_status(order_id: str) -> Dict:
    """
    Query order logistics status
    
    Args:
        order_id (str): Order ID
        
    Returns:
        Dict: Logistics status information
    """
    print(f"🚚 Querying logistics status: {order_id}")
    
    if order_id in MOCK_ORDERS:
        order = MOCK_ORDERS[order_id]
        
        logistics_info = {
            "order_id": order_id,
            "shipping_status": order["shipping_status"],
            "tracking_number": order.get("tracking_number", ""),
            "shipping_address": order["shipping_address"],
            "estimated_delivery": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        }
        
        # Simulate tracking history
        if order["shipping_status"] == "In Transit":
            logistics_info["tracking_history"] = [
                {"time": "2024-07-01 10:00", "status": "Shipped", "location": "Shenzhen Warehouse"},
                {"time": "2024-07-01 18:00", "status": "In Transit", "location": "Shenzhen Distribution Center"},
                {"time": "2024-07-02 08:00", "status": "In Transit", "location": "Guangzhou Distribution Center"}
            ]
        elif order["shipping_status"] == "Preparing":
            logistics_info["tracking_history"] = [
                {"time": "2024-07-02 09:15", "status": "Order Confirmed", "location": "LCSC System"},
                {"time": "2024-07-02 14:30", "status": "Preparing", "location": "Madrid Warehouse"}
            ]
        
        print(f"✅ Logistics status: {order['shipping_status']}")
        return {
            "success": True,
            "data": logistics_info,
            "message": f"Order {order_id} logistics status: {order['shipping_status']}"
        }
    else:
        print(f"❌ Order not found: {order_id}")
        return {
            "success": False,
            "data": None,
            "message": f"Order {order_id} does not exist"
        }

# Business tools list for Agent usage
BUSINESS_TOOLS = [
    query_order_by_id,
    query_customer_by_email,
    query_orders_by_customer,
    query_product_by_id,
    query_inventory_status,
    intercept_order_shipping,
    query_logistics_status
]
