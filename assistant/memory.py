"""
Here, a simple buffer memory in .json is implemented.
"""


import json
from pathlib import Path
from typing import Any, Dict


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
            self._write_json_memory({})
        self._cache: Dict[str, Any] = self._read_json_memory()

    def _read_json_memory(self) -> Dict[str, Any]:
        try:
            with self.path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _write_json_memory(self, data: Dict[str, Any]):
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        return self._cache.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value
        self._write_json_memory(self._cache)
