"""
Here, a secure file manager.
"""


import os
from pathlib import Path
from typing import Any, Dict
from .skill_base import Skill
from ..permissions import is_allowed, READ_FS, WRITE_FS


SAFE_DIR = Path("workspace").resolve()


def _ensure_workspace() -> None :
    SAFE_DIR.mkdir(parents=True, exist_ok=True)

def _safe_path(name: str) -> Path:
    # Deny the suspects relative paths and normalize it.
    p = (SAFE_DIR / name).resolve()
    if not str(p).startswith(str(SAFE_DIR)):
        raise ValueError("Chemin en dehors du dossier sécurisé.")
    return p


class FileSkill(Skill):
    name = "files"
    description = "Lit et écrit des fichiers dans un dossier sécurisé."
    priority = 35

    def can_handle(self, user_text: str) -> bool:
        t = user_text.strip().lower()
        return t.startswith("file ") or t.startswith("fichier ")

    def handle(self, user_text: str, memory: Dict[str, Any]) -> str:
        _ensure_workspace()
        prefs = memory.setdefault("preferences", {})
        perms = prefs.setdefault("permissions", {})

        parts = user_text.strip().split(maxsplit=2)
        if len(parts) < 2:
            return ("Utilisez 'file list' ou 'file read(lecture) <nom>' pour voir les fichiers, "
                    "ou encore 'file write(écriture) <nom> <texte> pour les éditer.")

        cmd = parts[1].lower()
        if cmd == "list":
            if not is_allowed(perms, READ_FS):
                return "Vous n'avez pas la permission de lire le dossier."
            files = [p.name for p in SAFE_DIR.iterdir() if p.is_file()]
            return "workspace/ :\n- " + "\n- ".join(files) if files else "Aucun fichier."

        if cmd == "read" or "lecture":
            if not is_allowed(perms, READ_FS):
                return "Vous n'avez pas la permission de lire le dossier."
            if len(parts) < 3:
                return "Utilisez 'file read <nom>' ou 'file lecture <nom>' pour lire un fichier."
            path = _safe_path(parts[2])
            if not path.exists():
                return f"Le fichier '{path}' n'existe pas."
            return path.read_text(encoding="utf-8")

        if cmd == "write" or "écriture":
            if not is_allowed(perms, READ_FS):
                return "Vous n'avez pas la permission de lire le dossier."
            if len(parts) < 3:
                return "Utilisez 'file write <nom> <texte>' ou 'file écriture <nom> <texte>' pour éditer un fichier."
            # Cutting: name + text.
            rest = parts[2].split(maxsplit=1)
            if len(rest) < 2:
                return "Précisez le texte à écrire : 'file write (ou écriture) <nom> <texte>'."
            name, content = rest[0], rest[1]
            path = _safe_path(name)
            path.write_text(content, encoding="utf-8")
            return f"Ecriture dans {path.name}."

        return "Commande : 'file list', 'file read (ou lecture) <nom>' ou 'file write (ou écriture) <nom> <texte>'."


