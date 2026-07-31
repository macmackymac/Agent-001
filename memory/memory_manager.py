"""
APPA Memory Manager
Handles reading and writing persistent memory.
"""

import json
from pathlib import Path
from datetime import datetime


class MemoryManager:

    BASE_PATH = Path("memory")

    @classmethod
    def load_json(cls, relative_path: str) -> dict:
        path = cls.BASE_PATH / relative_path

        if not path.exists():
            return {}

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def save_json(cls, relative_path: str, data: dict):
        path = cls.BASE_PATH / relative_path

        path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(data, dict):
            data["last_updated"] = datetime.utcnow().isoformat()

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_profile(cls):
        return cls.load_json("user/profile.json")

    @classmethod
    def save_profile(cls, profile: dict):
        cls.save_json("user/profile.json", profile)
