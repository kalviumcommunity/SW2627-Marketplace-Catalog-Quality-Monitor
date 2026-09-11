
import pandas as pd
from validator import validate_catalog

def test_negative_price():
    df = pd.DataFrame([{
        "feed_id": "F1", "seller_id": "S1", "product_id": "P1",
        "sku": "S1-P1", "product_name": "Test", "category": "Electronics",
        "mrp": 100, "selling_price": -10, "inventory": 5,
        "last_updated": "2026-09-01"
    }])
    issues = validate_catalog(df)
    assert "Invalid Price" in issues["issue_type"].values

def test_negative_inventory():
    df = pd.DataFrame([{
        "feed_id": "F2", "seller_id": "S1", "product_id": "P2",
        "sku": "S1-P2", "product_name": "Test", "category": "Home",
        "mrp": 100, "selling_price": 90, "inventory": -1,
        "last_updated": "2026-09-01"
    }])
    issues = validate_catalog(df)
    assert "Invalid Inventory" in issues["issue_type"].values
