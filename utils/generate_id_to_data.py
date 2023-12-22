"""
This generates the id of the data in uuid format.

Usage
  - replace data path variable with the location of the json contianing the datasets.
  - python generate_id_to_data.py

Output
  - the original json with the added ID in uuid format.
"""

import uuid
import json

data = "<path-to-json>.json"

main_dict = {"type": "FeatureCollection", "name": "Ausome Maps", "features": []}

data_with_id = []

with open(data, "r") as facilities_data_file:
    facilities_data = json.load(facilities_data_file)
    for facilities in facilities_data["features"]:
        facility_info = facilities.copy()
        if facility_info["id"] == "":
            facility_info["id"] = str(uuid.uuid4())
        data_with_id.append(facility_info)

main_dict["features"] = data_with_id

with open(f"{data}_with_id.json", "w") as output_file:
    json.dump(main_dict, output_file)
