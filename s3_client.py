import boto3
from botocore.client import Config

S3_ENDPOINT = "http://127.0.0.1:9000"
S3_ACCESS_KEY = "minioadmin"
S3_SECRET_KEY = "minioadmin"
S3_BUCKET = "files"

s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name="us-east-1",
    config=Config(signature_version="s3v4"),
)

# Create bucket if it doesn't exist
def ensure_bucket():
    buckets = s3_client.list_buckets()
    bucket_names = [b["Name"] for b in buckets.get("Buckets", [])]

    if S3_BUCKET not in bucket_names:
        s3_client.create_bucket(Bucket=S3_BUCKET)

ensure_bucket()
