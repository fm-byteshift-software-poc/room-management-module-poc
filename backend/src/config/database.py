import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use file-based SQLite for dev. Works reliably with multiple connections.
# For cloud deploys with ephemeral FS, switch back to :memory: and accept seed-on-every-request.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./room_poc.db")

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()