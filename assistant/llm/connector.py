from dataclasses import dataclass
from typing import Optional, Dict, Any, List

@dataclass
class LLMConfig:
    provider: str = "disabled" # "disabled" | "openai" | "other"
    model: str = "" # Nom du modèle si provider actif.
    max_tokens: int = 256 # Borne dure de sortie
    temperature: float = 0.2 # Sortie plutôt stable.
    api_key_env: str = "OPENAI_API_KEY" # Nom de la variable d'environnement.

class BaseLLM:
    def __init__(self, cfg: LLMConfig) -> None:
        self.cfg = cfg

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        # Minimal behavior: return short and careful reformulation.
        # We cut properly if it's too long.
        text = prompt.strip()
        if len(text) > 300:
            text = text[:300] + "..."
        return f"[LLM Désactivé] Reformulation prudente: {text}"

def buil_llm(cfg: LLMConfig) -> BaseLLM:
    if cfg.provider == "disabled":
        return DisabledLLM(cfg)
