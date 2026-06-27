"""
File: test_database.py
Version: 0.1.0
Purpose: Test SQLite database functions for MobilePartsDB without launching Kivy.
"""

# IMPORTS
from database import initialize_database, create_entry, get_all_entries

# MAIN
def main():
    initialize_database()

    create_entry("MAC valve")
    create_entry("Pressure regulator")
    create_entry("Door cylinder")

    entries = get_all_entries()

    print("\nSaved Entries:")
    print("----------------")

    for entry_id, created_at, quick_name, status in entries:
        print(f"{entry_id}: {quick_name} | {status} | {created_at}")


# PROGRAM START
if __name__ == "__main__":
    main()