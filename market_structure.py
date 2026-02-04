# market_structure.py
import numpy as np

# -------------------- TREND DETECTION --------------------

def detect_trend(df):
    df['trend'] = np.where(
        df['close'] > df['EMA_50'], 1,
        np.where(df['close'] < df['EMA_50'], -1, 0)
    )
    return df

# -------------------- SUPPORT & RESISTANCE --------------------

def support_resistance(df, window=20):
    df['support'] = df['low'].rolling(window).min()
    df['resistance'] = df['high'].rolling(window).max()
    return df

# -------------------- FIBONACCI LEVELS --------------------

def fibonacci_levels(df):
    high = df['high'].max()
    low = df['low'].min()

    diff = high - low
    levels = {
        "fib_0": high,
        "fib_23.6": high - 0.236 * diff,
        "fib_38.2": high - 0.382 * diff,
        "fib_50": high - 0.5 * diff,
        "fib_61.8": high - 0.618 * diff,
        "fib_100": low
    }
    return levels