from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from uuid import uuid4
from models import FileMetadata, Base
from database import engine, get_db
from sqlalchemy.orm import Session
from s3_client import s3_client, S3_BUCKET

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Generate unique ID
    file_id = str(uuid4())
    MAX_SIZE = 20 * 1024 * 1024  # 20 MB
    chunk_size = 1024 * 1024  # 1 MB
    size = 0
    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        size += len(chunk)

        if size > MAX_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File too large. Max allowed size is 20 MB."
            )

    # Reset file pointer before uploading to MinIO
    await file.seek(0)

    # Determine S3/MinIO object key
    s3_key = f"{file_id}_{file.filename}"

    # Upload to MinIO
    try:
        s3_client.upload_fileobj(
            file.file,
            S3_BUCKET,
            s3_key,
            ExtraArgs={"ContentType": file.content_type},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store file: {str(e)}")

    # Save metadata in DB
    metadata = FileMetadata(
        id=file_id,
        filename=file.filename,
        size=size,
        mime_type=file.content_type,
        s3_key=s3_key
    )

    db.add(metadata)
    db.commit()
    db.refresh(metadata)

    return {"id": file_id, "message": "File uploaded successfully"}


@app.get("/files")
def list_files(db: Session = Depends(get_db)):
    files = db.query(FileMetadata).all()
    return files


@app.get("/files/{file_id}")
def get_file(file_id: str, db: Session = Depends(get_db)):
    metadata = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()

    if not metadata:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=metadata.s3_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download from S3: {str(e)}")
    return StreamingResponse(
        response["Body"],
        media_type=metadata.mime_type,
        headers={"Content-Disposition": f'attachment; filename="{metadata.filename}"'}
    )

@app.delete("/files/{file_id}")
def delete_file(file_id: str, db: Session = Depends(get_db)):
    metadata = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()

    if not metadata:
        raise HTTPException(status_code=404, detail="File not found")
    try:
        s3_client.delete_object(Bucket=S3_BUCKET, Key=metadata.s3_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete from S3: {str(e)}")
    db.delete(metadata)
    db.commit()

    return {"message": "File deleted successfully"}
