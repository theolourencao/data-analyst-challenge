{{ config(
    materialized='table'
) }}

WITH avg_growth AS (
    SELECT 
        region,
        AVG((total_streams - last_month_streams) / NULLIF(last_month_streams, 0)) AS avg_monthly_growth
    FROM {{ ref('region_monthly_analysis') }}
    WHERE YEAR(day) IN (2022, 2023, 2024) AND NOT (YEAR(day) = 2024 AND MONTH(day) = 12)
    GROUP BY region
),
projection_2025 AS (
    SELECT 
        MAKE_DATE(2025, MONTH(yw.day), 1) AS day,
        yw.region,
        yw.total_streams * (1 + ag.avg_monthly_growth) AS projected_total_streams,
        yw.total_revenue * (1 + ag.avg_monthly_growth) AS projected_total_revenue,
        yw.total_downloads * (1 + ag.avg_monthly_growth) AS projected_total_downloads,
        yw.total_products 
    FROM {{ ref('region_monthly_analysis') }} yw
    JOIN avg_growth ag ON yw.region = ag.region
    WHERE YEAR(yw.day) = 2024
)
SELECT * FROM projection_2025
