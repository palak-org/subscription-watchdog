import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_connection():
    """
    Establish and return a connection to the Neon PostgreSQL database.
    Uses RealDictCursor to return query results as dictionaries.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        env_keys = list(os.environ.keys())
        commit_sha = os.getenv("RAILWAY_GIT_COMMIT_SHA", "unknown")
        raise ValueError(
            "DATABASE_URL environment variable is not set. "
            f"Active Commit: {commit_sha}. Available env keys: {env_keys}"
        )
    return psycopg2.connect(
        db_url,
        cursor_factory=psycopg2.extras.RealDictCursor
    )
