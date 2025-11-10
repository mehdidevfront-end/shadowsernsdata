import json
import os
import threading
from typing import Any, Dict, List

_lock = threading.Lock()


def _ensure_dir(path: str):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def read_json(path: str) -> Any:
    if not os.path.exists(path):
        return None
    with _lock:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)


def write_json(path: str, data: Any):
    _ensure_dir(path)
    with _lock:
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)


ASSETS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'backend_data', 'assets.json')
RISKS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'backend_data', 'risks.json')


def list_assets() -> List[Dict]:
    r = read_json(ASSETS_PATH)
    return r or []


def save_assets(items: List[Dict]):
    write_json(ASSETS_PATH, items)


def list_risks() -> List[Dict]:
    r = read_json(RISKS_PATH)
    return r or []


def save_risks(items: List[Dict]):
    write_json(RISKS_PATH, items)
