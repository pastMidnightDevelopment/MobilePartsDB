"""
File: database.py
Version: 0.1.0
Purpose: SQLite database functions for MobilePartsDB.
"""

# IMPORTS
import sqlite3
from datetime import datetime

from config import DATABASE_DIR, DATABASE_FILE, STATUS_NEEDS_INFO

# DATABASE
def initialize_database():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                quick_name TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)

        connection.commit()


def create_entry(quick_name):
    assert isinstance(quick_name, str)

    cleaned_name = quick_name.strip()

    if cleaned_name == "":
        cleaned_name = "Untitled Entry"

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO entries (created_at, quick_name, status)
            VALUES (?, ?, ?)
        """, (created_at, cleaned_name, STATUS_NEEDS_INFO))

        connection.commit()


def get_all_entries():
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, created_at, quick_name, status
            FROM entries
            ORDER BY id DESC
        """)

        return cursor.fetchall()