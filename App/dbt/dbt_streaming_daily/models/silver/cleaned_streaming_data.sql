{{ config(
    materialized='table'
) }}

with cleansing_data as
(SELECT
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
    CAST(is_download AS BOOLEAN) AS is_download,
    case when store like 'youtube%' then 'youtube'
        when store like 'facebook%' then 'facebook'
        when store like 'spotify%%' then 'spotify'
        when store like 'tiktok%' then 'tiktok'
        when store like 'amazon%' then 'amazon' end macro_store,
    date_trunc('month',min(date) over (partition by product order by date ASC )) first_payment_date
FROM 
    {{ref('streaming_data_view')}}),
pa as
(select *, datediff('month',first_payment_date,date_Trunc('month',date)) product_aging
from cleansing_data cd)
SELECT * from pa