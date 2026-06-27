from pathlib import Path
from app.backend.database import initialize_database

BASE_DIR = Path(__file__).resolve().parents[1]
DATABASE_DIR = BASE_DIR / "Database"
PHOTOS_DIR = BASE_DIR / "Photos"


def setup_first_launch():
    DATABASE_DIR.mkdir(exist_ok=True)
    PHOTOS_DIR.mkdir(exist_ok=True)
    initialize_database()