# pip install yfinance
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
from zoneinfo import ZoneInfo


def est_time_formatter(x, pos):
    dt = mdates.num2date(x).astimezone(ZoneInfo("America/New_York"))
    return dt.strftime('%H:%M')
# Parameters
ticker = "AAPL"
# Define your new date range (April 3, 2025)
start = datetime.date(2024, 1, 1)
end = datetime.date(2025, 3, 15)
interval = "1h"

# Download 10-minute interval data
df = yf.download(ticker, start=start, end=end, interval=interval)

# Flatten MultiIndex
df.columns = df.columns.get_level_values(0)

# Convert the DataFrame index to Eastern Time
df.index = df.index.tz_convert('America/New_York')

# Drop rows with missing data
df.dropna(inplace=True)

df = df[df['Volume'] > 0]

# Filter for the date range
df_range = df[(df.index.date >= start) & (df.index.date <= end)]

# Filter for the first hour (9:30 - 10:30)
first_hour_df = df_range.between_time("9:30", "10:30")

# Sum volume during the first hour for each trading day
daily_first_hour_volume = first_hour_df['Volume'].groupby(first_hour_df.index.date).sum()

# Count the number of trading days in the specified range
num_days = len(daily_first_hour_volume)

# Calculate the average first hour volume
avg_first_hour_volume = daily_first_hour_volume.sum() / num_days if num_days > 0 else 0

# Print the results
print("Total first-hour volume for each day:")
print(daily_first_hour_volume)
print(f"\nAverage first-hour volume across {num_days} trading days: {avg_first_hour_volume:,.0f}")

