import pandas as pd

# ---------------- FILE PATHS ----------------

mcx_file    = r"D:/Projects/pythons/mt5/mcx_gold_filled.csv"
xau_file    = r"D:/Projects/pythons/mt5/XAUUSD_H1.csv"
usdinr_file = r"D:/Projects/pythons/mt5/usdinr_fut_filled.csv"

# ---------------- LOAD MCX GOLD (IST) ----------------

mcx = pd.read_csv(mcx_file)
mcx['Date'] = pd.to_datetime(mcx['Date'])   # already IST
mcx = mcx.rename(columns={'Date': 'time', 'Close': 'mcx_close'})
mcx['mcx_close'] = pd.to_numeric(mcx['mcx_close'], errors='coerce')
mcx = mcx[['time', 'mcx_close']].dropna()

# ---------------- LOAD USDINR FUT (IST) ----------------

usd = pd.read_csv(usdinr_file)
usd['Date'] = pd.to_datetime(usd['Date'])   # already IST
usd = usd.rename(columns={'Date': 'time', 'Close': 'usdinr'})
usd['usdinr'] = pd.to_numeric(usd['usdinr'], errors='coerce')
usd = usd[['time', 'usdinr']].dropna()

# ---------------- LOAD XAUUSD (MT5 - UTC → IST) ----------------

xau = pd.read_csv(xau_file)
xau['time'] = pd.to_datetime(xau['time'])

# 🔥 IMPORTANT: Convert UTC → IST
xau['time'] = xau['time'] + pd.Timedelta(hours=5, minutes=30)

xau = xau.rename(columns={'close': 'xau_close'})
xau['xau_close'] = pd.to_numeric(xau['xau_close'], errors='coerce')
xau = xau[['time', 'xau_close']].dropna()

# ---------------- SORT ALL ----------------

mcx = mcx.sort_values('time')
usd = usd.sort_values('time')
xau = xau.sort_values('time')

# ---------------- MERGE ALL DATA ----------------

# Merge MCX with XAUUSD
data = pd.merge_asof(
    mcx,
    xau,
    on='time',
    tolerance=pd.Timedelta('30min'),
    direction='nearest'
)

# Merge USDINR
data = pd.merge_asof(
    data,
    usd,
    on='time',
    tolerance=pd.Timedelta('30min'),
    direction='nearest'
)

# Drop rows where something is missing
data = data.dropna()

# ---------------- CONVERT MCX → USD / OUNCE ----------------

GRAMS_PER_OUNCE = 31.1035
data['mcx_usd_per_oz'] = (data['mcx_close'] * GRAMS_PER_OUNCE) / data['usdinr']

# ---------------- COMPARE ----------------

data['price_diff'] = data['mcx_usd_per_oz'] - data['xau_close']
corr = data['mcx_usd_per_oz'].corr(data['xau_close'])

print("\n📊 Correct Gold Comparison Preview:")
print(data[['time', 'mcx_usd_per_oz', 'xau_close', 'price_diff']].head())

print("\n🔗 Correlation (MCX GoldPetal vs XAUUSD):", corr)

# Save final result
data.to_csv("MCX_vs_XAUUSD_with_USDINR.csv", index=False)
print("\n📁 Saved as MCX_vs_XAUUSD_with_USDINR.csv")