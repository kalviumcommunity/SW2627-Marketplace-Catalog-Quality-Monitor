
import pandas as pd
import numpy as np

ALLOWED_CATEGORIES = {
    "Electronics", "Home", "Fashion", "Beauty", "Sports", "Books"
}

REQUIRED_FIELDS = [
    "feed_id", "seller_id", "product_id", "sku",
    "product_name", "category", "selling_price",
    "inventory", "last_updated"
]

def validate_catalog(df: pd.DataFrame) -> pd.DataFrame:
    issues = []

    def add_issue(row, issue_type, severity, field, message):
        issues.append({
            "feed_id": row.get("feed_id"),
            "seller_id": row.get("seller_id"),
            "product_id": row.get("product_id"),
            "sku": row.get("sku"),
            "issue_type": issue_type,
            "severity": severity,
            "field": field,
            "message": message,
        })

    # Required fields
    for _, row in df.iterrows():
        for field in REQUIRED_FIELDS:
            if field in row and pd.isna(row[field]):
                add_issue(row, "Missing Required Field", "HIGH", field,
                          f"{field} is missing")

    # Price rules
    for _, row in df.iterrows():
        price = row.get("selling_price")
        mrp = row.get("mrp")
        if pd.notna(price):
            if price <= 0:
                add_issue(row, "Invalid Price", "CRITICAL", "selling_price",
                          "Selling price must be greater than zero")
        if pd.notna(price) and pd.notna(mrp) and mrp < price:
            add_issue(row, "MRP Inconsistency", "HIGH", "mrp",
                      "MRP is lower than selling price")

    # Inventory
    for _, row in df.iterrows():
        inv = row.get("inventory")
        if pd.notna(inv) and inv < 0:
            add_issue(row, "Invalid Inventory", "CRITICAL", "inventory",
                      "Inventory cannot be negative")

    # Categories
    for _, row in df.iterrows():
        category = row.get("category")
        if pd.notna(category) and category not in ALLOWED_CATEGORIES:
            add_issue(row, "Invalid Category", "MEDIUM", "category",
                      f"Category '{category}' is not in the approved category list")

    # Duplicate SKU
    if "sku" in df.columns:
        duplicate_mask = df["sku"].notna() & df["sku"].duplicated(keep=False)
        for _, row in df[duplicate_mask].iterrows():
            add_issue(row, "Duplicate SKU", "HIGH", "sku",
                      "SKU occurs multiple times in the feed")

    # Duplicate seller-product combinations. The same product may legitimately
    # be sold by multiple sellers, so product_id alone is not a duplicate key.
    if "seller_id" in df.columns and "product_id" in df.columns:
        duplicate_mask = (
            df["seller_id"].notna() & df["product_id"].notna()
            & df.duplicated(["seller_id", "product_id"], keep=False)
        )
        for _, row in df[duplicate_mask].iterrows():
            add_issue(row, "Duplicate Seller-Product", "HIGH", "product_id",
                      "The same seller submitted the same product more than once")

    # Stale feed records
    if "last_updated" in df.columns:
        dates = pd.to_datetime(df["last_updated"], errors="coerce")
        cutoff = pd.Timestamp("2026-08-01")
        stale_mask = dates.notna() & (dates < cutoff)
        for _, row in df[stale_mask].iterrows():
            add_issue(row, "Stale Listing", "MEDIUM", "last_updated",
                      "Listing has not been updated recently")

    # Large price changes relative to product median
    if "product_id" in df.columns and "selling_price" in df.columns:
        tmp = df.copy()
        tmp["selling_price"] = pd.to_numeric(tmp["selling_price"], errors="coerce")
        medians = tmp.groupby("product_id")["selling_price"].transform("median")
        tmp["_median"] = medians
        mask = (
            tmp["selling_price"].notna()
            & tmp["_median"].notna()
            & (tmp["_median"] > 0)
            & ((tmp["selling_price"] / tmp["_median"] > 3)
               | (tmp["selling_price"] / tmp["_median"] < 1/3))
        )
        for idx, row in tmp[mask].iterrows():
            add_issue(df.loc[idx], "Price Anomaly", "HIGH", "selling_price",
                      "Selling price is unusually far from the product median")

    return pd.DataFrame(issues)
