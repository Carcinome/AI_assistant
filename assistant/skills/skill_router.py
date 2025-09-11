"""
Make some routes for regex and intent labels.
"""


import re
from typing import Any, Dict, Optional, Pattern, Tuple
from .skill_base import Skill


class RegexIntentRouterSkill(Skill):
    name = "router"
    description = "Route les requêtes vers l'intention correspondante via des regex."
    priority = 0

    def __init__(self, intent_map: Dict[str, Skill]) -> None:
        """
        intent_map: Dictionary with intent names as keys and Skill objects as values.
                 {intent_label: skill_instance}
        Examples: {"greet": GreetSkill(), "time": TimeSkill()}
        """
        self.intent_map = intent_map
        # List (pattern, intent_label).
        self._patterns: List[Tuple[Pattern[str], str]] = [
            (re.compile(r"\b(onjour|salut|coucou|hello)\b", re.IGNORECASE), "greet"),
            (re.compile(r"\b(je m'appelle|je me nomme)\s+(?P<name>[A-Za-zÀ-ÖØ-öø-ÿ\-]+)", re.IGNORECASE), "greet"),
            # Hour/date.
            (re.compile(r"\b(heure|il est quelle heure|time)\b", re.IGNORECASE), "time"),
            (re.compile(r"\b(date du jour|quelle date|on est quel jour)\b", re.IGNORECASE), "time"),
            # Help.
            (re.compile(r"\b(help|\?|aide)\b", re.IGNORECASE), "help"),
        ]
        self._patterns += [
            # Caps (for testing).
            (re.compile(r"^\s*caps\s+(?P<payload>.+)$", re.IGNORECASE), "caps"),
            (re.compile(r"^\s*crie\s+(?P<payload>.+)$", re.IGNORECASE), "caps"),
        ]

    def can_handle(self, user_text: str) -> bool:
        text = user_text.strip()
        if not text:
            return False
        return any(p.search(text) for p, _ in self._patterns)

    def _match_intent(self, text: str) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Return (intent_label, entities) if founded. If not, (None, {}).
        """
        for pattern, intent in self._patterns:
            m = pattern.search(text)
            if m:
                # Extract grouped names.
                entities = m.groupdict() if m.groupdict() else {}
                return intent, entities
        return None, {}

    def handle(self, user_text: str, memory: Dict[str, Any]) -> str:
        intent, entities = self._match_intent(user_text)
        if intent is None:
            return "Je n'ai pas reconnu votre demande. Tapez 'help' pour voir ce que je sais faire."

        # Keep things in memory (useful for debug and evolution).
        memory["last_intent"] = intent
        memory["last_entities"] = entities

        # Delegate to the corresponding skill if it exists.
        target = self.intent_map.get(intent)
        if target is None:
            return f"Je reconnais l'intention '{intent}', mais je n'ai pas encore la compétence nécessaire pour accéder à cette requête."

        # Some skills (ex: Greet) need entities (ex: name).
        memory["_router_entities"] = entities # Reserved space for the router.
        try:
            return target.handle(user_text, memory)
        finally:
            memory.pop("_router_entities", None)
