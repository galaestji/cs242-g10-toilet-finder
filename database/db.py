import sqlite3
from config import DATABASE_NAME


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS toilets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            floor INTEGER,
            info TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            building_name TEXT
        )
    """)

    conn.commit()
    conn.close()