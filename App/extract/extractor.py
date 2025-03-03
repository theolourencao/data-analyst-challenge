
import duckdb
import os
import re
import gzip
import pandas as pd
from tqdm import tqdm
import gc

def descompactar_para_parquet(pasta_arquivos, parquet_destino, bloco_linhas=500_000, is_test=False):
    """Lê arquivos .gz parcialmente e escreve em Parquet particionado por data e separado por ano."""
    con = duckdb.connect(database=':memory:')
    
    arquivos_gz = [f for f in os.listdir(pasta_arquivos) if f.endswith('.gz')]
    print(f"Arquivos encontrados: {arquivos_gz}")

    # Se for teste, processa apenas o primeiro arquivo `.gz`
    if is_test and arquivos_gz:
        arquivos_gz = arquivos_gz[:1]
    
    if not arquivos_gz:
        print("Nenhum arquivo .gz encontrado.")
        return

    for arquivo in tqdm(arquivos_gz, desc="Processando arquivos"):
        caminho_arquivo = os.path.join(pasta_arquivos, arquivo)

        # Extrai o ano do nome do arquivo usando regex
        match = re.search(r'(\d{4})', arquivo)
        ano = match.group(1) if match else 'unknown'
        print(f"Processando o ano: {ano}")

        # Define o caminho com a subpasta do ano
        nome_base = arquivo.replace('.gz', '.parquet')
        destino_ano = parquet_destino if is_test else os.path.join(parquet_destino, ano)
        os.makedirs(destino_ano, exist_ok=True)
        print(f"Destino para Parquet: {destino_ano}")

        # Caminho para o arquivo Parquet
        caminho_parquet = os.path.join(destino_ano, nome_base)
        print(f"Salvando Parquet em: {caminho_parquet}")

        linhas_buffer = []
        pbar = tqdm(desc=f"Processando {arquivo}", unit=" linhas", dynamic_ncols=True)

        # Lê o arquivo gzip linha por linha
        with gzip.open(caminho_arquivo, 'rt', encoding='utf-8') as f_in:
            for linha in f_in:
                linhas_buffer.append(linha.strip().split(','))
                pbar.update(1)

                if len(linhas_buffer) >= bloco_linhas:
                    num_colunas = len(linhas_buffer[0])
                    colunas = [f'column{i+1}' for i in range(num_colunas)]

                    df = pd.DataFrame(linhas_buffer, columns=colunas)
                    con.execute("CREATE OR REPLACE TABLE temp AS SELECT * FROM df")
                    con.execute(f"COPY temp TO '{caminho_parquet}' (FORMAT 'parquet', PARTITION_BY (column2), OVERWRITE_OR_IGNORE)")
                    linhas_buffer = []

                    # Se está no modo de teste, sair após processar o primeiro bloco
                    if is_test:
                        break

        if not is_test and linhas_buffer:
            num_colunas = len(linhas_buffer[0])
            colunas = [f'column{i+1}' for i in range(num_colunas)]

            df = pd.DataFrame(linhas_buffer, columns=colunas)
            con.execute("CREATE OR REPLACE TABLE temp AS SELECT * FROM df")
            con.execute(f"COPY temp TO '{caminho_parquet}' (FORMAT 'parquet', PARTITION_BY (column2), OVERWRITE_OR_IGNORE)")

        pbar.close()
        print(f"✅ Parquet salvo em: {caminho_parquet}")

        con.execute("DROP TABLE IF EXISTS temp")
        gc.collect()

        if is_test:
            break