# import os

# import pandas as pd
# from influxdb_client_3 import InfluxDBClient3, Point, WritePrecision

# token = os.environ.get("INFLUXDB_TOKEN")
# org = "scc"
# host = "https://us-east-1-1.aws.cloud2.influxdata.com"

# client = InfluxDBClient3(host=host, token=token, org=org)


# database = "scc_data"


# # Get list of all csv files
# csv_files = [f for f in os.listdir("../data") if f.endswith(".csv")]

# for file in csv_files:
#     if "_Con_" in file:
#         print(f"Uploading {file} to InfluxDB...")
#         # Read the CSV file into a pandas DataFrame
#         df = pd.read_csv(f"../data/{file}")

#         # Convert the DataFrame to a list of dictionaries
#         data = df.to_dict("records")

#         # Create a list to hold the points
#         points = []

#         # Iterate over the data and create a point for each record
#         for record in data:
#             point = Point("conductivity")
#             for key, value in record.items():
#                 point.field(key, value)
#             points.append(point)

#         # Write the points to the database
#         # Check if the database already exists
#         if not client.get_database(database):
#             # If not, create it
#             client.create_database(database)

#         # Get the existing data from the database
#         existing_data = client.query(database=database)

#         # Append the new data to the existing data
#         new_data = existing_data + points

#         # Write the new data to the database
#         client.write(
#             database=database, record=new_data, write_precision=WritePrecision.NS
#         )

# print("CSV data uploaded to InfluxDB.")


import os

import pandas as pd
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB settings
token = os.environ.get("INFLUXDB_TOKEN")
org = "scc"
bucket = "scc_data"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

# Initialize the InfluxDB Client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Directory containing CSV files
csv_dir = "../data"

# Get list of all csv files
csv_files = [f for f in os.listdir(csv_dir) if f.endswith(".csv")]
print(csv_files)

for file in csv_files:
    if "_Con_" in file:
        print(f"Uploading {file} to InfluxDB...")
        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(os.path.join(csv_dir, file))
            df = df.dropna(axis=1, how="all")  # Drop empty columns
            df = df.dropna(axis=0, how="all")  # Drop empty rows
            df["timestamp"] = df["Date Time"]
            print(df.columns)
            # Convert `Date Time` column to a datetime object
            # Check if 'Date Time' column exists in the DataFrame
            if "timestamp" in df.columns:
                print("Converting 'timestamp' column to datetime object...")
                df["timestamp"] = pd.to_datetime(
                    df["timestamp"], format="%m/%d/%y %H:%M:%S.%f", errors="coerce"
                )
            else:
                print("ERORR: 'timestamp' column not found in DataFrame.")
            # Writing data to InfluxDB
            for row in df.itertuples():
                point = Point("conductivity").time(row.timestamp)
                for col in df.columns:
                    if col != "timestamp":  # Exclude the timestamp column
                        point.field(col, getattr(row, col))
                write_api.write(bucket=bucket, org=org, record=point)

            print(f"Successfully uploaded {file}.")
        except Exception as e:
            print(f"Failed to upload {file}. Error: {e}")

# Close the client
client.close()
