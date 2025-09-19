"""
Skill for testing memory of a developer and try to make it easily.
"""


from typing import Any, Dict
from .skill_base import Skill

class CapsSkill(Skill):
    name = "caps"
    description = "Transforme un texte en MAJUSCULES."
    priority = 30

    def can_handle(self, user_text: str) -> bool:
        text = user_text.strip().lower()
        # Simple triggers.
        return text.startswith("caps ") or text.startswith("crie ")

    def handle(self, user_text: str, memory: Dict[str, Any]) -> str:
        entities = memory.get("_router_entities") or {}
        payload = entities.get("payload")
        if not payload:
            # Fallback if direct call without router.
            # Retire keyword and upper().
            text = user_text.strip()
            if text.lower().startswith("caps "):
                payload = text[5:]
            elif text.lower().startswith("crie "):
                payload = text[5:]
            else:
                payload = text
        return payload.upper() if payload else "Que voulez-vous que je mette en majuscules ?"

