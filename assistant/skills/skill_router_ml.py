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


