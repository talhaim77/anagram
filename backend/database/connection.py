import psycopg2
from backend.config import settings as app_config


def get_connection():
    """
    Returns a new database connection using credentials from environment variables.
    """
    conn = psycopg2.connect(
        host=app_config.DB_HOST,
        dbname=app_config.DB_NAME,
        user=app_config.DB_USER,
        password=app_config.DB_PASSWORD
    )
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS words (
                    word TEXT PRIMARY KEY,
                    sorted_word TEXT
                );
            """)
            conn.commit()