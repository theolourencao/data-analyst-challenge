from ..utils.db_connection import DuckDBConnection
from .config_reader import absolute_parquet_folder
import duckdb

def main():
    # Initialize the database connection
    db_conn = DuckDBConnection()
    db_conn.connect()

    # SQL query to create or replace a table from Parquet files with renamed columns
    query = f"""
        CREATE OR REPLACE TABLE streaming_data AS
        SELECT
            column1 AS store,
            column2 AS date,
            column3 AS product,
            column4 AS quantity,
            column5 AS is_stream,
            column6 AS is_download,
            column7 AS revenue,
            column8 AS currency,
            column9 AS country_code,
            column10 AS genre_id,
            column11 AS genre_name
        FROM parquet_scan('{absolute_parquet_folder}/**/*.parquet')
    """
    try:
        # Execute the query
        result = db_conn.execute_query(query)
        if result is not None:
            print(result)
    except duckdb.Error as e:
        print("Error occurred:", e)
    finally:
        # Ensure closing the connection
        db_conn.close()

if __name__ == '__main__':
    main()

