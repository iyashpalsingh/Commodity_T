# signal_generator.py

def generate_signals(df):

    df = df.copy()

    df['BUY_SIGNAL'] = (
        df['structure_HTF'].isin(['BOS_BULLISH', 'CHoCH_BULLISH']) &
        (df['structure'] == 'CHoCH_BULLISH') &
        (df['liquidity_sweep_low']) &
        (df['bullish_engulf'] | df['fvg_bullish'])
    )

    df['SELL_SIGNAL'] = (
        df['structure_HTF'].isin(['BOS_BEARISH', 'CHoCH_BEARISH']) &
        (df['structure'] == 'CHoCH_BEARISH') &
        (df['liquidity_sweep_high']) &
        (df['bearish_engulf'] | df['fvg_bearish'])
    )

    return df
