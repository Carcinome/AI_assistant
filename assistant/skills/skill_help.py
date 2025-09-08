"""
For helping users to use the assistant.
"""


from typing import Any, Dict
from .skill_base import Skill


class HelpSkill(Skill):
    name = "help"
    description = "Liste des commandes disponibles."

    def __init__(self, skill_registry: Dict[str, str]) -> None:
        self.registry = skill_registry

    def can_handle(self, user_text: str) -> bool:
        return user_text.lower() in {"help", "aide", "?"}

    def handle(self, user_text: str, memory: Dict[str, Any]) -> str:
        lines = ["Capacités disponibles :"]
        for skill_name, desc in self.registry.items():
            lines.append(f"- {skill_name}: {desc}")
        lines.append("Pressez 'quit' pour quitter.")
        return "\n".join(lines)

