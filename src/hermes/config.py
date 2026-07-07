import os
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

FRED_API = os.getenv("FRED_API")


def normalize_db_url(raw_url: str | None) -> str | None:
    if not raw_url:
        return None
    if raw_url.startswith(("http://", "https://")):
        return None

    try:
        parts = urlsplit(raw_url)
    except ValueError:
        return raw_url

    if not parts.hostname:
        return raw_url

    if parts.password:
        encoded_password = quote(parts.password, safe="%")
        userinfo = parts.username or ""
        if userinfo:
            userinfo = f"{userinfo}:{encoded_password}"
        else:
            userinfo = encoded_password
        netloc = f"{userinfo}@{parts.hostname}"
        if parts.port:
            netloc = f"{netloc}:{parts.port}"
        return urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))

    return raw_url


# Supabase is the source of truth for Hermes data.
SUPABASE_DB_URL = normalize_db_url(
    os.getenv("SUPABASE_DB_URL")
    or os.getenv("DIRECT_URL")
    or os.getenv("DATABASE_URL")
)
DB_URL = SUPABASE_DB_URL

ACLED_EMAIL=os.getenv("ACLED_EMAIL")
ACLED_PASSWORD=os.getenv("ACLED_PASSWORD")

HOST=os.getenv("HOST")
PORT=os.getenv("PORT")
ENV=os.getenv("ENV")


SUPABASE_KEY=os.getenv('SUPABASE_KEY')

SUPABASE_PUBLISHABLE_KEY=os.getenv('SUPABASE_PUBLISHABLE_KEY')
SUPABASE_SECRET_KEY=os.getenv('SUPABASE_SECRET_KEY')
SUPABASE_JWKS_URL=os.getenv('SUPABASE_JWKS_URL')