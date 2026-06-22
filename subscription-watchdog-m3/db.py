import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    """
    Establish and return a connection to the Neon PostgreSQL database.
    Uses RealDictCursor to return query results as dictionaries.
    """
    if not DATABASE_URL:
        raise ValueError(
            "DATABASE_URL environment variable is not set. "
            "Please ensure you have configured it in your .env file."
        )
    return psycopg2.connect(
        DATABASE_URL,
        cursor_factory=psycopg2.extras.RealDictCursor
    )
