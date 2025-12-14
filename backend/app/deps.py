# dependencies

from collections.abc import Generator
from sqlalchemy.orm import Session
from app.db.database import SessionLocal

# DB session dependency
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # ensure the session will be closed after uses
