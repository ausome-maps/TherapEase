import json
import requests

# replace with location of data json
data_path = (
    "/Users/lkp/Dev/projects/ausomemaps/formatted_therapycenters_with_id_8222023.json"
)

with open(data_path, "r") as therap_file:
    therap_data = json.load(therap_file)
    for d in therap_data["features"]:
        headers = {"Content-Type": "application/json"}
        resp = requests.put("http://localhost:9001/facilities", headers=headers, json=d)
        print(resp.json())
