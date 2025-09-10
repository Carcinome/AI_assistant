"""
To manage and write a little task list.
"""


import re
from typing import Any, Dict
from .skill_base import Skill


class TodoSkill(Skill):
    name = "todo"
    description = "Gère une petite liste de tâches."
    priority = 30

    def can_handle(self, user_text: str) -> bool:
        text = user_text.lower()
        return text.startswith("todo") or "tâche" in text

    def handle(self, user_text: str, memory: Dict[str, Any]) -> str:
        preferences = memory.setdefault("preferences", {})
        todos = preferences.setdefault("todos", [])

        # To add a task.
        m_add = re.match(r"todo\s+ajouter\s+(.+)", user_text, re.IGNORECASE)
        if m_add:
            task = m_add.group(1).strip()
            todos.append(task)
            return f"Tâche ajoutée: {task}."

        # Listing of tasks.
        if "liste" in user_text.lower():
            if not todos:
                return "Votre liste de tâches est vide."
            return "Vos tâches :\n- " + "\n- ".join(todos)

        # Delete a task.
        m_del = re.match(r"todo\s+supprimer\s+(.+)", user_text, re.IGNORECASE)
        if m_del:
            task = m_del.group(1).strip()
            if task in todos:
                todos.remove(task)
                return f"Tâche supprimée : {task}."
            return f"La tâche '{task}' n'est pas dans votre liste."

        return "Utilisez 'todo ajouter <texte>', 'todo liste' ou 'todo supprimer <texte>'."