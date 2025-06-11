import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from urllib.parse import urlparse

# Load from environment if needed
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Jones14@localhost:5432/petpal_db")

def check_db_url(url):
    try:
        result = urlparse(url)
        assert result.scheme.startswith("postgres")
        assert result.hostname is not None
        assert result.path != ''
        print(f"URL is valid: {url}")
        return True
    except Exception as e:
        print(f"Invalid DATABASE_URL: {e}")
        return False

def check_db_connection(url):
    if not check_db_url(url):
        return False
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("Database connection successful!")
        return True
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    url = DATABASE_URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    check_db_connection(url)
