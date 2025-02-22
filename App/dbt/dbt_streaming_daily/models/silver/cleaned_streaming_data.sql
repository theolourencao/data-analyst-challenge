{{ config(
    materialized='table'
) }}

SELECT
    CAST(store AS STRING) AS store,
    CAST(product AS STRING) AS product,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(revenue AS DOUBLE) AS revenue,
    CAST(currency AS STRING) AS currency,
    CAST(country_code AS STRING) AS country_code,
    genre_id,
    genre_name,
    date,
    CAST(is_stream AS BOOLEAN) AS is_stream,
    CAST(is_download AS BOOLEAN) AS is_download
FROM 
    {{ ref('streaming_data_view') }}