import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class Settings:
    """Application settings loaded from environment variables."""

    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DATABASE: str = os.getenv("MONGO_DATABASE", "ecommerce_db")


settings = Settings()
