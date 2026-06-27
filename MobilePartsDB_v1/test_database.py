"""
File: test_database.py
Version: 0.2.1
Purpose: Test SQLite database functions and automatic photo storage.
"""

# IMPORTS
from pathlib import Path

from database import (
    initialize_database,
    create_entry,
    add_photo_to_entry,
    get_all_entries,
    get_photos_for_entry,
)


# CONSTANTS
TEST_PHOTO_FOLDER = Path("TestPhotos")


# FUNCTIONS
def create_fake_test_photo(file_name):
    TEST_PHOTO_FOLDER.mkdir(parents=True, exist_ok=True)

    test_photo_path = TEST_PHOTO_FOLDER / file_name
    test_photo_path.write_text("Fake test photo file.", encoding="utf-8")

    return test_photo_path


# MAIN
def main():
    initialize_database()

    test_photo_1 = create_fake_test_photo("test_photo_1.jpg")
    test_photo_2 = create_fake_test_photo("test_photo_2.jpg")
    test_photo_3 = create_fake_test_photo("nameplate.png")

    entry_id = create_entry("MAC valve")

    add_photo_to_entry(entry_id, str(test_photo_1))
    add_photo_to_entry(entry_id, str(test_photo_2))
    add_photo_to_entry(entry_id, str(test_photo_3))

    entries = get_all_entries()

    print("\nSaved Entries:")
    print("----------------")

    for entry_id, created_at, quick_name, status in entries:
        print(f"{entry_id}: {quick_name} | {status} | {created_at}")

        photos = get_photos_for_entry(entry_id)

        for photo_id, photo_path, photo_created_at in photos:
            print(f"    Photo {photo_id}: {photo_path}")


# PROGRAM START
if __name__ == "__main__":
    main()