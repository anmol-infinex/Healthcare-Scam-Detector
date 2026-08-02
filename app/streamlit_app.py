"""Streamlit app for the healthcare scam detector."""

from __future__ import annotations

import html
import sys
from pathlib import Path

import joblib
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import MODEL_PATH, SUSPICIOUS_KEYWORDS
from src.modeling import predict_with_confidence
from src.predict import explain_prediction, suspicious_terms


def load_model():
    if not MODEL_PATH.exists():
        st.error("Model file is missing. Run `python -m src.train --rebuild-data` first.")
        st.stop()
    return joblib.load(MODEL_PATH)


def highlight_terms(text: str, terms: list[str]) -> str:
    safe = html.escape(text)
    for term in sorted(terms, key=len, reverse=True):
        safe = safe.replace(html.escape(term), f"<mark>{html.escape(term)}</mark>")
        safe = safe.replace(html.escape(term.title()), f"<mark>{html.escape(term.title())}</mark>")
    return safe


st.set_page_config(page_title="Healthcare Scam Detector", page_icon="H", layout="centered")
st.title("Healthcare Scam Detector")
st.caption("Classifies healthcare SMS, emails, and messages as legitimate or scam/phishing.")

if "history" not in st.session_state:
    st.session_state.history = []

message = st.text_area(
    "Message",
    height=180,
    placeholder="Paste a healthcare-related SMS, email, or portal message...",
)

col_a, col_b = st.columns([1, 1])
predict_clicked = col_a.button("Analyze", type="primary", use_container_width=True)
clear_clicked = col_b.button("Clear History", use_container_width=True)

if clear_clicked:
    st.session_state.history = []

if predict_clicked and message.strip():
    model = load_model()
    result = predict_with_confidence(model, message)
    terms = suspicious_terms(message)
    result["suspicious_terms"] = terms
    result["explanation"] = explain_prediction(message, result["label"], terms)
    st.session_state.history.insert(0, {"message": message, **result})

if st.session_state.history:
    latest = st.session_state.history[0]
    label = "Scam / Phishing" if latest["label"] == "scam" else "Legitimate"
    st.metric("Prediction", label, f"{latest['confidence']:.1%} confidence")
    st.progress(latest["scam_probability"], text=f"Scam probability: {latest['scam_probability']:.1%}")
    st.write(latest["explanation"])
    if latest["suspicious_terms"]:
        st.markdown("Suspicious terms: " + ", ".join(f"`{term}`" for term in latest["suspicious_terms"]))
    st.markdown(highlight_terms(latest["message"], latest["suspicious_terms"]), unsafe_allow_html=True)

    st.subheader("Prediction History")
    for item in st.session_state.history[:10]:
        st.write(
            f"**{'Scam / Phishing' if item['label'] == 'scam' else 'Legitimate'}** "
            f"({item['confidence']:.1%}) - {item['message'][:120]}"
        )
else:
    st.info("Enter a message and click Analyze.")
