import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

FRED_API = os.getenv("FRED_API")
DB_URL = os.getenv("DATABASE_URL")
