"""
This the loader script for the therapy centers data.
Requirements
  - python requests
Usage
  - replace the data_path variable with the location of the therapy_centers
  - python load_data.py
"""

import json
import requests

# replace with location of data json
data_path = "/Users/lkp/Dev/projects/ausomemaps/FINAL_PASP_PAOT_with_id.json"

with open(data_path, "r") as therap_file:
    therap_data = json.load(therap_file)
    for d in therap_data["features"]:
        headers = {"Content-Type": "application/json"}
        resp = requests.put("http://localhost:9001/facilities", headers=headers, json=d)
        print(resp.json())
