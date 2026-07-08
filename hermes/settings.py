import json
import os
from pathlib import Path

HERMES_DIR = Path.home() / ".hermes"
CREDENTIALS_FILE = HERMES_DIR / "credentials.json"
CONFIG_FILE = HERMES_DIR / "config.json"
EXPORTS_DIR = HERMES_DIR / "exports"
CACHE_DIR = HERMES_DIR / "cache"

DEFAULT_CONFIG = {
    "theme": "default",
    "log_level": "info",
}

DEFAULT_CREDENTIALS = {}


def ensure_hermes_home():
    """Create ~/.hermes/ and its contents if they don't already exist."""
    
    HERMES_DIR.mkdir(mode=0o700, exist_ok=True)
    EXPORTS_DIR.mkdir(exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)

    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2))

    if not CREDENTIALS_FILE.exists():
        CREDENTIALS_FILE.write_text(json.dumps(DEFAULT_CREDENTIALS, indent=2))
        os.chmod(CREDENTIALS_FILE, 0o600)  # restrict access, since it holds secrets


def load_config():
    ensure_hermes_home()
    return json.loads(CONFIG_FILE.read_text())


def load_credentials():
    ensure_hermes_home()
    return json.loads(CREDENTIALS_FILE.read_text())


# Run on import so any module that imports settings gets a ready ~/.hermes/
ensure_hermes_home()