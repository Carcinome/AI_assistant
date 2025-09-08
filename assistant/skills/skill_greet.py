"""
Skill for learn first name and salute.
"""


import re
from typing import Any, Dict, Optional
from .skill_base import Skill


class GreetSkill(Skill):
    name = "greet"
    description = "Salue l'utilisateur et apprend/retiens son prénom."
    priority = 10 # After the router but before other skills if needed.

    def can_handle(self, user_text: str) -> bool:
        # Can make direct trigger, without the router.
        text = user_text.lower()
        return any(w in text for w in ["greet", "greeting", "bonjour", "salut", "coucou", "hello"])

    def _extract_name_from_router(self, memory: Dict[str, Any]) -> Optional[str]:
        entities = memory.get("_router_entities") or {}
        # The router can give 'name' if the user tells 'my name is X'.
        name = entities.get("name")
        if isinstance(name, str):
            return name.strip().capitalize()
        return None

    def _extract_name_inline(self, user_text: str) -> Optional[str]:
        # Fallback if the router doesn't give a name.
        m = re.search(r"je m'appelle|je me nomme\s+([A-Za-zÀ-ÖØ-öø-ÿ\-]+)", user_text, re.IGNORECASE)
        if m:
            return m.group(2).strip().capitalize()
        return None

    def handle(self, user_text: str, memory: Dict[str, Any]) -> str:
        # Return the name from the router or indirectly.
        name = self._extract_name_from_router(memory) or self._extract_name_inline(user_text)
        if name:
            memory["user_name"] = name

        stored = memory.get("user_name")
        if stored:
            return f"Bonjour {stored} !"
        return "Bonjour ! Quel est votre prénom ? (Vous pouvez dire : 'Je m'appelle <VotrePrenom>')"

