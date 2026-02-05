# mt5_trader.py

import MetaTrader5 as mt5


def get_open_positions(symbol):
    positions = mt5.positions_get(symbol=symbol)
    return positions if positions else []


def place_trade(symbol, signal_row, lot=0.01, rr=2.0):

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        print("❌ No tick data")
        return

    atr = signal_row['ATR']

    if atr is None or atr == 0:
        print("⚠ ATR invalid")
        return

    # ---------------- BUY ----------------
    if signal_row['BUY_SIGNAL']:

        price = tick.ask
        sl = price - atr
        tp = price + (price - sl) * rr
        order_type = mt5.ORDER_TYPE_BUY
        print("📈 BUY signal detected")

    # ---------------- SELL ----------------
    elif signal_row['SELL_SIGNAL']:

        price = tick.bid
        sl = price + atr
        tp = price - (sl - price) * rr
        order_type = mt5.ORDER_TYPE_SELL
        print("📉 SELL signal detected")

    else:
        print("ℹ No trade signal")
        return

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 123456,
        "comment": "SmartMoneyBot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("❌ Trade failed:", result)
    else:
        print("✅ Trade executed:", result)
