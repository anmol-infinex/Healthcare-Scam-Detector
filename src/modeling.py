"""Training and inference helpers for the classifier."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from src.config import RANDOM_STATE, SCAM_RECALL_PRIORITY_WEIGHT


@dataclass(frozen=True)
class TrainResult:
    """Container for a trained model and its metrics."""

    name: str
    estimator: Pipeline
    test_metrics: dict[str, float]
    comparison: pd.DataFrame


def _candidate_models() -> dict[str, tuple[Pipeline, dict[str, list[Any]]]]:
    vectorizer = TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2), min_df=1)
    return {
        "logistic_regression": (
            Pipeline(
                [
                    ("tfidf", vectorizer),
                    (
                        "classifier",
                        LogisticRegression(
                            max_iter=2000,
                            class_weight={"legit": 1.0, "scam": SCAM_RECALL_PRIORITY_WEIGHT},
                            random_state=RANDOM_STATE,
                        ),
                    ),
                ]
            ),
            {"classifier__C": [0.5, 1.0, 2.0]},
        ),
        "multinomial_nb": (
            Pipeline([("tfidf", vectorizer), ("classifier", MultinomialNB())]),
            {"classifier__alpha": [0.2, 0.5, 1.0]},
        ),
        "linear_svm": (
            Pipeline(
                [
                    ("tfidf", vectorizer),
                    (
                        "classifier",
                        LinearSVC(class_weight={"legit": 1.0, "scam": SCAM_RECALL_PRIORITY_WEIGHT}, random_state=RANDOM_STATE),
                    ),
                ]
            ),
            {"classifier__C": [0.5, 1.0, 2.0]},
        ),
        "random_forest": (
            Pipeline(
                [
                    ("tfidf", vectorizer),
                    (
                        "classifier",
                        RandomForestClassifier(
                            n_estimators=120,
                            class_weight={"legit": 1.0, "scam": SCAM_RECALL_PRIORITY_WEIGHT},
                            random_state=RANDOM_STATE,
                        ),
                    ),
                ]
            ),
            {"classifier__max_depth": [None, 12]},
        ),
    }


def _score_predictions(model: Pipeline, texts: pd.Series, labels: pd.Series) -> dict[str, float]:
    predictions = model.predict(texts)
    metrics = {
        "accuracy": accuracy_score(labels, predictions),
        "precision_scam": precision_score(labels, predictions, pos_label="scam", zero_division=0),
        "recall_scam": recall_score(labels, predictions, pos_label="scam", zero_division=0),
        "f1_scam": f1_score(labels, predictions, pos_label="scam", zero_division=0),
    }
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(texts)
        scam_index = list(model.classes_).index("scam")
        metrics["roc_auc"] = roc_auc_score(labels, probabilities[:, scam_index])
    elif hasattr(model, "decision_function"):
        metrics["roc_auc"] = roc_auc_score(labels, model.decision_function(texts))
    return {key: float(value) for key, value in metrics.items()}


def train_and_select_model(frame: pd.DataFrame) -> TrainResult:
    """Train candidate models and select by scam recall first, then F1."""
    train_x, test_x, train_y, test_y = train_test_split(
        frame["text"],
        frame["label"],
        test_size=0.2,
        stratify=frame["label"],
        random_state=RANDOM_STATE,
    )
    min_class_count = int(train_y.value_counts().min())
    folds = max(2, min(5, min_class_count))
    cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=RANDOM_STATE)

    rows: list[dict[str, float | str]] = []
    best_name = ""
    best_model: Pipeline | None = None
    best_rank = (-1.0, -1.0, -1.0)

    for name, (pipeline, grid) in _candidate_models().items():
        search = GridSearchCV(pipeline, grid, cv=cv, scoring="recall_macro", n_jobs=-1, error_score="raise")
        search.fit(train_x, train_y)
        model = search.best_estimator_
        metrics = _score_predictions(model, test_x, test_y)
        row = {"model": name, "cv_recall_macro": float(search.best_score_), **metrics}
        rows.append(row)
        rank = (metrics["recall_scam"], metrics["f1_scam"], metrics["accuracy"])
        if rank > best_rank:
            best_name = name
            best_model = model
            best_rank = rank

    if best_model is None:
        raise RuntimeError("No model was trained.")

    comparison = pd.DataFrame(rows).sort_values(["recall_scam", "f1_scam", "accuracy"], ascending=False)
    return TrainResult(best_name, best_model, _score_predictions(best_model, test_x, test_y), comparison)


def predict_with_confidence(model: Pipeline, text: str) -> dict[str, Any]:
    """Predict label and confidence for a single message."""
    prediction = str(model.predict([text])[0])
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([text])[0]
        confidence = float(np.max(probabilities))
        scam_probability = float(probabilities[list(model.classes_).index("scam")])
    elif hasattr(model, "decision_function"):
        score = float(model.decision_function([text])[0])
        scam_probability = float(1.0 / (1.0 + np.exp(-score)))
        confidence = scam_probability if prediction == "scam" else 1.0 - scam_probability
    else:
        confidence = 1.0
        scam_probability = 1.0 if prediction == "scam" else 0.0
    return {"label": prediction, "confidence": confidence, "scam_probability": scam_probability}
