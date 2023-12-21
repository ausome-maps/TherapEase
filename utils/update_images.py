'''
This script updates the images in the database from the minio bucket.
'''

import os
from apps.core.facilities.models import FacilityProperties
from minio import Minio

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
MINIO_API_HOST = "http://localhost:9000" # replace with host of minio
mc_client = Minio(
    "localhost:9000", # replace with host of minio
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False # set to true
)

image_bucket = "images"
url_template = f"{MINIO_API_HOST}/{image_bucket}"

objects = mc_client.list_objects(bucket_name=image_bucket, recursive=True)
images = {}
for object in objects:
    obj_name_list = object.object_name.split("/")
    facility_id = obj_name_list[0]
    filename = obj_name_list[1]
    new_img_dict = {
        "img_url": f"{url_template}/{facility_id}/{filename}",
        "img_label": filename
    }
    if facility_id in images.keys():
        images[facility_id].append(new_img_dict)
    else:
        images[facility_id] = [new_img_dict]

for image in images:
    fp = FacilityProperties.objects.get(osm_id=image)
    fp.images = images[image]
    fp.save()
    