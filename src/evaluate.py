"""Evaluate the saved healthcare scam detector."""

from __future__ import annotations

import json

import joblib
from sklearn.metrics import classification_report, confusion_matrix

from src.config import MODEL_PATH
from src.data import load_training_data


def main() -> None:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run python -m src.train first.")
    model = joblib.load(MODEL_PATH)
    frame = load_training_data()
    predictions = model.predict(frame["text"])
    output = {
        "classification_report": classification_report(frame["label"], predictions, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(frame["label"], predictions, labels=["legit", "scam"]).tolist(),
        "labels": ["legit", "scam"],
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
