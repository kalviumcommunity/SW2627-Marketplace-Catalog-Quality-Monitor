# Marketplace Catalog Quality Monitor

## Problem

A multi-vendor marketplace receives product listings, pricing updates, and
inventory feeds from thousands of sellers daily, but inconsistent catalog
data can reach customers without being detected first.

## Solution

This project is a basic data-quality validation application. It reads a seller
catalog feed, checks it against predefined validation rules, stores the
results in SQLite, and displays the results through a Streamlit dashboard.

## Validation checks

- Missing required fields
- Invalid or non-positive selling prices
- MRP lower than selling price
- Negative inventory
- Invalid categories
- Duplicate seller-product submissions
- Stale listings
- Unusual price anomalies

## Technology

- Python
- Pandas
- SQLite / SQL
- Streamlit
- GitHub Actions

## Project structure

```text
seller_catalog_feed.csv    Sample seller feed
validator.py               Validation rules
pipeline.py                Data processing and database pipeline
catalog_quality.db         SQLite output database
app.py                     Streamlit dashboard
queries.sql                Example SQL analysis
test_validator.py          Basic validation tests
DATA_DICTIONARY.md         Dataset documentation
requirements.txt           Python dependencies
.github/workflows/         GitHub Actions validation
```

## Run locally

```bash
pip install -r requirements.txt
python pipeline.py
streamlit run app.py
```

## Dataset

The included dataset is synthetic and was created for demonstration and
testing. It contains realistic marketplace fields and intentionally includes
data-quality problems so that the validation workflow can be demonstrated
without using private seller data.

## Scope

This is a functional prototype focused on the core validation workflow and a
simple operational dashboard.
