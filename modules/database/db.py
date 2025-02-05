from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from typing import Generator
from dotenv import load_dotenv

# Load the .env file into the environment variables
load_dotenv()

# Retrieve variables (provide defaults as needed)
POSTGRES_USER = os.environ.get("username", "postgres")
POSTGRES_PASSWORD = os.environ.get("password", "secret")
POSTGRES_DB = os.environ.get("database", "mydatabase")
POSTGRES_HOST = os.environ.get("hostname", "localhost")
POSTGRES_PORT = os.environ.get("port", "5432")

# Construct the connection URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

print("Connection URL:", SQLALCHEMY_DATABASE_URL)

# 2. Create engine
#    Note: You can configure your pool size, timeouts, etc. as needed.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=0,     # Disallow pool overflow
    pool_timeout=30,    # Seconds to wait before giving up on a connection
    pool_recycle=1800,  # Recycle connections after 30 minutes
)

# 3. Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """Dependency that provides a SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()