import os
from minio import Minio
from minio.error import S3Error


def _get_minio_client():
    return Minio(
        os.environ.get("MINIO_ENDPOINT", "localhost:9000"),
        access_key=os.environ.get("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.environ.get("MINIO_SECRET_KEY", "minioadmin"),
        secure=os.environ.get("MINIO_SECURE", "0") == "1",
    )


def upload_to_minio(uploaded_file):
    bucket = os.environ.get("MINIO_BUCKET", "submissions")
    client = _get_minio_client()

    try:
        found = client.bucket_exists(bucket)
        if not found:
            client.make_bucket(bucket)

        name = uploaded_file.name
        base, ext = os.path.splitext(name)
        safe_name = f"{base}{ext.lower()}"

        ext_lower = ext.lower()
        ext_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        content_type = ext_map.get(ext_lower, "application/octet-stream")

        client.put_object(
            bucket,
            safe_name,
            uploaded_file,
            length=uploaded_file.size,
            content_type=content_type,
        )

        endpoint = os.environ.get("MINIO_PUBLIC_ENDPOINT", os.environ.get("MINIO_ENDPOINT", "localhost:9000"))
        secure = os.environ.get("MINIO_SECURE", "0") == "1"
        protocol = "https" if secure else "http"
        url = f"{protocol}://{endpoint}/{bucket}/{safe_name}"

        return {"img_name": safe_name, "img_url": url}

    except S3Error as e:
        return {"error": f"Upload failed: {e}"}
