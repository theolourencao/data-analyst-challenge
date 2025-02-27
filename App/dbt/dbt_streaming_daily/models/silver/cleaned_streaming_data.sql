{{ config(
    materialized='table'
) }}

WITH cleansing_data AS (
    SELECT
        CAST(store AS STRING) AS store,
        CAST(product AS STRING) AS product,
        CAST(quantity AS INTEGER) AS quantity,
        CAST(revenue AS DOUBLE) AS revenue,
        CAST(sdv.currency AS STRING) AS currency,
        CAST(country_code AS STRING) AS country_code,
        c.name AS country_name,   
        c.region,
        c.subregion,
        genre_id,
        genre_name,
        date,
        CAST(is_stream AS BOOLEAN) AS is_stream,
        CAST(is_download AS BOOLEAN) AS is_download,
        CASE 
            WHEN store LIKE 'youtube%' THEN 'youtube'
            WHEN store LIKE 'facebook%' THEN 'facebook'
            WHEN store LIKE 'spotify%%' THEN 'spotify'
            WHEN store LIKE 'tiktok%' THEN 'tiktok'
            WHEN store LIKE 'amazon%' THEN 'amazon' 
        END AS macro_store,
        DATE_TRUNC('month', MIN(date) OVER (PARTITION BY product ORDER BY date ASC)) AS first_payment_date
    FROM {{ ref('streaming_data_view') }} sdv
    LEFT JOIN {{ ref('countries') }} c 
        ON country_code = c.iso2
),
pa AS (
    SELECT *, 
           DATEDIFF('month', first_payment_date, DATE_TRUNC('month', date)) AS product_aging
    FROM cleansing_data
)
SELECT * FROM pa
