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

