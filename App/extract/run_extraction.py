import os
from dotenv import load_dotenv
from extractor import descompactar_para_parquet
import multiprocessing

# Caminho dos arquivos
pasta_arquivos = os.getenv('LOCAL_GZIP_FILES_PATH')

# Listar arquivos para debug
if pasta_arquivos:
    print(f"Caminho dos arquivos: {pasta_arquivos}")
    print("Arquivos no diretório:")
    print(os.listdir(pasta_arquivos))
else:
    print("Variável de ambiente LOCAL_GZIP_FILES_PATH não definida.")


# Carrega as variáveis do arquivo .env
load_dotenv()

def rodar_em_segundo_plano(is_test=False):
    pasta_arquivos = os.getenv('LOCAL_GZIP_FILES_PATH')
    parquet_destino = r'.\Data\Parquets'
    
    processo = multiprocessing.Process(target=descompactar_para_parquet, args=(pasta_arquivos, parquet_destino, 500_000, is_test))
    processo.start()
    print(f"🚀 Processo iniciado em segundo plano (PID: {processo.pid})")

if __name__ == '__main__':
    IS_TEST = False  # Muda para False para rodar completo
    rodar_em_segundo_plano(IS_TEST)

