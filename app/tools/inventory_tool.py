from app.database import SessionLocal
from app.models import Product

def check_low_stock(threshold: int = 5):
    """
    Checks for products with stock below the given threshold using the database.
    """
    db = SessionLocal()
    try:
        low_stock_items = db.query(Product).filter(Product.stock <= threshold).all()
        
        return {
            "status": "success",
            "low_stock_count": len(low_stock_items),
            "threshold": threshold,
            "items": [
                {
                    "id": p.id,
                    "name": p.name,
                    "stock": p.stock,
                    "price": p.price
                }
                for p in low_stock_items
            ]
        }
    finally:
        db.close()

if __name__ == "__main__":
    import json
    # test
    print(json.dumps(check_low_stock(), indent=2))
