# draw_tools.py
import numpy as np

def trendline(df, lookback=50):
    y = df['close'].tail(lookback).values
    x = np.arange(len(y))

    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept

def supply_demand_zones(df, window=30):
    supply = df['high'].rolling(window).max()
    demand = df['low'].rolling(window).min()
    return supply, demand