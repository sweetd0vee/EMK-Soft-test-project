from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load the database URL from environment variables or .env file
SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")
# For local development, you can uncomment this line:
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1:5432/shop"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configure session factory: disable autocommit and autoflush for explicit control
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """
    Provide a SQLAlchemy database session generator for dependency injection.
    This ensures the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
