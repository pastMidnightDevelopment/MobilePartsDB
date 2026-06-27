"""
File: database.py
Version: 0.2.1
Purpose: SQLite database functions for MobilePartsDB.
"""

# IMPORTS
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

from config import DATABASE_DIR, DATABASE_FILE, PHOTOS_DIR, STATUS_NEEDS_INFO


# CONSTANTS
PHOTO_EXTENSION_DEFAULT = ".jpg"


# DATABASE
def initialize_database():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_id INTEGER NOT NULL,
                photo_path TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (entry_id) REFERENCES entries (id)
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

        entry_id = cursor.lastrowid

    create_entry_photo_folder(entry_id)

    return entry_id


def create_entry_photo_folder(entry_id):
    assert isinstance(entry_id, int)

    entry_photo_folder = PHOTOS_DIR / str(entry_id)
    entry_photo_folder.mkdir(parents=True, exist_ok=True)

    return entry_photo_folder


def get_next_photo_number(entry_id):
    assert isinstance(entry_id, int)

    photos = get_photos_for_entry(entry_id)

    return len(photos) + 1


def build_photo_file_path(entry_id, photo_number, file_extension=PHOTO_EXTENSION_DEFAULT):
    assert isinstance(entry_id, int)
    assert isinstance(photo_number, int)
    assert isinstance(file_extension, str)

    entry_photo_folder = create_entry_photo_folder(entry_id)
    clean_extension = file_extension.lower().strip()

    if clean_extension == "":
        clean_extension = PHOTO_EXTENSION_DEFAULT

    if not clean_extension.startswith("."):
        clean_extension = f".{clean_extension}"

    file_name = f"{photo_number:03d}{clean_extension}"

    return entry_photo_folder / file_name


def add_photo_to_entry(entry_id, source_photo_path):
    assert isinstance(entry_id, int)
    assert isinstance(source_photo_path, str)

    source_path = Path(source_photo_path)

    if not source_path.exists():
        raise FileNotFoundError(f"Photo file not found: {source_photo_path}")

    photo_number = get_next_photo_number(entry_id)
    destination_path = build_photo_file_path(
        entry_id,
        photo_number,
        source_path.suffix
    )

    shutil.copy2(source_path, destination_path)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO photos (entry_id, photo_path, created_at)
            VALUES (?, ?, ?)
        """, (entry_id, str(destination_path), created_at))

        connection.commit()

    return destination_path


def get_photos_for_entry(entry_id):
    assert isinstance(entry_id, int)

    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, photo_path, created_at
            FROM photos
            WHERE entry_id = ?
            ORDER BY id ASC
        """, (entry_id,))

        return cursor.fetchall()


def get_all_entries():
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, created_at, quick_name, status
            FROM entries
            ORDER BY id DESC
        """)

        return cursor.fetchall()