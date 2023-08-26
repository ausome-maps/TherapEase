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

# force register user
user_reg = {
    "name": "sample name",
    "email": "sample@sample.com",
    "password": "mypassword1234",
    "passwordConfirm": "mypassword1234",
}
user_reg_resp = requests.post(
    "http://localhost:9001/auth/register",
    headers={"Content-type": "application/json"},
    json=user_reg,
)
print(user_reg_resp.text)

# authenticate user
user = {"username": "sample@sample.com", "password": "mypassword1234"}
token = requests.post("http://localhost:9001/auth/jwt/login", data=user)
access_token = token.json()["access_token"]

# store to opensearch index
with open(data_path, "r") as therap_file:
    therap_data = json.load(therap_file)
    for d in therap_data["features"]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        resp = requests.put("http://localhost:9001/facilities", headers=headers, json=d)
        print(resp.json())
