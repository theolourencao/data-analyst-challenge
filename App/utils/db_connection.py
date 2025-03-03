import os
import duckdb

class DuckDBConnection:
    def __init__(self, database_path=None):
        if database_path is None:
            # Use caminho relativo em relação ao diretório de execução
            self.database_path = os.path.join('App', 'dbt', 'my_database.db')
        else:
            self.database_path = database_path
        self.connection = None

    def connect(self):
        """Establish a connection to the DuckDB database."""
        try:
            abs_path = os.path.abspath(self.database_path)
            print(f"Tentando conectar a {abs_path}")
            self.connection = duckdb.connect(database=abs_path)
            print(f"Connected to database at {abs_path}")
        except duckdb.Error as e:
            print(f"Error connecting to database: {e}")
        
    def close(self):
        """Close the current database connection."""
        if self.connection:
            try:
                self.connection.close()
                print("Connection closed successfully.")
            except duckdb.Error as e:
                print(f"Error closing connection: {e}")

    def execute_query(self, query):
        """Execute a given SQL query."""
        if self.connection:
            try:
                return self.connection.execute(query).fetchdf()
            except duckdb.Error as e:
                print(f"Error executing query: {e}")
                return None

if __name__ == '__main__':
    db_conn = DuckDBConnection()
    db_conn.connect()
    db_conn.close()
