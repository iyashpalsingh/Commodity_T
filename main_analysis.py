# main_analysis.py
from indicators import *
from market_structure import *
from draw_tools import *
from mt5_fetch_data import connect_mt5, fetch_data

import MetaTrader5 as mt5
import os

# -------------------- CONFIG --------------------

symbol = "XAUUSD"
bars = 2000
timeframes = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "H1": mt5.TIMEFRAME_H1
}

output_dir = "enriched_data"
os.makedirs(output_dir, exist_ok=True)

# -------------------- MT5 CONNECT --------------------

if not connect_mt5():
    raise RuntimeError("MT5 connection failed")

# -------------------- MULTI-TF LOOP --------------------

for tf_name, tf_value in timeframes.items():
    print(f"\n📥 Processing {symbol} | {tf_name}")

    df = fetch_data(symbol, tf_value, bars)

    if df is None or df.empty:
        print(f"⚠️ Skipping {tf_name} (no data)")
        continue

    # -------- Indicators --------
    df = add_moving_averages(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_atr(df)

    # -------- Market Structure --------
    df = detect_trend(df)
    df = support_resistance(df)

    # -------- Save --------
    filename = f"{output_dir}/{symbol}_{tf_name}_enriched.csv"
    df.to_csv(filename, index=False)

    print(f"✅ Saved → {filename}")

# -------------------- SHUTDOWN --------------------

mt5.shutdown()
print("\n🔌 MT5 connection closed")