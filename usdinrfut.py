import pandas as pd

# Load your data
df = pd.read_csv("USDINR JAN FUT (20260121160000000 _ 20251202120000000).csv")

# Clean and parse Date column
df['Date'] = df['Date'].str.replace(r" GMT.*", "", regex=True)
df['Date'] = pd.to_datetime(df['Date'], format="%a %b %d %Y %H:%M:%S")

df = df.sort_values('Date').reset_index(drop=True)

filled_rows = []

for i in range(len(df) - 1):
    current_row = df.iloc[i]
    next_row = df.iloc[i + 1]

    filled_rows.append(current_row)

    current_time = current_row['Date']
    next_time = next_row['Date']

    gap_hours = int((next_time - current_time).total_seconds() // 3600)

    # If market closed gap (after 5 PM till next 9 AM)
    if gap_hours > 1:
        last_close = current_row['Close']

        for h in range(1, gap_hours):
            new_time = current_time + pd.Timedelta(hours=h)

            fake_row = {
                'Date': new_time,
                'Open': last_close,
                'High': last_close,
                'Low': last_close,
                'Close': last_close,
                'Volume': 0,
                'RSI(14)': None,
                'MACD(12,26,9)': None,
                'Signal MACD(12,26,9)': None,
                'MACD(12,26,9)_hist': None
            }

            filled_rows.append(pd.Series(fake_row))

# Add last original row
filled_rows.append(df.iloc[-1])

new_df = pd.DataFrame(filled_rows)

new_df = new_df.sort_values('Date').reset_index(drop=True)

# Save output
new_df.to_csv("usdinr_fut_filled.csv", index=False)

print("✅ USDINR FUT overnight freeze candles inserted successfully!")
