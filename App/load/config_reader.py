import os

# Define the path to include all Parquet files inside 'Parquets' directory
parquet_folder = './Data/Parquets'

# Debugging: print the absolute path to ensure correctness
absolute_parquet_folder = os.path.abspath(parquet_folder)
print("Looking for Parquet files in:", absolute_parquet_folder)
