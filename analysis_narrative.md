# Marketplace Catalog Quality: Executive Narrative

## Context

Marketplace customers rely on accurate prices, stock levels, categories, and product details. When a seller feed contains errors, a product can be shown with the wrong price, appear available when it is not, or fail to appear in the right category. These problems create customer frustration and manual work for catalog operations. This analysis asks whether the current seller feed is ready for publication and which operational changes will reduce the greatest risk first.

## Data Summary

We examined the synthetic seller catalog feed included with this project. It contains 12,120 records from 120 sellers and 4,550 products, covering updates dated from December 15, 2025 through September 10, 2026. Each record was checked for required fields, price and inventory validity, approved categories, duplicate submissions, stale updates, and unusually large differences from the typical price for that product. The validation results contain 1,801 individual issues and are stored in the project database for follow-up.

## Key Findings

- 10,967 records passed all checks and 1,153 records failed at least one check. The feed quality score is 90.5%, so roughly one record in ten needs attention before publication.
- Missing required fields are the largest issue, with 566 occurrences. A missing identifier or customer-facing field weakens traceability and can block downstream processing.
- High-severity problems account for 1,346 of the 1,801 issues. The most urgent individual risks are 123 invalid prices and 111 negative inventory values, which can directly affect what customers are charged or whether an item appears available.
- Duplicate submissions are also material: 240 duplicate SKUs and 238 repeated seller-product submissions were found. These duplicates can create conflicting offers and make it unclear which seller update should be trusted.
- Problems are concentrated enough to support seller-level follow-up. Seller S0111 has the highest issue count with 36 issues across 16 products, followed by S0091 with 31 issues across 10 products.

## Anomaly Investigation

The pattern is consistent with feed controls being weaker than the validation rules. The feed contains 120 missing categories plus 80 visibly inconsistent category values such as "Unknown," "Electonic," "Misc," "Homee," and "Fashon." This suggests that free-text seller input and incomplete pre-submission checks are allowing preventable errors into the batch. Duplicate records point to a second control gap: the system accepts repeated seller-product submissions without first deciding whether the record is a correction or an additional offer. These findings do not prove customer impact by themselves, but they identify the exact points where operational controls can prevent it.

## Recommendations

- **Quarantine critical price and inventory errors before publication.** Catalog Operations and Engineering should block the 234 critical issues, notify the seller with the affected field, and require correction. Implement the workflow within two weeks; the immediate outcome is that invalid prices and negative stock cannot reach customers.
- **Make required fields and categories controlled inputs.** Seller Operations should make the 566 required-field failures and invalid category values blocking errors, use the approved six-category list, and return row-level correction messages. Ship the feed checks within 30 days and target a 75% reduction in these errors in the next feed cycle.
- **Prevent duplicates and manage seller quality.** Engineering should enforce a seller-product submission key and retain a clear correction path, while Seller Operations should review a weekly scorecard beginning within 30 days. Start with S0111 and the other highest-issue sellers; target a 50% reduction in duplicate issues within 60 days.

The recommended sequence protects customers first, removes common data-entry causes, and then creates accountability with sellers. Together, these actions should raise the 90.5% quality score while making the remaining exceptions faster to resolve.