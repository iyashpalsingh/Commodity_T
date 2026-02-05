# structure_logic.py
import pandas as pd
import numpy as np

# -------------------- SWING POINTS --------------------

def detect_swings(df, lookback=3):
    df = df.copy()

    df['swing_high'] = (
        (df['high'] > df['high'].shift(1)) &
        (df['high'] > df['high'].shift(-1)) &
        (df['high'] > df['high'].shift(lookback)) &
        (df['high'] > df['high'].shift(-lookback))
    )

    df['swing_low'] = (
        (df['low'] < df['low'].shift(1)) &
        (df['low'] < df['low'].shift(-1)) &
        (df['low'] < df['low'].shift(lookback)) &
        (df['low'] < df['low'].shift(-lookback))
    )

    return df


# -------------------- BOS / CHoCH --------------------

def detect_bos_choch(df):
    df = df.copy()

    df['structure'] = "NONE"
    last_high = None
    last_low = None
    trend = None  # "bullish" or "bearish"

    for i in range(len(df)):
        if df.loc[df.index[i], 'swing_high']:
            last_high = df.loc[df.index[i], 'high']

        if df.loc[df.index[i], 'swing_low']:
            last_low = df.loc[df.index[i], 'low']

        close = df.loc[df.index[i], 'close']

        # -------- Bullish Structure --------
        if last_high and close > last_high:
            if trend == "bearish":
                df.loc[df.index[i], 'structure'] = "CHoCH_BULLISH"
            else:
                df.loc[df.index[i], 'structure'] = "BOS_BULLISH"
            trend = "bullish"

        # -------- Bearish Structure --------
        if last_low and close < last_low:
            if trend == "bullish":
                df.loc[df.index[i], 'structure'] = "CHoCH_BEARISH"
            else:
                df.loc[df.index[i], 'structure'] = "BOS_BEARISH"
            trend = "bearish"

    return df