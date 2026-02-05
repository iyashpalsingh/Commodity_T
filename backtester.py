# backtester.py

import pandas as pd


def backtest_strategy(df, rr=2.0, sl_atr_mult=1.0):

    df = df.copy()

    trades = []
    position = None

    for i in range(len(df)):

        if position is None:

            # ---------- BUY ----------
            if df.iloc[i]['BUY_SIGNAL']:

                entry = df.iloc[i]['close']
                atr = df.iloc[i]['ATR']

                sl = entry - atr * sl_atr_mult
                tp = entry + (entry - sl) * rr

                position = {
                    'type': 'BUY',
                    'entry': entry,
                    'sl': sl,
                    'tp': tp
                }

            # ---------- SELL ----------
            elif df.iloc[i]['SELL_SIGNAL']:

                entry = df.iloc[i]['close']
                atr = df.iloc[i]['ATR']

                sl = entry + atr * sl_atr_mult
                tp = entry - (sl - entry) * rr

                position = {
                    'type': 'SELL',
                    'entry': entry,
                    'sl': sl,
                    'tp': tp
                }

        else:
            high = df.iloc[i]['high']
            low = df.iloc[i]['low']

            if position['type'] == 'BUY':

                if low <= position['sl']:
                    trades.append(-1)
                    position = None

                elif high >= position['tp']:
                    trades.append(2)
                    position = None

            if position and position['type'] == 'SELL':

                if high >= position['sl']:
                    trades.append(-1)
                    position = None

                elif low <= position['tp']:
                    trades.append(2)
                    position = None

    # ---------------- STATS ----------------

    total = len(trades)
    wins = sum(1 for t in trades if t > 0)
    losses = sum(1 for t in trades if t < 0)

    win_rate = (wins / total) * 100 if total > 0 else 0
    profit_factor = abs(sum(t for t in trades if t > 0) /
                        sum(t for t in trades if t < 0)) if losses > 0 else 0

    return {
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "profit_factor": profit_factor
    }
