{{ config(
    materialized='table'
) }}

WITH month_total AS (
    SELECT 
        DATE_TRUNC('month', date) AS day,
        region,
        SUM(quantity) AS total_streams,
        SUM(revenue) AS total_revenue,
        SUM(is_download) AS total_downloads,
        COUNT(DISTINCT product) AS total_products
    FROM {{  'cleaned_streaming_data' }}
    GROUP BY DATE_TRUNC('month', date), region
),
year_windows AS (
    SELECT 
        day, 
        region, 
        total_streams, 
        total_revenue, 
        total_downloads, 
        total_products,
        SUM(total_streams) OVER (PARTITION BY region, YEAR(day)) AS year_streams,
        LAG(total_streams) OVER (PARTITION BY region ORDER BY day) AS last_month_streams,
        SUM(total_streams) OVER (
            PARTITION BY region, YEAR(day) 
            ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS year_to_date_streams
    FROM month_total
)
SELECT 
    yw.day,
    yw.region,
    yw.total_streams,
    yw.total_revenue,
    yw.total_downloads,
    yw.total_products,
    yw.year_streams,
    yw.last_month_streams,
    yw.year_to_date_streams,
    last_year.year_streams AS last_year_total_streams,
    last_year.year_to_date_streams AS last_year_to_date_streams,
    yw.total_streams / NULLIF(yw.year_streams, 0) AS year_share,
    (yw.year_to_date_streams - last_year.year_to_date_streams) / NULLIF(last_year.year_to_date_streams, 0) AS ytd_delta,
    (yw.year_streams - last_year.year_streams) / NULLIF(last_year.year_streams, 0) AS year_total_delta
FROM year_windows yw
LEFT JOIN year_windows last_year 
    ON yw.region = last_year.region 
    AND YEAR(yw.day) = YEAR(last_year.day) + 1
    AND MONTH(yw.day) = MONTH(last_year.day)
ORDER BY yw.region, yw.day
