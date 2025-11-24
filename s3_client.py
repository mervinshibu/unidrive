import boto3
from botocore.client import Config
from dotenv import load_dotenv
import os

load_dotenv()

S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")

s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=S3_REGION,
    config=Config(signature_version="s3v4"),
)

# Create bucket if it doesn't exist
def ensure_bucket():
    buckets = s3_client.list_buckets()
    bucket_names = [b["Name"] for b in buckets.get("Buckets", [])]

    if S3_BUCKET not in bucket_names:
        s3_client.create_bucket(Bucket=S3_BUCKET)

ensure_bucket()
