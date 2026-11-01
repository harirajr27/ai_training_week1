import os
import sys

# Append the project root to sys.path so scripts can find modules inside config/src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import get_db_connection


def create_tables():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        department VARCHAR(100),
        salary NUMERIC CHECK (salary > 0)
    );
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'employees' created successfully with required constraints!")
    except Exception as e:
        print(f"Failed to create table: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    create_tables()
