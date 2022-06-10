import minio
import os

MINIO_HOST = os.path.environ["MWDB_S3_STORAGE_ENDPOINT"]
ACCESS_KEY = os.path.environ["MWDB_S3_STORAGE_ACCESS_KEY"]
SECRET_KEY = os.path.environ["MWDB_S3_STORAGE_SECRET_KEY"]
BUCKET_NAME = os.path.environ["MWDB_S3_STORAGE_BUCKET_NAME"]

minio.Minio(
    MINIO_HOST, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=True
).make_bucket(BUCKET_NAME)
