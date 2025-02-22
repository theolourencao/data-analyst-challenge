{{ config(
    materialized='view'
) }}

SELECT * FROM streaming_data