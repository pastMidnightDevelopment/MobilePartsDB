"""
File: config.py
Version: 0.1.0
Purpose: Configuration constants for MobilePartsDB.
"""

# IMPORTS
from pathlib import Path

# CONFIGURATION
APP_NAME = "MobilePartsDB"

# CONSTANTS
BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "Database"
PHOTOS_DIR = BASE_DIR / "Photos"

DATABASE_FILE = DATABASE_DIR / "parts.db"

STATUS_NEEDS_INFO = "Needs Info"