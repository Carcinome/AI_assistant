"""
A little tool for asking 'what time is it?'
"""


from datetime import datetime
from typing import Any, Dict
from .skill_base import Skill


class TimeSkill(Skill):
    name = "time"
    description = "Donne l'heure actuelle."

    def can_handle(self, user_text: str) -> bool:
        text = user_text.lower()
        triggers = {
            "quelle heure",
            "donne l'heure",
            "il est quelle heure",
            "time",
            "Alfred, donne l'heure",
            "heure"
        }
        return any(t in text for t in triggers)

    def handle(self, user_text: str, memory: dict[str, Any]) -> str:
        now = datetime.now()
        return f"Il est {now:%Hh%M}."
