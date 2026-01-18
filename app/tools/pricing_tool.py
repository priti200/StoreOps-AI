import json
from typing import List, Dict, Any

def analyze_sales(product_id: str = None) -> Dict[str, Any]:
    """
    Analyzes sales data. If product_id is provided, analyzes for that specific product.
    Otherwise, returns aggregate sales data.
    """
    orders_path = "app/data/orders.json"
    try:
        with open(orders_path, "r") as f:
            orders = json.load(f)
    except FileNotFoundError:
        return {"error": "Orders data not found."}

    if product_id:
        product_sales = [o for o in orders if o['product_id'] == product_id]
        total_revenue = sum(o['revenue'] for o in product_sales)
        total_units = sum(o['quantity'] for o in product_sales)
        return {
            "status": "success",
            "type": "product_analysis",
            "product_id": product_id,
            "total_revenue": total_revenue,
            "total_units_sold": total_units,
            "order_count": len(product_sales)
        }
    else:
        total_revenue = sum(o['revenue'] for o in orders)
        return {
            "status": "success",
            "type": "aggregate_analysis",
            "total_revenue": total_revenue,
            "total_orders": len(orders)
        }

def suggest_price_change(product_id: str) -> Dict[str, Any]:
    """
    Suggests a price change based on sales velocity and stock.
    (Mock logic: if stock is low & sales high -> increase price; if stock high & sales low -> decrease)
    """
    # This mock requires access to both products and sales. Use tools or load data directly.
    # For simplicity, we load data here.
    
    metrics = analyze_sales(product_id)
    if "error" in metrics:
        return metrics
        
    # Load product details for stock
    products_path = "app/data/products.json"
    try:
        with open(products_path, "r") as f:
            products = json.load(f)
            product = next((p for p in products if p['id'] == product_id), None)
            if not product:
                 return {"error": f"Product {product_id} not found."}
    except FileNotFoundError:
        return {"error": "Products data not found."}

    stock = product['stock']
    sales_count = metrics['total_units_sold'] # Mock assumption: use total units sold as proxy for recent demand
    
    suggestion = "KEEP"
    reason = "Balanced metrics."
    new_price_factor = 1.0

    if stock < 5 and sales_count > 10:
        suggestion = "INCREASE"
        reason = "High demand (sales > 10) and low stock (< 5)."
        new_price_factor = 1.10
    elif stock > 50 and sales_count < 5:
        suggestion = "DECREASE"
        reason = "Low demand (sales < 5) and high stock (> 50)."
        new_price_factor = 0.90
        
    return {
        "status": "success",
        "product_id": product_id,
        "current_price": product['price'],
        "suggestion": suggestion,
        "suggested_price": round(product['price'] * new_price_factor, 2),
        "reason": reason
    }

if __name__ == "__main__":
    print("--- Analyze Sales (All) ---")
    print(json.dumps(analyze_sales(), indent=2))
    print("\n--- Suggest Price (p1 - Headphones) ---")
    print(json.dumps(suggest_price_change("p1"), indent=2))
    print("\n--- Suggest Price (p3 - Green Tea) ---")
    print(json.dumps(suggest_price_change("p3"), indent=2))
