from ..utils.db_connection import DuckDBConnection
import pandas as pd

# Função para exportar os dados para um arquivo CSV (que pode ser aberto no Excel)
def export_to_csv(dataframe, filename):
    # Criando conexão com DuckDB
    db_conn = DuckDBConnection()
    db_conn.connect()

    # Executando query e convertendo para DataFrame do Pandas
    df = db_conn.execute_query(f"SELECT * FROM {dataframe}")

    # Fechando conexão
    db_conn.close()

    # Salvando CSV com UTF-8-SIG para evitar problemas no Excel
    df.to_csv(filename, index=False, encoding="utf-8-sig", decimal=",")

    print(f"✅ Data exported to {filename}")

# Chamando a função para exportar os dados
export_to_csv('region_monthly_analysis', 'Data/CSVs/region_monthly_analysis.csv')
