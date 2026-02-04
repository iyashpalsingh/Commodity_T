# market_depth.py
import MetaTrader5 as mt5
import pandas as pd

def get_market_depth(symbol):
    depth = mt5.market_book_get(symbol)

    if depth is None:
        print("❌ No market depth data")
        return None

    df = pd.DataFrame(depth)
    return df

def analyze_order_flow(df):
    buy_volume = df[df['type'] == mt5.BOOK_TYPE_BUY]['volume'].sum()
    sell_volume = df[df['type'] == mt5.BOOK_TYPE_SELL]['volume'].sum()

    return {
        "buy_volume": buy_volume,
        "sell_volume": sell_volume,
        "delta": buy_volume - sell_volume
    }