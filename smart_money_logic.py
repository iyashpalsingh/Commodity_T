#smart_money_logic.py
import pandas as pd

# -------------------- HTF → LTF ALIGNMENT --------------------

def align_htf_structure(ltf_df, htf_df):

    ltf_df = ltf_df.copy()
    htf_df = htf_df.copy()

    ltf_df['time'] = pd.to_datetime(ltf_df['time'])
    htf_df['time'] = pd.to_datetime(htf_df['time'])

    ltf_df = ltf_df.sort_values('time')
    htf_df = htf_df.sort_values('time')

    # ⭐ Rename HTF structure BEFORE merge
    htf_df = htf_df.rename(columns={'structure': 'structure_HTF'})

    merged = pd.merge_asof(
        ltf_df,
        htf_df[['time', 'structure_HTF']],
        on='time',
        direction='backward'
    )

    # Fill missing HTF values
    merged['structure_HTF'] = merged['structure_HTF'].ffill()
    merged['structure_HTF'] = merged['structure_HTF'].bfill()

    return merged


# -------------------- LIQUIDITY SWEEP --------------------

def detect_liquidity_sweep(df):

    df = df.copy()
    df['liquidity_sweep_high'] = False
    df['liquidity_sweep_low'] = False

    last_swing_high = None
    last_swing_low = None

    for i in range(len(df)):

        if df.loc[df.index[i], 'swing_high']:
            last_swing_high = df.loc[df.index[i], 'high']

        if df.loc[df.index[i], 'swing_low']:
            last_swing_low = df.loc[df.index[i], 'low']

        if last_swing_high:
            if (
                df.loc[df.index[i], 'high'] > last_swing_high and
                df.loc[df.index[i], 'close'] < last_swing_high
            ):
                df.loc[df.index[i], 'liquidity_sweep_high'] = True

        if last_swing_low:
            if (
                df.loc[df.index[i], 'low'] < last_swing_low and
                df.loc[df.index[i], 'close'] > last_swing_low
            ):
                df.loc[df.index[i], 'liquidity_sweep_low'] = True

    return df

# -------------------- ENGULFING --------------------

def detect_engulfing(df):

    df = df.copy()

    df['bullish_engulf'] = (
        (df['close'] > df['open']) &
        (df['close'].shift(1) < df['open'].shift(1)) &
        (df['close'] > df['open'].shift(1)) &
        (df['open'] < df['close'].shift(1))
    )

    df['bearish_engulf'] = (
        (df['close'] < df['open']) &
        (df['close'].shift(1) > df['open'].shift(1)) &
        (df['open'] > df['close'].shift(1)) &
        (df['close'] < df['open'].shift(1))
    )

    return df

# -------------------- FVG / IMBALANCE --------------------

def detect_fvg(df):

    df = df.copy()
    df['fvg_bullish'] = False
    df['fvg_bearish'] = False

    for i in range(2, len(df)):

        # Bullish imbalance
        if df['low'].iloc[i] > df['high'].iloc[i-2]:
            df.loc[df.index[i], 'fvg_bullish'] = True

        # Bearish imbalance
        if df['high'].iloc[i] < df['low'].iloc[i-2]:
            df.loc[df.index[i], 'fvg_bearish'] = True

    return df
