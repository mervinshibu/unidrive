from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

USERNAME = "postgres"
PASSWORD = "postgres"
HOSTNAME = "127.0.0.1:5432"
DATABASE_NAME = "files_db"

# DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DATABASE_NAME}"

DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1:5432/files_db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
