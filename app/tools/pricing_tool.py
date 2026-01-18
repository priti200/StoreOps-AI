from sqlalchemy import func
from app.database import SessionLocal
from app.models import Order, Product

def analyze_sales(product_id: str = None):
    """
    Analyzes sales data using the database.
    """
    db = SessionLocal()
    try:
        if product_id:
            # Query for specific product aggregation
            result = db.query(
                func.sum(Order.revenue),
                func.sum(Order.quantity),
                func.count(Order.order_id)
            ).filter(Order.product_id == product_id).first()
            
            total_revenue, total_units, order_count = result
            
            return {
                "status": "success",
                "type": "product_analysis",
                "product_id": product_id,
                "total_revenue": total_revenue or 0.0,
                "total_units_sold": total_units or 0,
                "order_count": order_count or 0
            }
        else:
            # Aggregate all
            result = db.query(
                func.sum(Order.revenue),
                func.count(Order.order_id)
            ).first()
            
            total_revenue, total_orders = result
            
            return {
                "status": "success",
                "type": "aggregate_analysis",
                "total_revenue": total_revenue or 0.0,
                "total_orders": total_orders or 0
            }
    finally:
        db.close()

def suggest_price_change(product_id: str):
    """
    Suggests price change based on DB metrics.
    """
    db = SessionLocal()
    try:
        # Get Product
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"error": f"Product {product_id} not found."}
            
        # Get Sales metrics (re-use logic or manual query)
        # For efficiency, we query directly here
        sales_count = db.query(func.sum(Order.quantity)).filter(Order.product_id == product_id).scalar() or 0
        
        stock = product.stock
        current_price = product.price
        
        suggestion = "KEEP"
        reason = "Balanced metrics."
        new_price_factor = 1.0

        # Mock Logic
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
            "current_price": current_price,
            "suggestion": suggestion,
            "suggested_price": round(current_price * new_price_factor, 2),
            "reason": reason
        }
    finally:
        db.close()

if __name__ == "__main__":
    import json
    print("--- Analyze Sales (All) ---")
    print(json.dumps(analyze_sales(), indent=2))
    print("\n--- Suggest Price (p1) ---")
    print(json.dumps(suggest_price_change("p1"), indent=2))
