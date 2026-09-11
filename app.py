import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import tempfile
import sys

BASE = Path(__file__).parent
DB = BASE / "catalog_quality.db"

st.set_page_config(
    page_title="Marketplace Catalog Quality Monitor",
    page_icon="🔎",
    layout="wide"
)

st.title("Marketplace Catalog Quality Monitor")
st.write("A simple validation system for product, pricing and inventory feeds.")

@st.cache_data
def load_database():
    conn = sqlite3.connect(DB)
    issues = pd.read_sql("SELECT * FROM validation_issues", conn)
    summary = pd.read_sql("SELECT * FROM quality_summary", conn)
    conn.close()
    return issues, summary

issues, summary = load_database()

st.sidebar.header("Filters")

severity_options = sorted(issues["severity"].dropna().unique())
type_options = sorted(issues["issue_type"].dropna().unique())

selected_severity = st.sidebar.multiselect(
    "Severity",
    severity_options,
    default=severity_options
)

selected_types = st.sidebar.multiselect(
    "Issue type",
    type_options,
    default=type_options
)

seller_search = st.sidebar.text_input("Seller ID")

filtered = issues[
    issues["severity"].isin(selected_severity)
    & issues["issue_type"].isin(selected_types)
].copy()

if seller_search:
    filtered = filtered[
        filtered["seller_id"].fillna("").astype(str).str.contains(
            seller_search, case=False, na=False
        )
    ]

total_records = int(summary.iloc[0]["total_records"])
valid_records = int(summary.iloc[0]["valid_records"])
invalid_records = int(summary.iloc[0]["invalid_records"])
quality_score = float(summary.iloc[0]["quality_score"])
critical_count = int((issues["severity"] == "CRITICAL").sum())

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Records", f"{total_records:,}")
c2.metric("Valid", f"{valid_records:,}")
c3.metric("Invalid", f"{invalid_records:,}")
c4.metric("Quality Score", f"{quality_score:.1f}%")
c5.metric("Critical Issues", f"{critical_count:,}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Issues by Type")
    st.bar_chart(
        issues["issue_type"].value_counts().rename("Issues")
    )

with col2:
    st.subheader("Issues by Severity")
    st.bar_chart(
        issues["severity"].value_counts().rename("Issues")
    )

st.subheader("Most Problematic Sellers")
seller_table = (
    issues.groupby("seller_id")
    .agg(
        issues=("issue_type", "size"),
        affected_products=("product_id", "nunique")
    )
    .sort_values("issues", ascending=False)
    .head(10)
)
st.dataframe(seller_table, use_container_width=True)

st.subheader("Validation Issues")
st.caption(f"{len(filtered):,} issues match the selected filters.")

display_columns = [
    "feed_id", "seller_id", "product_id", "sku",
    "issue_type", "severity", "field", "message"
]
st.dataframe(
    filtered[display_columns],
    use_container_width=True,
    height=400
)

st.download_button(
    "Download Validation Report",
    filtered.to_csv(index=False),
    file_name="validation_report.csv",
    mime="text/csv"
)

st.divider()
st.subheader("About")
st.write(
    "The application checks seller feeds for missing fields, invalid prices, "
    "inventory errors, category errors, duplicate submissions, stale listings "
    "and unusual price changes."
)
