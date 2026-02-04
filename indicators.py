# indicators.py
import pandas as pd
import numpy as np

# -------------------- MOVING AVERAGES --------------------

def add_moving_averages(df, periods=[20, 50, 200]):
    for p in periods:
        df[f"SMA_{p}"] = df['close'].rolling(p).mean()
        df[f"EMA_{p}"] = df['close'].ewm(span=p).mean()
    return df

# -------------------- RSI --------------------

def add_rsi(df, period=14):
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# -------------------- MACD --------------------

def add_macd(df):
    ema12 = df['close'].ewm(span=12).mean()
    ema26 = df['close'].ewm(span=26).mean()
    df['MACD'] = ema12 - ema26
    df['MACD_SIGNAL'] = df['MACD'].ewm(span=9).mean()
    df['MACD_HIST'] = df['MACD'] - df['MACD_SIGNAL']
    return df

# -------------------- ATR --------------------

def add_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = abs(df['high'] - df['close'].shift())
    low_close = abs(df['low'] - df['close'].shift())

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['ATR'] = tr.rolling(period).mean()
    return df