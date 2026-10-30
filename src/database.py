import psycopg2
from config.settings import DATABASE_URL

def get_db_connection():
    """Opens a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise e
