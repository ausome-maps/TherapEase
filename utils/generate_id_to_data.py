import uuid
import json

data = "/Users/lkp/Downloads/FINAL_PASP_PAOT.json"

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

with open("FINAL_PASP_PAOT.json", "w") as output_file:
    json.dump(main_dict, output_file)
