"""
File: test_database.py
Version: 0.3.0
Purpose: Test SQLite database functions and attachment storage.
"""

# IMPORTS
from pathlib import Path

from MobilePartsDB_v1.app.backend.database import (
    initialize_database,
    create_entry,
    add_attachment_to_entry,
    get_all_entries,
    get_attachments_for_entry,
    FILE_TYPE_IMAGE,
)


# CONSTANTS
TEST_ATTACHMENT_FOLDER = Path("TestAttachments")


# FUNCTIONS
def create_fake_test_file(file_name):
    TEST_ATTACHMENT_FOLDER.mkdir(parents=True, exist_ok=True)

    test_file_path = TEST_ATTACHMENT_FOLDER / file_name
    test_file_path.write_text("Fake test attachment file.", encoding="utf-8")

    return test_file_path


# MAIN
def main():
    initialize_database()

    test_file_1 = create_fake_test_file("test_photo_1.jpg")
    test_file_2 = create_fake_test_file("test_photo_2.jpg")
    test_file_3 = create_fake_test_file("nameplate.png")

    entry_id = create_entry("MAC valve")

    add_attachment_to_entry(entry_id, str(test_file_1), FILE_TYPE_IMAGE)
    add_attachment_to_entry(entry_id, str(test_file_2), FILE_TYPE_IMAGE)
    add_attachment_to_entry(entry_id, str(test_file_3), FILE_TYPE_IMAGE)

    entries = get_all_entries()

    print("\nSaved Entries:")
    print("----------------")

    for entry_id, created_at, quick_name, status in entries:
        print(f"{entry_id}: {quick_name} | {status} | {created_at}")

        attachments = get_attachments_for_entry(entry_id)

        for attachment_id, file_path, file_type, attachment_created_at in attachments:
            print(f"    Attachment {attachment_id}: {file_path} | {file_type}")


# PROGRAM START
if __name__ == "__main__":
    main()