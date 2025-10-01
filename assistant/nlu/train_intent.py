"""
Here, we train the intent classifier.
"""


import json
from pathlib import Path
from typing import List, Tuple
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix


DATA = Path(__file__).with_name("intent_dataset.json")
MODEL_DIR = Path(__file__).with_name("models")
MODEL_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODEL_DIR / "intent_clf.joblib"

def load_data() -> Tuple[List[str], List[str]]:
    rows = json.loads(DATA.read_text(encoding="utf-8"))
    x = [r["text"] for r in rows]
    y = [r["intent"] for r in rows]
    return x, y

def build_pipeline() -> Pipeline:
    """
    Pipeline = (1) TF-IDF + (2) Logistic Regression
    - TF-IDF transforms text into numeric vectors (words / bigrams.)
    - LogisticRegression learn how to associate a vector with intent.
    """
    return Pipeline(steps=[
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            token_pattern=r"(?u)\b\w+\b",
            ngram_range=(1, 2),
            min_df=1
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            multi_class="auto",
            random_state=42
        ))
    ])

def main() -> None:
    x, y = load_data()

    # Simple split train/test (80/20).
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe = build_pipeline()
    pipe.fit(x_train, y_train)

    # Test set evaluation.
    y_pred = pipe.predict(x_test)
    print("=== Rapport de classification (test) ===")
    print(classification_report(y_test, y_pred, digits=3))
    print("=== Matrice de confusion (test) ===")
    print(confusion_matrix(y_test, y_pred))

    # Save the trained model.
    joblib.dump(pipe, MODEL_PATH)
    print(f"\n Modèle enregistré : {MODEL_PATH}")

    if __name__ == "__main__":
        main()
