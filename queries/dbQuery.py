
import duckdb
import os

# Path to the directory where all Parquet files are stored
DATA_DIR = '../data/BAJAJFINSV'  # Change this to your index/instrument folder

# Initialize DuckDB in-memory database
con = duckdb.connect(database=':memory:')

# Register all parquet files in the given directory
parquet_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith('.parquet')]
parquet_glob = os.path.join(DATA_DIR, '*.parquet')

# Load all parquet files into a DuckDB virtual table
con.execute(f"""
    CREATE OR REPLACE TABLE stock_data AS
    SELECT * FROM read_parquet('{parquet_glob}')
""")

# Sample queries you can run
# Example 1: Filter by a specific date and select price columns
query1 = '''
SELECT *
FROM stock_data
WHERE date = '2024-06-10'
ORDER BY time
'''

# Example 2: Find top 5 time points with highest volume
query2 = '''
SELECT date, time, close, "chg in percentage", volume
FROM stock_data
ORDER BY volume DESC
LIMIT 5
'''

# Example 3: Find average close and RSI for a given date range
query3 = '''
SELECT date, AVG(close) AS avg_close, AVG(RSI) AS avg_rsi
FROM stock_data
WHERE date BETWEEN '2024-06-01' AND '2024-06-15'
GROUP BY date
ORDER BY date
'''

query4 = '''
SELECT date, time, close, VWAP
FROM stock_data
WHERE close > VWAP * 1.05
ORDER BY date, time
'''

# Execute and print results for demonstration
log_file_path = "query_results.log"
with open(log_file_path, "w", encoding="utf-8") as log_file:
    for i, q in enumerate([query1, query2, query3, query4], 1):
        result = con.execute(q).fetchdf()
        log_file.write(f"\n🔍 Query {i} Results:\n")
        log_file.write(result.to_string(index=False))  # Pretty format without index
        log_file.write("\n" + "="*60 + "\n")
