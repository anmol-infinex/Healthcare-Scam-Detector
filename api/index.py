"""Vercel Python Function for healthcare scam inference."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from flask import Flask, jsonify, request

app = Flask(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "healthcare_scam_detector.joblib"
MODEL_PATH = Path(os.environ.get("MODEL_PATH", DEFAULT_MODEL_PATH))

SUSPICIOUS_KEYWORDS = {
    "urgent",
    "verify",
    "password",
    "ssn",
    "social security",
    "bank",
    "claim",
    "refund",
    "medicare card",
    "medicaid",
    "insurance suspended",
    "click",
    "link",
    "gift card",
    "otp",
    "one time password",
    "account locked",
    "billing problem",
    "free test",
    "limited time",
    "confirm identity",
    "routing number",
    "credit card",
}

_MODEL: Any | None = None


def load_model() -> Any:
    """Load the trained model once per warm serverless function."""
    global _MODEL
    if _MODEL is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        _MODEL = joblib.load(MODEL_PATH)
    return _MODEL


def suspicious_terms(text: str) -> list[str]:
    """Return suspicious scam indicators found in the submitted message."""
    lowered = text.lower()
    return sorted({term for term in SUSPICIOUS_KEYWORDS if term in lowered})


def explain_prediction(label: str, terms: list[str]) -> str:
    """Create a concise explanation for the UI."""
    if label == "scam":
        if terms:
            return "The message contains urgency, identity, payment, credential, or link patterns often used in healthcare scams."
        return "The wording resembles scam or phishing messages learned by the classifier."
    if terms:
        return "The model judged the message legitimate overall, but the highlighted terms should still be verified through official channels."
    return "The message resembles routine healthcare communication and does not contain common scam indicators."


def predict_payload(text: str) -> dict[str, Any]:
    """Run model inference and return a JSON-safe payload."""
    model = load_model()
    label = str(model.predict([text])[0])
    terms = suspicious_terms(text)

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([text])[0]
        classes = list(model.classes_)
        scam_probability = float(probabilities[classes.index("scam")])
        confidence = float(np.max(probabilities))
    elif hasattr(model, "decision_function"):
        score = float(model.decision_function([text])[0])
        scam_probability = float(1.0 / (1.0 + np.exp(-score)))
        confidence = scam_probability if label == "scam" else 1.0 - scam_probability
    else:
        scam_probability = 1.0 if label == "scam" else 0.0
        confidence = 1.0

    return {
        "label": label,
        "display_label": "Scam / Phishing" if label == "scam" else "Legitimate",
        "confidence": round(confidence, 6),
        "scam_probability": round(scam_probability, 6),
        "suspicious_terms": terms,
        "explanation": explain_prediction(label, terms),
    }


@app.get("/api/health")
@app.get("/health")
def health():
    return jsonify({"ok": True, "model": MODEL_PATH.name})


@app.post("/api/predict")
@app.post("/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    text = str(payload.get("message", "")).strip()
    if not text:
        return jsonify({"error": "Message is required."}), 400
    if len(text) > 5000:
        return jsonify({"error": "Message is too long. Please keep it under 5000 characters."}), 413
    return jsonify(predict_payload(text))


@app.get("/api")
@app.get("/")
def root():
    return jsonify({"service": "Healthcare Scam Detector API", "endpoints": ["/api/health", "/api/predict"]})


handler = app
