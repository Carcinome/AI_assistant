"""
A little tool for asking 'what time is it?'
"""


from datetime import datetime
from typing import Any, Dict
from .skill_base import Skill


class TimeSkill(Skill):
    name = "time"
    description = "Donne l'heure actuelle (et la date si demandé)."
    priority = 20

    def can_handle(self, user_text: str) -> bool:
        text = user_text.lower()
        triggers = {
            "quelle heure",
            "donne l'heure",
            "il est quelle heure",
            "time",
            "Alfred, donne l'heure",
            "heure",
            "date",
            "quel jour",
        }
        return any(t in text for t in triggers)

    def handle(self, user_text: str, memory: dict[str, Any]) -> str:
        now = datetime.now()
        text = user_text.lower()
        if "date" in text or "jour" in text:
            return f"Nous sommes le {now:%d/%m/%Y}."
        return f"Il est {now:%H:%M}."
