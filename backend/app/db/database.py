from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..utils.config import DATABASE_URL

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set!")

# Create the database engine
engine = create_engine(DATABASE_URL)

# Each request will use a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()
