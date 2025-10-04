from pathlib import Path
from typing import Any, Dict, Optional, List, Tuple
import joblib
import numpy as np
import re


from .skill_base import Skill

class MLIntentRouterSkill(Skill):
    name = "router_ml"
    description = "Routeur d'intentions (fallback ML) avec seuil de confiance."
    priority = 5

    def __init__(self, intent_map: Dict[str, Skill], model_path: str = "nlu/models/intent_clf.joblib",
                                                                        confidence_threshold: float = 0.55) -> None:
        """
        intent_map: dict |intent_label: skill_instance|
        model_path: Path of the trained joblib model.
        confidence_threshold: Minimum confidence level to consider the intent as valid.
        """
        self.intent_map = intent_map
        self.model_path = Path(model_path)
        self.model = joblib.load(self.model_path) if self.model_path.exists() else None
        self.labels_: Optional[List[str]] = None
        self.confidence_threshold = confidence_threshold

        # Trying to return known labels from the model.
        if self.model is not None and hasattr(self.model, "classes_"):
            self.labels_ = list(self.model.classes_)

        # Mini normalizations (ex: usual variants).
        self._normalize: List[Tuple[re.Pattern, str]] = [
            (re.compile(r"\bil est quelle heure\b", re.IGNORECASE), "il est quelle heure"),
            (re.compile(r"\bquelle est la date du jour\b", re.IGNORECASE), "quelle est la date du jour")
        ]

    def can_handle(self, user_text: str) -> bool:
            # ML fallback is 'available' if one model is loaded.
            return self.model is not None

    def _normalize_text(self, text: str) -> str:
            out = text.strip()
            for pat, rep in self._normalize:
                out = pat.sub(rep, out)
            return out

    def handle(self, user_text: str, memory: Dict[str, Any]) -> str:
        if not self.model:
                return "Le routeur ML n'est pas disponible."

        text = self._normalize_text(user_text)

        # Class probability (if available).
        proba = None
        if hasattr(self.model, "predict_proba"):
            proba = self.model.predict_proba([text])[0] # np.array shape.
            best_idx = int(np.argmax(proba))
            best_lable = self.model.classes_[best_idx]
            best_conf = float(proba[best_idx])
        else:
            # No probability fallback.
            best_label = self.model.predict([text])[0]
            best_conf = 1.0
            proba = None

        # Memory track for debug and improvement.
        memory["last_intent_ml"] = best_label
        memory["last_intent_confidence"] = round(best_conf, 3)

        # Trust level.
        if best_conf < self.confidence_threshold:
            return (
                "Je ne suis pas assez sûr de votre intention. (confiance "
                f"{best_conf:.2f} < {self.confidence_threshold:.2f})."
                "Pouvez-vous reformuler ou taper 'help' ?"
            )

        # Skill delegation.
        target = self.intent_map.get(best_label)
        if target is None:
            return (
                f"J'ai reconnu l'intention '{best_label}' (confiance {best_conf:.2f}), "
                "mais je n'ai pas la compétence correspondante."
            )

        return target.handle(user_text, memory)



