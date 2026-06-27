"""
File: database.py
Version: 0.3.0
Purpose: SQLite database and attachment functions for MobilePartsDB.
"""

# IMPORTS
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

from config import DATABASE_DIR, DATABASE_FILE, PHOTOS_DIR, STATUS_NEEDS_INFO


# CONSTANTS
FILE_EXTENSION_DEFAULT = ".jpg"

FILE_TYPE_IMAGE = "image"
FILE_TYPE_VIDEO = "video"
FILE_TYPE_AUDIO = "audio"
FILE_TYPE_PDF = "pdf"
FILE_TYPE_DOCUMENT = "document"


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
            CREATE TABLE IF NOT EXISTS attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_id INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT NOT NULL,
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

    create_entry_attachment_folder(entry_id)

    return entry_id


def create_entry_attachment_folder(entry_id):
    assert isinstance(entry_id, int)

    entry_attachment_folder = PHOTOS_DIR / str(entry_id)
    entry_attachment_folder.mkdir(parents=True, exist_ok=True)

    return entry_attachment_folder


def get_attachments_for_entry(entry_id):
    assert isinstance(entry_id, int)

    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, file_path, file_type, created_at
            FROM attachments
            WHERE entry_id = ?
            ORDER BY id ASC
        """, (entry_id,))

        return cursor.fetchall()


def get_next_attachment_number(entry_id):
    assert isinstance(entry_id, int)

    attachments = get_attachments_for_entry(entry_id)

    return len(attachments) + 1


def build_attachment_file_path(
    entry_id,
    attachment_number,
    file_extension=FILE_EXTENSION_DEFAULT
):
    assert isinstance(entry_id, int)
    assert isinstance(attachment_number, int)
    assert isinstance(file_extension, str)

    create_entry_attachment_folder(entry_id)

    clean_extension = file_extension.lower().strip()

    if clean_extension == "":
        clean_extension = FILE_EXTENSION_DEFAULT

    if not clean_extension.startswith("."):
        clean_extension = f".{clean_extension}"

    file_name = f"{attachment_number:03d}{clean_extension}"

    relative_file_path = Path(str(entry_id)) / file_name
    full_file_path = PHOTOS_DIR / relative_file_path

    return relative_file_path, full_file_path


def add_attachment_to_entry(
    entry_id,
    source_file_path,
    file_type=FILE_TYPE_IMAGE
):
    assert isinstance(entry_id, int)
    assert isinstance(source_file_path, str)
    assert isinstance(file_type, str)

    source_file = Path(source_file_path)

    if not source_file.exists():
        raise FileNotFoundError(f"Attachment file not found: {source_file_path}")

    attachment_number = get_next_attachment_number(entry_id)

    relative_file_path, full_file_path = build_attachment_file_path(
        entry_id,
        attachment_number,
        source_file.suffix
    )

    shutil.copy2(source_file, full_file_path)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO attachments (entry_id, file_path, file_type, created_at)
            VALUES (?, ?, ?, ?)
        """, (entry_id, str(relative_file_path), file_type, created_at))

        connection.commit()

    return full_file_path


def get_full_attachment_path(relative_file_path):
    assert isinstance(relative_file_path, str)

    return PHOTOS_DIR / relative_file_path


def get_all_entries():
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, created_at, quick_name, status
            FROM entries
            ORDER BY id DESC
        """)

        return cursor.fetchall()