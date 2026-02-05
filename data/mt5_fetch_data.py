#mt5_fetch_data.py
from dotenv import load_dotenv
import os
import MetaTrader5 as mt5
import pandas as pd

# 👇 FORCE LOAD THE .env FILE WITH FULL PATH
load_dotenv()

LOGIN = int(os.getenv("MT5_LOGIN"))
PASSWORD = os.getenv("MT5_PASSWORD")
SERVER = os.getenv("MT5_SERVER")

# -------------------- CONNECT FUNCTION --------------------

def connect_mt5():
    print("⏳ Initializing MT5...")

    if not mt5.initialize(login=LOGIN, password=PASSWORD, server=SERVER):
        print("❌ MT5 initialize() failed")
        print("Error code:", mt5.last_error())
        return False

    print("✅ Connected to MT5 successfully")
    return True

# -------------------- FETCH DATA FUNCTION --------------------

def fetch_data(symbol, timeframe, bars):
    if not mt5.symbol_select(symbol, True):
        print(f"❌ Failed to select symbol {symbol}")
        return None

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)

    if rates is None:
        print(f"❌ No data received for {symbol} | TF={timeframe}")
        return None

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    return df

# -------------------- MAIN --------------------

# if __name__ == "__main__":
#     if connect_mt5():

#         symbol = "XAUUSD"
#         bars = 2000

#         # 🔁 MULTIPLE TIMEFRAMES
#         timeframes = {
#             "M15": mt5.TIMEFRAME_M1,
#             "H1": mt5.TIMEFRAME_M5,
#             "H4": mt5.TIMEFRAME_M15,
#             "D1": mt5.TIMEFRAME_H1
#         }

#         for tf_name, tf_value in timeframes.items():
#             print(f"\n📥 Fetching {symbol} | {tf_name}")

#             data = fetch_data(symbol, tf_value, bars)

#             if data is not None:
#                 print(data.head())

#                 filename = f"{symbol}_{tf_name}.csv"
#                 data.to_csv(filename, index=False)
#                 print(f"📁 Saved → {filename}")

#         mt5.shutdown()
#         print("\n🔌 MT5 connection closed")
        