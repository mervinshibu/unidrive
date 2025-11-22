"""End-to-end tests for the FastAPI file service.

Assumes the API is running locally on http://localhost:8000 and that
dependencies (Postgres, MinIO) are up. Uses the sample test-image.jpg in
the repo root.
"""

import hashlib
import os
from io import BytesIO
from pathlib import Path
import uuid

import requests


BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
TEST_FILE = Path(__file__).parent / "test-file.jpg"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def test_end_to_end_flow():
    assert TEST_FILE.exists(), "test-image.jpg is missing in the repo root"
    original_hash = _sha256_file(TEST_FILE)

    # Error case: upload with no file should return 400
    resp_no_file = requests.post(f"{BASE_URL}/upload")
    assert resp_no_file.status_code == 400

    # Error case: upload a file over 20 MB should return 413
    # Create an in-memory file slightly over 20 MB
    over_limit_bytes = BytesIO(b"0" * (21 * 1024 * 1024))
    resp = requests.post(
        f"{BASE_URL}/upload",
        files={"file": ("too-big.bin", over_limit_bytes, "application/octet-stream")},
    )
    assert resp.status_code == 413

    # Happy path upload
    with TEST_FILE.open("rb") as f:
        upload_resp = requests.post(
            f"{BASE_URL}/upload",
            files={"file": (TEST_FILE.name, f, "image/jpeg")},
        )
    assert upload_resp.status_code == 200
    upload_body = upload_resp.json()
    file_id = upload_body["id"]

    try:
        # Download and verify checksum
        download_resp = requests.get(f"{BASE_URL}/files/{file_id}", stream=True)
        assert download_resp.status_code == 200
        downloaded_bytes = b"".join(download_resp.iter_content(chunk_size=8192))
        downloaded_hash = _sha256_bytes(downloaded_bytes)
        assert downloaded_hash == original_hash

        # List should contain the uploaded file metadata
        list_resp = requests.get(f"{BASE_URL}/files")
        assert list_resp.status_code == 200
        files = list_resp.json()
        assert any(item.get("id") == file_id for item in files)

        # Error case: fetching a non-existent file id returns 404
        missing_id = str(uuid.uuid4())
        missing_resp = requests.get(f"{BASE_URL}/files/{missing_id}")
        assert missing_resp.status_code == 404
    finally:
        # Delete the uploaded file
        delete_resp = requests.delete(f"{BASE_URL}/files/{file_id}")
        assert delete_resp.status_code == 200

    # After deletion, the file should return 404
    post_delete_resp = requests.get(f"{BASE_URL}/files/{file_id}")
    assert post_delete_resp.status_code == 404

    # Error case: deleting a non-existent file should return 404
    second_delete_resp = requests.delete(f"{BASE_URL}/files/{file_id}")
    assert second_delete_resp.status_code == 404


if __name__ == "__main__":
    # Allow running as a script without pytest
    test_end_to_end_flow()
    print("E2E test completed successfully")
