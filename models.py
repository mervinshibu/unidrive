from datetime import datetime
from sqlalchemy import Column, String, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    size = Column(BigInteger, nullable=False)
    mime_type = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
