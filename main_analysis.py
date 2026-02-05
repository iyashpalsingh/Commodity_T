# main_analysis.py

from indicators import *
from market_structure import *
from structure_logic import *
from smart_money_logic import *
from draw_tools import *
from mt5_fetch_data import connect_mt5, fetch_data
from signal_generator import generate_signals
from backtester import backtest_strategy

import MetaTrader5 as mt5
import pandas as pd
import os

# ---------------- CONFIG ----------------

symbol = "XAUUSD"
bars = 2000

timeframes = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "H1": mt5.TIMEFRAME_H1
}

os.makedirs("enriched_data", exist_ok=True)

# ---------------- CONNECT MT5 ----------------

if not connect_mt5():
    raise RuntimeError("MT5 connection failed")

# =========================================================
# STEP 1 → FETCH + STRUCTURE BUILD
# =========================================================

for tf_name, tf_value in timeframes.items():

    print(f"\n📥 Fetching {symbol} | {tf_name}")

    df = fetch_data(symbol, tf_value, bars)

    if df is None or df.empty:
        print(f"⚠ Skipping {tf_name}")
        continue

    df = add_moving_averages(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_atr(df)

    df = detect_trend(df)
    df = support_resistance(df)

    df = detect_swings(df)
    df = detect_bos_choch(df)

    filename = f"enriched_data/{symbol}_{tf_name}_structure.csv"
    df.to_csv(filename, index=False)

    print(f"✅ Saved structure → {filename}")

# =========================================================
# STEP 2 → SMART MONEY ALIGNMENT
# =========================================================

print("\n🧠 Running Smart Money Alignment")

h1_path = f"enriched_data/{symbol}_H1_structure.csv"
m15_path = f"enriched_data/{symbol}_M15_structure.csv"

if not os.path.exists(h1_path) or not os.path.exists(m15_path):
    raise RuntimeError("Required structure files missing")

# Load datasets
h1_df = pd.read_csv(h1_path)
m15_structure_df = pd.read_csv(m15_path)

# Alignment
m15_smart_df = align_htf_structure(m15_structure_df, h1_df)

# Smart Money Features
m15_smart_df = detect_liquidity_sweep(m15_smart_df)
m15_smart_df = detect_engulfing(m15_smart_df)
m15_smart_df = detect_fvg(m15_smart_df)

# Debug Guard
if 'structure_HTF' not in m15_smart_df.columns:
    raise RuntimeError("HTF alignment failed")

smart_file = f"enriched_data/{symbol}_M15_smart_money.csv"
m15_smart_df.to_csv(smart_file, index=False)

print(f"✅ Smart Money dataset saved → {smart_file}")

# =========================================================
# STEP 3 → SIGNAL GENERATION
# =========================================================

m15_signal_df = generate_signals(m15_smart_df)

signal_file = f"enriched_data/{symbol}_M15_signals.csv"
m15_signal_df.to_csv(signal_file, index=False)

print(f"✅ Signals saved → {signal_file}")

# =========================================================
# STEP 4 → BACKTEST
# =========================================================

results = backtest_strategy(m15_signal_df)

print("\n📊 BACKTEST RESULTS")
for k, v in results.items():
    print(f"{k}: {v}")

# ---------------- SHUTDOWN ----------------

mt5.shutdown()
print("\n🔌 MT5 connection closed")