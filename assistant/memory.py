"""
Here, a simple buffer memory in .json is implemented.
"""


import json
from pathlib import Path
from typing import Any, Dict, List


class Memory:
    """
    Represents a memory management system for storing and retrieving data
    persistently in a JSON file.

    This class provides functionality to manage memory by reading and
    writing data to a JSON file. It ensures the persistence of data and
    maintains a cache for quick access.
    """
    def __init__(self, path: str = "memory.json") -> None:
        self.path = Path(path)
        if not self.path.exists():
            self._write_json_memory({"history": [], "counters": {}, "preferences": {}})
        self._cache: Dict[str, Any] = self._read_json_memory()

    def _read_json_memory(self) -> Dict[str, Any]:
        try:
            with self.path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"history": [], "counters": {}, "preferences": {}}

    def _write_json_memory(self, data: Dict[str, Any]):
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # KV classic storage.
    def get(self, key: str, default: Any = None) -> Any:
        return self._cache.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value
        self._write_json_memory(self._cache)

    # History added here.
    def add_history(self, speaker: str, text: strp) -> None:
        entry = {"speaker": speaker, "text": text}
        self._cache.setdefault("history", []).append(entry)
        self._write_json_memory(self._cache)

    def get_history(self, n: int = 10) -> List[Dict[str, str]]:
        return self._cache.get("history", [])[-n:]

    # Counters added here.
    def increment_counter(self, skill_name: str) -> None:
        counters = self._cache.setdefault("counters", {})
        counters[skill_name] = counters.get(skill_name, 0) + 1
        self._write_json_memory(self._cache)

    def get_counter(self, skill_name: str) -> int:
        return self._cache.get("counters", {}).get(skill_name, 0)

    # Preferences added here.
    def set_preference(self, key: str, value: Any) -> None:
        preferences = self._cache.setdefault("preferences", {})
        preferences[key] = value
        self._write_json_memory(self._cache)

    def get_preference(self, key: str, default: Any = None) -> Any:
        return self._cache.get("preferences", {}).get(key, default)









































