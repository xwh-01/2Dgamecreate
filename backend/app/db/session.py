# Database session management (SQLAlchemy)
import json
import os
import threading
from typing import Any, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_lock = threading.Lock()


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _path(name: str) -> str:
    _ensure_data_dir()
    return os.path.join(DATA_DIR, f"{name}.json")


def _load(name: str, default: Any = None) -> Any:
    path = _path(name)
    if not os.path.exists(path):
        return default if default is not None else {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(name: str, data: Any):
    with _lock:
        path = _path(name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)


class JsonStore:
    def __init__(self, collection: str):
        self.collection = collection

    def get_all(self) -> dict:
        return _load(self.collection, {})

    def get(self, key: str) -> Optional[dict]:
        data = self.get_all()
        return data.get(key)

    def set(self, key: str, value: dict):
        data = self.get_all()
        data[key] = value
        _save(self.collection, data)

    def delete(self, key: str) -> bool:
        data = self.get_all()
        if key in data:
            del data[key]
            _save(self.collection, data)
            return True
        return False

    def list_by(self, field: str, value: Any) -> list[dict]:
        data = self.get_all()
        return [v for v in data.values() if v.get(field) == value]


class SessionManager:
    def __init__(self):
        self.projects = JsonStore("projects")
        self.styles = JsonStore("styles")
        self.tasks = JsonStore("tasks")
        self.assets = JsonStore("assets")
        self.exports = JsonStore("exports")


_session_manager: Optional[SessionManager] = None


def get_session() -> SessionManager:
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
