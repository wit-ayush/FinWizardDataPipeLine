import pandas as pd
import numpy as np

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    # RSI (14)
    delta_price = df['close'].diff()
    gain = delta_price.where(delta_price > 0, 0)
    loss = -delta_price.where(delta_price < 0, 0)
    
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD (12, 26, 9)
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # ATR (14)
    df['previous_close'] = df['close'].shift(1)
    df['H-L'] = df['high'] - df['low']
    df['H-PC'] = abs(df['high'] - df['previous_close'])
    df['L-PC'] = abs(df['low'] - df['previous_close'])
    tr = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df['ATR'] = tr.rolling(window=14).mean()

    # Drop intermediate columns for ATR
    df.drop(columns=['previous_close', 'H-L', 'H-PC', 'L-PC'], inplace=True)

    # Bollinger Bands (20, 2)
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['std_20'] = df['close'].rolling(window=20).std()
    df['Bollinger_Upper'] = df['SMA_20'] + (df['std_20'] * 2)
    df['Bollinger_Lower'] = df['SMA_20'] - (df['std_20'] * 2)

    # 9 EMA, 21 EMA, 5 EMA
    df['EMA_9'] = df['close'].ewm(span=9, adjust=False).mean()
    df['EMA_21'] = df['close'].ewm(span=21, adjust=False).mean()
    df['EMA_5'] = df['close'].ewm(span=5, adjust=False).mean()

    # VWAP (Volume Weighted Average Price)
    df['cumulative_volume'] = df['volume'].cumsum()
    df['cumulative_vwap'] = (df['close'] * df['volume']).cumsum()
    df['VWAP'] = df['cumulative_vwap'] / df['cumulative_volume']

    # Drop cumulative columns
    df.drop(columns=['cumulative_volume', 'cumulative_vwap'], inplace=True)

    return df
