"""Command-line inference for healthcare scam detection."""

from __future__ import annotations

import argparse
import json

import joblib

from src.config import MODEL_PATH, SUSPICIOUS_KEYWORDS
from src.modeling import predict_with_confidence


def suspicious_terms(text: str) -> list[str]:
    """Return suspicious healthcare scam indicators found in text."""
    lowered = text.lower()
    return sorted({term for term in SUSPICIOUS_KEYWORDS if term in lowered})


def explain_prediction(text: str, label: str, terms: list[str]) -> str:
    if label == "scam":
        if terms:
            return "The message contains pressure, identity, payment, or credential patterns commonly found in healthcare scams."
        return "The wording resembles known spam or phishing patterns from the training set."
    if terms:
        return "The model judged the message legitimate overall, but the highlighted terms deserve manual verification."
    return "The message does not contain common scam indicators and resembles routine healthcare communication."


def main() -> None:
    parser = argparse.ArgumentParser(description="Predict whether a healthcare message is legitimate or scam.")
    parser.add_argument("message", help="Message text to classify.")
    args = parser.parse_args()

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run python -m src.train first.")
    model = joblib.load(MODEL_PATH)
    result = predict_with_confidence(model, args.message)
    terms = suspicious_terms(args.message)
    result["suspicious_terms"] = terms
    result["explanation"] = explain_prediction(args.message, result["label"], terms)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
