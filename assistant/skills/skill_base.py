"""
Here we build the base class for all skills.
"""


from abc import ABC, abstractmethod
from typing import Any, Dict


class Skill(ABC):
    name: str = "base"
    description: str = "Base class for all skills."
    priority: int = 100 # Lower is higher priority.

    @abstractmethod
    def can_handle(self, user_text: str) -> bool:
        """
        Return True if this skill knows how to handle the entry in 'user_text'.
        """
        raise NotImplementedError


    @abstractmethod
    def handle(self, user_text: str, memory: Dict[str, Any]) -> str:
        """
        Process the user text and optionally use memory to return a text response.
        """
        raise NotImplementedError
