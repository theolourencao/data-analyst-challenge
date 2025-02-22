{{ config(
    materialized='table'
) }}

SELECT
    DATE_TRUNC('month', date) AS month,
    product,
    store,
    country_code,
    genre_id,
    SUM(quantity) AS total_quantity,
    SUM(revenue) AS total_revenue,
    SUM(is_stream) AS total_streams,
    SUM(is_download) AS total_downloads
FROM 
    {{ ref('cleaned_streaming_data') }}
GROUP BY 
    month, product, store, country_code, genre_id
ORDER BY 
    month, product, store
