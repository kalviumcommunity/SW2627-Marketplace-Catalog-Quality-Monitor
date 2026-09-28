# Supporting Evidence

This document supports the findings in [analysis_narrative.md](../analysis_narrative.md). The values below were produced by running `python pipeline.py` against the included synthetic feed.

## Finding 1: One in ten records needs correction

**Evidence:** The quality summary reports 12,120 records processed, 10,967 valid records, 1,153 invalid records, and a 90.5% quality score.

**Why it matters:** 1,153 records can carry a catalog error into publication. The quality score gives leadership a simple baseline for measuring improvement after each feed cycle.

**Business meaning:** The feed is mostly usable, but the remaining 9.5% is large enough to justify a gate before publication.

## Finding 2: Missing fields are the largest recurring problem

**Evidence:** The issue summary reports 566 `Missing Required Field` issues, more than any other issue type. The feed also contains 120 missing category values.

**Why it matters:** Missing identifiers and product details make records difficult to process, trace, or display correctly.

**Business meaning:** Controlled seller forms and row-level correction messages can prevent a large share of errors before they enter the marketplace.

## Finding 3: High-severity issues create direct customer risk

**Evidence:** There are 1,346 high-severity issues and 234 critical issues. The critical total includes 123 invalid prices and 111 negative inventory values.

**Why it matters:** A non-positive price or negative stock value can produce an incorrect offer or availability state. These errors should be stopped before publication rather than discovered afterward.

**Business meaning:** A quarantine rule for critical issues is the fastest customer-protection measure.

## Finding 4: Duplicate submissions and seller concentration are actionable

**Evidence:** The validator found 240 duplicate SKUs and 238 duplicate seller-product submissions. Seller S0111 has 36 issues across 16 products; S0091 has 31 issues across 10 products.

**Why it matters:** Duplicate offers can conflict, while seller concentration means targeted coaching can address more risk than a broad seller campaign.

**Business meaning:** Enforce a seller-product key and begin weekly reviews with the highest-issue sellers.

## Reproducibility

The evidence comes from the validator rules in `validator.py`, the sample feed in `seller_catalog_feed.csv`, and the summary queries in `queries.sql`. The dataset is synthetic, so these findings describe the prototype feed and should be rechecked against production history before financial or customer-impact claims are made.