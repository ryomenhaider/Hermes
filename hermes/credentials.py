import json
import os
from pathlib import Path
import logging
from settings import CREDENTIALS_FILE, ensure_hermes_home

logger = logging.getLogger(__name__)

def _read_all():
    
    ensure_hermes_home()
    try:
        content = CREDENTIALS_FILE.read_text().strip()
        return json.loads(content) if content else {}
    except json.JSONDecodeError as e:
        logger.error(f"Error: {e}")
        return {}


def _write_all(data):
    
    CREDENTIALS_FILE.write_text(json.dumps(data, indent=2))
    os.chmod(CREDENTIALS_FILE, 0o600)


def save_credential(service, value):
    
    data = _read_all()
    data[service] = value
    _write_all(data)


def get_credential(service, default=None):
    data = _read_all()
    return data.get(service, default)


def delete_credential(service):
    data = _read_all()
    if service in data:
        del data[service]
        _write_all(data)
        return True
    return False


def list_credentials():
    data = _read_all()
    return list(data.keys())