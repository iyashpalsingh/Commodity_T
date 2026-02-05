#research_pipeline.py
from core.feature_engine import *
from data.mt5_fetch_data import connect_mt5, fetch_data
from research.backtester import backtest_strategy
import MetaTrader5 as mt5
import pandas as pd
from config import *


def run_research(symbol="XAUUSD", bars=10000):

    connect_mt5()

    # -------- Fetch --------
    ltf = fetch_data(SYMBOL, LTF, RESEARCH_BARS)
    htf = fetch_data(SYMBOL, HTF, RESEARCH_BARS)

    # -------- Features --------
    ltf = build_features(ltf)
    htf = build_features(htf)

    # -------- Smart Money --------
    ltf = build_smart_money(ltf, htf)

    # -------- Signals --------
    ltf = build_signals(ltf)

    # -------- Backtest --------
    results = backtest_strategy(ltf)

    print(results)

    mt5.shutdown()
    
if __name__ == "__main__":
    run_research()