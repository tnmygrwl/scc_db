import os

import pandas as pd
from flask import Flask, request
from werkzeug.utils import secure_filename

# from influxdb_client_3 import InfluxDBClient3, Point, WritePrecision
# from screen import calculate_specific_conductance_seawater
# import upload_to_influxdb


app = Flask(__name__)


def upload_to_influxdb(data):
    # Code from ingest.py to upload data to InfluxDB
    pass


def calculate_specific_conductance_seawater(ye, t):
    # Code from screen.py to calculate specific conductance
    pass


def process_and_upload(filepath):
    df = pd.read_csv(filepath)
    highRange = df["HighRange"]
    temp = df["temp"]
    processed_data = [
        calculate_specific_conductance_seawater(ye, t) for ye, t in zip(highRange, temp)
    ]
    upload_to_influxdb(processed_data)


@app.route("/api/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    filename = secure_filename(file.filename)
    filepath = os.path.join("/path/to/save", filename)  # some db
    file.save(filepath)
    process_and_upload(filepath)
    return "File uploaded and data processed successfully."
