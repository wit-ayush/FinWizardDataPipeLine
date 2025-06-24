import os
import pandas as pd

# Path to the directory containing Parquet files
DATA_DIR = '../data/BAJAJFINSV'  # Change if needed

# Load all Parquet files into a single DataFrame
parquet_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith('.parquet')]
df_list = [pd.read_parquet(file) for file in parquet_files]
df = pd.concat(df_list, ignore_index=True)

# Ensure datetime columns are parsed correctly
df['date'] = pd.to_datetime(df['date'])

# 1. Filter by specific date
result1 = df[df['date'] == '2024-06-10'].sort_values('time')
print("\n🔍 Query 1: Rows for 2024-06-10")
print(result1)

# 2. Top 5 by volume
result2 = df[['date', 'time', 'close', 'chg in percentage', 'volume']].sort_values(by='volume', ascending=False).head(5)
print("\n🔍 Query 2: Top 5 rows by volume")
print(result2)

# 3. Average Close & RSI between two dates
mask = (df['date'] >= '2024-06-01') & (df['date'] <= '2024-06-15')
result3 = df[mask].groupby('date')[['close', 'RSI']].mean().reset_index()
result3.rename(columns={'close': 'avg_close', 'RSI': 'avg_rsi'}, inplace=True)
print("\n🔍 Query 3: Average Close & RSI (2024-06-01 to 2024-06-15)")
print(result3)

# 4. Close price more than 5% above VWAP
result4 = df[df['close'] > df['VWAP'] * 1.05]
print("\n🔍 Query 4: Close > 1.05 * VWAP")
print(result4[['date', 'time', 'close', 'VWAP']])
