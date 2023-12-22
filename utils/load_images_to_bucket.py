"""
The loader script for uploading images to a minio bucket.
Requirements
  - minio
Usage
  - ensure that the following are available:
    - MINIO: ACCESS_KEY, SECRET_KEY, MINIO_DOMAIN
    - FILES: LOCAL_IMG_DIR
      - the images should be in the format of /path-to-image-dir/folder-name/filename
"""

from minio import Minio
from dotenv import load_dotenv
import os
import json

load_dotenv()

LOCAL_IMG_DIR = os.environ.get('LOCAL_IMG_DIR', 'images')

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
MINIO_DOMAIN = os.environ.get('MINIO_DOMAIN', "localhost:9000")
MINIO_API_HOST = f"http://{MINIO_DOMAIN}"
MINIO_CLIENT = Minio(
    MINIO_DOMAIN,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False # set to true
)

def create_bucket(bucket_name):
    bucket_name = bucket_name.replace("/", "")
    found = MINIO_CLIENT.bucket_exists(bucket_name)
    if not found:
        MINIO_CLIENT.make_bucket(bucket_name)
    else:
        print("Bucket already exists")

    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
                "Resource": f"arn:aws:s3:::{bucket_name}",
            },
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*",
            },
        ],
    }
    MINIO_CLIENT.set_bucket_policy(bucket_name, json.dumps(bucket_policy))

def upload_file(orig_path):
    bucket = orig_path.split("/")[1]
    filename = orig_path.split("/")[-1]
    # print(bucket, filename)    
    MINIO_CLIENT.fput_object(
        bucket, filename, orig_path,
    )

if __name__ == "__main__":
    for root, dirs, files in os.walk(LOCAL_IMG_DIR):
        for dir in dirs: 
            create_bucket(dir)
        for file in files:
            upload_file(os.path.join(root, file))

