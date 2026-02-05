# signal_generator.py

def generate_signals(df):

    df = df.copy()

    # ---------------- TREND BUY ----------------
    trend_buy = (
        (df['structure_HTF'] == 'BOS_BULLISH') &
        (df['structure'] == 'BOS_BULLISH') &
        (
            df['bullish_engulf'] |
            df['fvg_bullish'] |
            df['liquidity_sweep_low']
        )
    )

    # ---------------- REVERSAL BUY ----------------
    reversal_buy = (
        (df['structure_HTF'] == 'BOS_BULLISH') &
        (df['structure'] == 'CHoCH_BULLISH') &
        (
            df['liquidity_sweep_low'] |
            df['bullish_engulf']
        )
    )

    df['BUY_SIGNAL'] = trend_buy | reversal_buy

    # ---------------- TREND SELL ----------------
    trend_sell = (
        (df['structure_HTF'] == 'BOS_BEARISH') &
        (df['structure'] == 'BOS_BEARISH') &
        (
            df['bearish_engulf'] |
            df['fvg_bearish'] |
            df['liquidity_sweep_high']
        )
    )

    # ---------------- REVERSAL SELL ----------------
    reversal_sell = (
        (df['structure_HTF'] == 'BOS_BEARISH') &
        (df['structure'] == 'CHoCH_BEARISH') &
        (
            df['liquidity_sweep_high'] |
            df['bearish_engulf']
        )
    )

    df['SELL_SIGNAL'] = trend_sell | reversal_sell

    return df