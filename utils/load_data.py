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
data_path = "/Users/lkp/Dev/projects/ausomemaps/data/FINAL_PASP_PAOT_with_id.json"
api_url = "http://127.0.0.1:9001"

secret_key = "thisisaverysecretkey12345"

# force register user
user_reg = {
    "name": "admin_user",
    "email": "sample@sample.com",
    "password": "mypassword1234",
    "passwordConfirm": "mypassword1234",
}
user_reg_resp = requests.post(
    f"{api_url}/auth/register",
    headers={"Content-type": "application/json"},
    json=user_reg,
)

# authenticate user
user = {"username": user_reg["email"], "password": user_reg["password"]}
token = requests.post(f"{api_url}/auth/jwt/login", data=user)
access_token = token.json()["access_token"]

# store to opensearch index
with open(data_path, "r") as therap_file:
    therap_data = json.load(therap_file)
    for d in therap_data["features"]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        d["key"] = secret_key
        resp = requests.put(
            f"{api_url}/facilities",
            headers=headers,
            json=d,
            cookies={"key": secret_key},
        )
        print(resp.text)
