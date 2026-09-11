-- Overall quality
SELECT
    total_records,
    valid_records,
    invalid_records,
    quality_score
FROM quality_summary;

-- Most common issues
SELECT issue_type, COUNT(*) AS issue_count
FROM validation_issues
GROUP BY issue_type
ORDER BY issue_count DESC;

-- Seller quality
SELECT
    seller_id,
    COUNT(*) AS issue_count,
    COUNT(DISTINCT product_id) AS affected_products
FROM validation_issues
GROUP BY seller_id
ORDER BY issue_count DESC;

-- Critical issues
SELECT *
FROM validation_issues
WHERE severity = 'CRITICAL'
ORDER BY seller_id;
