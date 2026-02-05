#live_bot.py
import time
import MetaTrader5 as mt5

from core.feature_engine import *
from data.mt5_fetch_data import connect_mt5, fetch_data
from execution.trader import place_trade, get_open_positions
from config import *

SYMBOL = "XAUUSD"
BARS = 500  # smaller for live


def run_live():

    if not connect_mt5():
        return

    ltf = fetch_data(SYMBOL, LTF, LIVE_BARS)
    htf = fetch_data(SYMBOL, HTF, LIVE_BARS)

    ltf = build_features(ltf)
    htf = build_features(htf)

    ltf = build_smart_money(ltf, htf)
    ltf = build_signals(ltf)

    latest = ltf.iloc[-1]

    if not get_open_positions(SYMBOL):
        place_trade(SYMBOL, latest)

    mt5.shutdown()


print("🤖 LIVE BOT STARTED")

while True:
    run_live()
    time.sleep(90)

