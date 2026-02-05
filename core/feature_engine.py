#feature_engine.py
from core.indicators import *
from core.market_structure import *
from core.structure_logic import *
from core.smart_money_logic import *
from core.signal_generator import generate_signals


def build_features(df):
    df = add_moving_averages(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_atr(df)

    df = detect_trend(df)
    df = support_resistance(df)
    df = detect_swings(df)
    df = detect_bos_choch(df)

    return df


def build_smart_money(ltf_df, htf_df):
    df = align_htf_structure(ltf_df, htf_df)
    df = detect_liquidity_sweep(df)
    df = detect_engulfing(df)
    df = detect_fvg(df)

    return df


def build_signals(df):
    return generate_signals(df)