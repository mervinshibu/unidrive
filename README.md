## Setup instructions

1. Start dependencies: `docker-compose up -d` (brings up Postgres on 5432 and MinIO on 9000/9001).
2. Create a virtualenv and install deps:
   - macOS/Linux: `python3 -m venv venv && source venv/bin/activate`
   - Windows (PowerShell): `python -m venv venv; .\\venv\\Scripts\\Activate.ps1`
   - `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` (defaults match `docker-compose`: postgres/postgres and MinIO minioadmin/minioadmin on localhost). Adjust if needed.
4. Run the API: `uvicorn main:app --reload`.

## How to test

- Upload: `curl -F "file=@/path/to/file" http://localhost:8000/upload`
- List: `curl http://localhost:8000/files`
- Download: `curl -OJ http://localhost:8000/files/{id}`
- Delete: `curl -X DELETE http://localhost:8000/files/{id}`

## Design decisions

- FastAPI with `UploadFile` streams directly to S3/MinIO to avoid loading whole files into memory (aside from size check loop).
- Size guard implemented manually before upload to return a 413 for >20 MB.
- Metadata stored in Postgres tracks id, filename, size, mime type, S3 key, and uploaded timestamp.
- For file storage, the system uses MinIO, which provides S3-compatible APIs. Because of this compatibility, our application can use boto3 as if it were interacting with AWS S3, making local development and production deployment consistent.
