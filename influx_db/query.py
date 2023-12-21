import os

from influxdb_client_3 import InfluxDBClient3

token = os.environ.get("INFLUXDB_TOKEN")
org = "scc"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"

client = InfluxDBClient3(host=host, token=token, org=org)
# query = """
# SELECT "Date Time", "CONDUCTIVITY (?S/cm)  #21742582", "Temp (°C)  #21742582", "Specific Conductance (?S/cm)", "Salinity (ppt)"
# FROM "conductivity"
# """

query = '''SELECT * FROM "conductivity"'''


# Execute the query
table = client.query(query=query, database="scc_data", language="sql")

# Convert to dataframe
# df = table.to_pandas().sort_values(by="Date Time")
df = table.to_pandas()
print(df)
