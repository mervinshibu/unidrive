## Setup instructions

1. Setup docker: `docker-compose up -d` (brings up Postgres on 5432 and MinIO on 9000/9001).
2. Create a python virtualenv and install depedencies:
   - macOS/Linux: `python3 -m venv venv && source venv/bin/activate`
   - Windows (PowerShell): `python -m venv venv; .\\venv\\Scripts\\Activate.ps1`
   - `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` (defaults match `docker-compose`: postgres/postgres and MinIO minioadmin/minioadmin on localhost). Adjust if needed.
4. Run the API: `uvicorn main:app --reload`.

## Basic Usage

- Upload: ```curl -F "file=@/path/to/file" http://localhost:8000/upload```
- List: ```curl http://localhost:8000/files```
- Download: ```curl -OJ http://localhost:8000/files/{id}```
- Delete: ```curl -X DELETE http://localhost:8000/files/{id}```

## Manual tests

Manual checks via FastAPI's Swagger UI (http://localhost:8000/docs):

- Test 1 — Small File Upload (Success): upload a small file (e.g., .txt); expect 200 with an `id`; confirm file in MinIO console and metadata in Postgres via Adminer. Verifies upload flow, DB insert, S3 storage.
- Test 2 — File Too Large (>20MB) (Failure): upload >20MB; expect 413. Verifies max-size validation.
- Test 3 — Download Existing File: GET `/files/{id}` from Test 1; expect exact file; compare contents. Verifies S3 → API streaming.
- Test 4 — Download Non-Existing File: GET `/files/<invalid-id>`; expect 404. Verifies error handling.
- Test 5 — List Files: GET `/files`; expect array of metadata objects. Verifies DB retrieval.
- Test 6 — Delete File: DELETE `/files/{id}` from Test 1, then GET `/files/{id}` → 404 and confirm removal from MinIO. Verifies cleanup logic.

## Assumptions

- Local Postgres and MinIO via the provided `docker-compose.yml` on default ports.
- MinIO credentials/bucket come from `.env` and match the defaults (`minioadmin`, bucket `files`).
- Files are limited to 20 MB per upload in this version.

## Design decisions

- Uploads are handled using FastAPI’s `UploadFile`, which streams data to a temporary file instead of loading it into memory. The API processes the file in 1MB chunks for size validation, and boto3 then streams it to S3/MinIO, ensuring constant low memory usage.
- Size guard implemented manually before upload to return a 413 for >20 MB.
- Metadata stored in Postgres tracks id, filename, size, mime type, S3 key, and uploaded timestamp.
- For file storage, the system uses MinIO, which provides S3-compatible APIs. Because of this compatibility, our application can use boto3 as if it were interacting with AWS S3, making local development and production deployment consistent.

## AI Usage
As permitted in the assignment guidelines, I used AI selectively to assist with certain aspects of the project. 
Final architectural decisions and code implementation were made by me.
I also used AI to improve the clarity and wording of my README.md.
All the technical content, structure, and explanations in the README were written by me — AI was only used to improve English phrasing and readability.
### Prompts Used
- How do I interact with a MinIO server in Python using an S3-compatible client such as boto3?
- Give me Python code to validate an uploaded file’s size without loading the whole file into memory. I want to read the file in 1MB chunks and reject it if it exceeds 20MB.
- Give me code for a full end-to-end automated test using Python `requests` to test all API flows. Start by uploading a file (e.g., test-file.jpg from the same directory), check the upload response, then use the GET API to download the file and verify integrity via checksum. Next, call the list API to confirm the uploaded file appears, then delete the file and confirm deletion by calling GET again. Also include negative tests: sending no file in the payload, sending an in-memory file larger than 20 MB (to trigger the 413 error), and GET/DELETE requests for non-existent IDs. 

