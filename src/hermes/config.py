import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

FRED_API = os.getenv("FRED_API")
DB_URL = os.getenv("DATABASE_URL")

ACLED_EMAIL=os.getenv("ACLED_EMAIL")
ACLED_PASSWORD=os.getenv("ACLED_PASSWORD")

HOST=os.getenv("HOST")
PORT=os.getenv("PORT")
ENV=os.getenv("ENV")