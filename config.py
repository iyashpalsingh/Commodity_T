import MetaTrader5 as mt5

# ---------- SYMBOL ----------
SYMBOL = "XAUUSD"

# ---------- TIMEFRAMES ----------
LTF = mt5.TIMEFRAME_M15  # Trading timeframe
HTF = mt5.TIMEFRAME_H1   # Higher timeframe

# ---------- DATA ----------
LIVE_BARS = 500
RESEARCH_BARS = 10000

# ---------- RISK ----------
LOT_SIZE = 0.01
RR_RATIO = 2.0