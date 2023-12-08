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
data_path = "path-to-data/FINAL_PASP_PAOT_with_id.json"
api_url = "http://127.0.0.1:9001"

# authenticate user
access_token = "my-access-token"  # retrieve from api admin

# store to opensearch index
with open(data_path, "r") as therap_file:
    therap_data = json.load(therap_file)
    for d in therap_data["features"]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {access_token}",
        }
        d["properties"]["contact_number"] = d["properties"]["contact_number_landline"]
        if len(d["properties"]["contact_number_mobile"]) > len(
            d["properties"]["contact_number_landline"]
        ):
            d["properties"]["contact_number"] = d["properties"]["contact_number_mobile"]
        d["properties"]["alt_contact_number"] = d["properties"]["alt_contact_numbers"]
        resp = requests.post(
            f"{api_url}/facilities",
            headers=headers,
            json=d,
        )
        print(d["id"], resp.status_code)
