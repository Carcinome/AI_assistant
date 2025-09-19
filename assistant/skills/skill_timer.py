"""
A skill to create, update, and delete reminders.
"""


import re
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from .skill_base import Skill
from ..permissions import is_allowed, USE_TIMER


IN_PATTERN = re.compile(r"remind\s+in\s+(\d+)\s*(s|sec|seconds|m|min|minutes|h|hr|heures?)\s+(.+)", re.IGNORECASE)
AT_PATTERN = re.compile(r"remind\s+at\s+(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s+(.+)", re.IGNORECASE)
LIST_PATTERN = re.compile(r"reminders?\s+list", re.IGNORECASE)
CLEAR_PATTERN = re.compile(r"reminders?\s+clear", re.IGNORECASE)


def _parse_in(n: int, unit: str) -> timedelta:
    unit = unit.lower()
    if unit.startswith("s"):
        return timedelta(seconds=n)
    if unit.startswith("m"):
        return timedelta(minutes=n)
    if unit.startswith("h"):
        return timedelta(hours=n)
    raise ValueError("Unité non supportée.")


class TimerSkill(Skill):
    name = "timer"
    description = "Crée et gère des rappels ('remind in', 'remind at', 'reminders list', 'reminders clear')."
    priority = 28

    def can_handle(self, user_text: str) -> bool:
        t = user_text.strip().lower()
        return t.startswith(("remind ", "reminders "))

    def handle(self, user_text: str, memory: Dict[str, Any]) -> str:
        prefs = memory.setdefault("preferences", {})
        perms = prefs.setdefault("permissions", {})
        if not is_allowed(perms, USE_TIMER):
            return "Permission refusée : les rappels ne sont pas autorisés."

        reminders = prefs.setdefault("reminders", [])

        m = IN_PATTERN.match(user_text)
        if m:
            n = int(m.group(1))
            td = _parse_in(n, m.group(2))
            text = m.group(3).strip()
            when = (datetime.now() + td).isoformat(timespec="minutes")
            reminders.append({"when": when, "text": text.strip()})
            return f"Rappel crée pour {when} : {text}"

        m = AT_PATTERN.match(user_text)
        if m:
            date_s, time_s, text = m.groups()
            when = f"{date_s}T{time_s}"
            try:
                datetime.fromisoformat(when)
            except ValueError:
                return "Format 'remind at YYYY-MM-DD HH:MM <texte>' invalide."
            reminders.append({"when": when, "text": text.strip()})
            return f"Rappel crée pour {when} : {text.strip()}"

        if LIST_PATTERN.match(user_text):
            if not reminders:
                return "Aucun rappel en cours."
            lines = [f"- {r['when']}: {r['text']}"]
            return "Rappels : \n" + "\n".join(lines for lines in [f"- {r['when']}: {r['text']}" for r in reminders])

        if CLEAR_PATTERN.match(user_text):
            prefs["reminders"] = []
            return "Tous les rappels ont été supprimés."

        return "Utilisez : 'remind in 10 min <texte>', 'remind at YYYY-MM-DD HH:MM <texte>', 'reminders list', 'reminders clear'."





