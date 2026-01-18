import json
from typing import List, Dict, Any

def check_low_stock(threshold: int = 5) -> Dict[str, Any]:
    """
    Checks for products with stock below the given threshold.
    
    Args:
        threshold (int): The stock level below which a product is considered low stock.
        
    Returns:
        Dict[str, Any]: A dictionary containing the list of low stock items and a summary.
    """
    products_path = "app/data/products.json"
    try:
        with open(products_path, "r") as f:
            products = json.load(f)
    except FileNotFoundError:
        return {"error": "Products data not found."}
        
    low_stock_items = [p for p in products if p['stock'] <= threshold]
    
    return {
        "status": "success",
        "low_stock_count": len(low_stock_items),
        "threshold": threshold,
        "items": [
            {
                "id": p['id'],
                "name": p['name'],
                "stock": p['stock'],
                "price": p['price']
            }
            for p in low_stock_items
        ]
    }

if __name__ == "__main__":
    # Test
    result = check_low_stock()
    print(json.dumps(result, indent=2))
