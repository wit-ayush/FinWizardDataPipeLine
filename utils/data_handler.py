import os
import pandas as pd
import requests
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from utils.kite_api import fetch_historical_data
from utils.indicators import calculate_indicators
from config.constants import *
from threading import Lock

write_lock = Lock()

def fetch_data_for_period(index_name, token, start_date, end_date, session):
    # Define the directory where data will be stored
    ticker_dir = BASE_PATH + index_name + '/'
    os.makedirs(ticker_dir, exist_ok=True)

    # Define the filename for the current period
    file_name = f"{start_date.strftime('%d-%m-%Y')}_to_{end_date.strftime('%d-%m-%Y')}.parquet"
    output_file = ticker_dir + file_name

    if os.path.exists(output_file):
        print(f"✅ File for period {start_date.date()} to {end_date.date()} already exists. Skipping...")
        return

    # Fetch data for the period
    print(f"📥 Fetching data for {start_date.date()} to {end_date.date()}...")

    candles = fetch_historical_data(token, USER_ID, start_date, end_date, session=session)

    if not candles:
        print(f"⚠️ No data for {start_date.date()} to {end_date.date()}. Skipping...")
        return

    # Process the fetched candles data into DataFrame
    df = pd.DataFrame(candles, columns=["datetime", "open", "high", "low", "close", "volume", "oi"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["date"] = df["datetime"].dt.strftime('%Y-%m-%d')
    df["time"] = df["datetime"].dt.strftime('%H:%M:%S')
    df["chg in price"] = df["close"].diff().round(2)
    df["chg in percentage"] = df["close"].pct_change().multiply(100).round(2)

    # Calculate technical indicators
    df = calculate_indicators(df)

    # Finalize the data to be saved
    final_df = df[[
        "date", "time", "open", "high", "low", "close",
        "chg in price", "chg in percentage", "RSI", "MACD", "Signal", "ATR",
        "Bollinger_Upper", "Bollinger_Lower", "EMA_9", "EMA_21", "EMA_5", "VWAP"
    ]]

    # Save data for the period into a Parquet file
    # Fetch data
    with write_lock:
        print(f"💾 Saving data for period {len(final_df)} to {end_date.date()} to {output_file}...")
        final_df.to_parquet(output_file, index=False)
    print(f"✅ Saved data for period {start_date.date()} to {end_date.date()} to {output_file}")


def update_index_data(index_name: str, token: int, session=None):
    # Define the directory where data will be stored
    ticker_dir = os.path.join(BASE_PATH, index_name)
    os.makedirs(ticker_dir, exist_ok=True)  # Create ticker directory if it doesn't exist

    print(f"\n🔄 Updating: {index_name} (Token: {token})")

    # Check the latest date from existing files in the ticker directory
    existing_files = [f for f in os.listdir(ticker_dir) if f.endswith('.parquet')]
    
    if existing_files:
        # Read the most recent file to determine the last date
        existing_files.sort()  # Sort to find the most recent file
        last_file = existing_files[-1]
        last_date = datetime.strptime(last_file.split('.')[0], '%d-%m-%Y')
        start_date = last_date + timedelta(days=1)  # Start from the next day after the latest file
        print(f"📂 Found {len(existing_files)} existing files. Last date: {last_date.date()}")
    else:
        start_date = START_DATE_DEFAULT  # Default start date if no existing files

    if start_date.date() > END_DATE_MASTER.date():
        print("✅ Already up-to-date.")
        return

    session = session or requests.Session()
    current = start_date

    # Use a ThreadPoolExecutor to fetch data concurrently
    with ThreadPoolExecutor() as executor:
        while current <= END_DATE_MASTER:
            # Define the chunk (let's say fetch data for a month or a week at a time)
            chunk_end = min(current + timedelta(days=30), END_DATE_MASTER)

            # Fetch the data for this period asynchronously
            executor.submit(fetch_data_for_period, index_name, token, current, chunk_end, session)

            # Move to the next period
            current = chunk_end + timedelta(days=1)
