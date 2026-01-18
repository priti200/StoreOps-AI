import json
from app.database import SessionLocal, engine
from app.models import Base, Product, Order

# Create tables
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # Seed Products
    try:
        with open("app/data/products.json", "r") as f:
            products_data = json.load(f)
            
        for p in products_data:
            # Check if exists
            existing = db.query(Product).filter(Product.id == p['id']).first()
            if not existing:
                db_product = Product(**p)
                db.add(db_product)
        
        db.commit()
        print("Products seeded.")
    except Exception as e:
        print(f"Error seeding products: {e}")

    # Seed Orders
    try:
        with open("app/data/orders.json", "r") as f:
            orders_data = json.load(f)
            
        for o in orders_data:
            existing = db.query(Order).filter(Order.order_id == o['order_id']).first()
            if not existing:
                db_order = Order(**o)
                db.add(db_order)
        
        db.commit()
        print("Orders seeded.")
    except Exception as e:
        print(f"Error seeding orders: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
