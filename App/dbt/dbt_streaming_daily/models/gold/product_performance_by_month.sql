{{ config(
    materialized='table'
) }}

SELECT
    DATE_TRUNC('month', date) AS day,
    product,
    macro_store,
    store,
    first_payment_date,
    country_code,
    country_name,
    region,
    subregion,
    genre_id,
    genre_name,
    product_aging,
    is_stream,
    case 
        when product_aging = 0 then '0 - early'
        when product_aging = 1 then '1 - new'
        when product_aging between 2 and 5 then '2 - existing'
        else '3 - old' end as product_age_group,
    SUM(quantity) AS total_streams,
    SUM(revenue) AS total_revenue,
    SUM(is_download) AS total_downloads,
    COUNT(DISTINCT product) AS total_products

FROM 
    {{ ref('cleaned_streaming_data') }}
GROUP BY 
    all
ORDER BY 
    day, country_code, store
