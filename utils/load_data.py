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

urls = "http://localhost:9001"

# implement a login with 
data = {"username": "root@admin.com", "password": "rootpassword1234"}
r = requests.post(urls + "/auth/jwt/login", data=data)
access_token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

# replace with location of data json
data_path = (
    "/Users/lkp/Dev/projects/ausomemaps/formatted_therapycenters_with_id_8222023.json"
)

with open(data_path, "r") as therap_file:
    therap_data = json.load(therap_file)
    for d in therap_data["features"]:
        resp = requests.put(f"{urls}/facilities", headers=headers, json=d)
        print(resp.json())
