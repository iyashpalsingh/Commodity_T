import pandas as pd

# ============================================================
# SCRIPT: MCX Overnight / Holiday Reaction to XAUUSD
# ------------------------------------------------------------
# This script:
# 1. Uses your aligned dataset (MCX + XAUUSD + USDINR, IST time)
# 2. Detects periods where MCX price is flat (market closed / holiday)
# 3. Measures how XAUUSD moved during that closed window
# 4. Measures how MCX reacted on the FIRST candle after market open
# 5. Saves a summary file for analysis / ML
# ============================================================

# ---------------- FILE PATH ----------------

# This should be the file you created earlier after alignment + filling
input_file = r"D:/Projects/pythons/mt5/MCX_vs_XAUUSD_with_USDINR.csv"

# ---------------- LOAD DATA ----------------

data = pd.read_csv(input_file)
data['time'] = pd.to_datetime(data['time'])

data = data.sort_values('time').reset_index(drop=True)

# ---------------- PARAMETERS ----------------

# Minimum hours of flat MCX to consider market closed (night / holiday)
MIN_CLOSED_HOURS = 2

# ---------------- DETECT CLOSED PERIODS ----------------

closed_windows = []

start_idx = None

for i in range(1, len(data)):
    # If MCX price unchanged → possibly market closed
    if data.loc[i, 'mcx_close'] == data.loc[i-1, 'mcx_close']:
        if start_idx is None:
            start_idx = i - 1
    else:
        # MCX price changed again → market opened
        if start_idx is not None:
            end_idx = i - 1

            duration = end_idx - start_idx + 1

            # Only consider meaningful closures
            if duration >= MIN_CLOSED_HOURS:
                closed_windows.append((start_idx, end_idx, i))  # i = first open candle index

            start_idx = None

# ---------------- ANALYZE EACH CLOSED WINDOW ----------------

results = []

for (start_idx, end_idx, open_idx) in closed_windows:
    start_row = data.loc[start_idx]
    end_row   = data.loc[end_idx]
    open_row  = data.loc[open_idx]

    # Time info
    close_start_time = start_row['time']
    close_end_time   = end_row['time']
    open_time        = open_row['time']

    hours_closed = int((close_end_time - close_start_time).total_seconds() / 3600) + 1

    # XAUUSD movement during MCX closed period
    xau_start = start_row['xau_close']
    xau_end   = end_row['xau_close']

    xau_return = (xau_end - xau_start) / xau_start * 100

    # MCX reaction at open
    mcx_last_close = start_row['mcx_close']
    mcx_open_price = open_row['mcx_close']

    mcx_gap = (mcx_open_price - mcx_last_close) / mcx_last_close * 100

    # Direction comparison
    xau_dir = "UP" if xau_return > 0 else "DOWN" if xau_return < 0 else "FLAT"
    mcx_dir = "UP" if mcx_gap > 0 else "DOWN" if mcx_gap < 0 else "FLAT"

    same_direction = (xau_dir == mcx_dir)

    results.append({
        "close_start": close_start_time,
        "close_end": close_end_time,
        "open_time": open_time,
        "hours_closed": hours_closed,
        "xau_start": xau_start,
        "xau_end": xau_end,
        "xau_return_pct": xau_return,
        "mcx_last_close": mcx_last_close,
        "mcx_open": mcx_open_price,
        "mcx_gap_pct": mcx_gap,
        "xau_direction": xau_dir,
        "mcx_direction": mcx_dir,
        "same_direction": same_direction
    })

# ---------------- SAVE & REPORT ----------------

summary = pd.DataFrame(results)

summary.to_csv("MCX_overnight_reaction_summary.csv", index=False)

print("\n📊 Overnight / Holiday Reaction Analysis Completed")
print("Total closed windows detected:", len(summary))

if len(summary) > 0:
    accuracy = summary['same_direction'].mean() * 100
    print(f"Direction match accuracy: {accuracy:.2f}%")

    print("\nSample results:")
    print(summary.head())

print("\n📁 Saved as MCX_overnight_reaction_summary.csv")
