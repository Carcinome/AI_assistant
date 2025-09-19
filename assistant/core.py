"""
Here, the core of our AI assistant.
"""


from typing import List, Any, Dict
from datetime import datetime
from .memory import Memory
from .skills.skill_base import Skill
from .permissions import DEFAULT_PERMISSIONS


class Assistant:

    def __init__(self, skills: List[Skill]) -> None:
        self.memory = Memory()
        # Inject permissions by default if it's missing.
        prefs = self.memory._cache.setdefault("preferences", {})
        perms = prefs.setdefault("permissions", {})
        for k, v in DEFAULT_PERMISSIONS.items():
            perms.setdefault(k, v)
        self.memory._write_json_memory(self.memory._cache)

        self.skills = sorted(skills, key=lambda s: getattr(s, "priority", 100))

    def _collect_due_reminders(self) -> List[str]:
        """
        Return and remove due reminders.
        """
        prefs = self.memory._cache.setdefault("preferences", {})
        reminders = prefs.setdefault("reminders", [])
        now = datetime.now()
        due = [r for r in reminders if datetime.fromisoformat(r["when"]) <= now]
        if due:
            # Keep what is not yet due.
            remaining = [r for r in reminders if r not in due]
            prefs["reminders"] = remaining
            self.memory._write_json_memory(self.memory._cache)
        return [f"Rappel : {r['text']} (échéance {r['when']})" for r in due]

    def respond(self, user_text: str) -> str:
        text = user_text.strip()
        if not text:
            return "Je n'ai rien reçu. Pouvez-vous reformuler ?"

        # Save history.
        self.memory.add_history("user", text)

        # Fast interns commands.
        if text.lower() in {"quit", "exit", "bye", "au revoir"}:
            self.memory.add_history("assistant", "Au revoir !")
            return "__EXIT__"

        # Check reminders then before answering.
        notices = self._collect_due_reminders()
        prefix = ("\n".join(notices) + "\n") if notices else ""

        # Search a skill it can be handled.
        for skill in self.skills:
            if skill.can_handle(text):
                reply = skill.handle(text, self.memory._cache)
                self.memory.add_history("assistant", reply)
                self.memory.increment_counter(skill.name)
                return prefix + reply

        reply = prefix + "Je n'ai pas encore cette capacité. Tapez 'help' pour voir les commandes."
        self.memory.add_history("assistant", reply)
        return reply


