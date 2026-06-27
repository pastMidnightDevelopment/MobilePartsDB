"""
File: reset_database.py
Version: 0.1.0
Purpose: Reset the MobilePartsDB test database during development.
"""

# IMPORTS
from MobilePartsDB_v1.app.backend.config import DATABASE_FILE
from MobilePartsDB_v1.app.backend.database import initialize_database

# FUNCTIONS
def reset_database():
    if DATABASE_FILE.exists():
        DATABASE_FILE.unlink()

    initialize_database()
    print("Database reset complete.")


# PROGRAM START
if __name__ == "__main__":
    reset_database()