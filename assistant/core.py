"""
Here, the core of our AI assistant.
"""


from typing import List, Any, Dict
from .memory import Memory
from .skills.skill_base import Skill


class Assistant:

    def __init__(self, skills: List[Skill]) -> None:
        self.memory = Memory()
        self.skills = sorted(skills, key=lambda s: getattr(s, "priority", 100))

    def respond(self, user_text: str) -> str:
        text = user_text.strip()
        if not text:
            return "Je n'ai rien reçu. Pouvez-vous reformuler ?"

        # Fast interns commands.
        if text.lower() in {"quit", "exit", "bye", "au revoir"}:
            return "__EXIT__"

        # Search a skill it can be handled.
        for skill in self.skills:
            if skill.can_handle(text):
                return skill.handle(text, self.memory._cache)

        # Fallback if nothing respond.
        return "Je n'ai pas encore cette capacité. Tapez 'help' pour voir les commandes."



