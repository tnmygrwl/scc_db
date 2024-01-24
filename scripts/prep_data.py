import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define the file name
file_name = "RB1_SpecCon_6_9_2023_lkg.csv"

# Read the CSV file
df = pd.read_csv(file_name)

# Check if the first row contains "Plot Title"
if "Plot Title" in df.iloc[0].values:
    df = df.iloc[1:]

# Set the first row as column names
df.columns = df.iloc[0]
df = df.iloc[1:]

# Convert the date column to datetime format
df["Date Time, GMT-04:00"] = pd.to_datetime(df["Date Time, GMT-04:00"])

# Extract the end date from the file name
end_date_str = file_name.split("_")[2]
end_date = datetime.strptime(end_date_str, "%m_%d_%Y")

# Calculate the start date
start_date = end_date - timedelta(days=7)

# Find the first and last non-zero and non-NaN value in the "High Range" column
first_index = df[df["HighRange"].replace(0, np.nan).notna()].index[0]
last_index = df[df["HighRange"].replace(0, np.nan).notna()].index[-1]

# Record the details
details = {
    "start_date": start_date,
    "end_date": end_date,
    "first_index": first_index,
    "last_index": last_index
}
