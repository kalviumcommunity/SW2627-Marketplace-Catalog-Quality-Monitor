import sqlite3
from pathlib import Path
import pandas as pd
from validator import validate_catalog

BASE = Path(__file__).parent
RAW = BASE / "seller_catalog_feed.csv"
DB = BASE / "catalog_quality.db"

df = pd.read_csv(RAW)
issues = validate_catalog(df)

invalid_feed_ids = set(issues["feed_id"].dropna())
invalid_records = df[df["feed_id"].isin(invalid_feed_ids)].copy()
valid_records = df[~df["feed_id"].isin(invalid_feed_ids)].copy()

quality_score = 100 * len(valid_records) / max(len(df), 1)

summary = pd.DataFrame([{
    "total_records": len(df),
    "valid_records": len(valid_records),
    "invalid_records": len(invalid_records),
    "quality_score": quality_score
}])

conn = sqlite3.connect(DB)

tables = {
    "raw_catalog": df,
    "valid_catalog": valid_records,
    "invalid_catalog": invalid_records,
    "validation_issues": issues,
    "quality_summary": summary
}

for table_name, table_data in tables.items():
    table_data.to_sql(table_name, conn, if_exists="replace", index=False)

conn.close()

print("Marketplace Catalog Validation Complete")
print(f"Records processed : {len(df):,}")
print(f"Valid records     : {len(valid_records):,}")
print(f"Invalid records   : {len(invalid_records):,}")
print(f"Validation issues : {len(issues):,}")
print(f"Quality score     : {quality_score:.1f}%")
