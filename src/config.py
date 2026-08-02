"""Project configuration."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODEL_DIR = PROJECT_ROOT / "models"

HEALTHCARE_SEED_PATH = PROCESSED_DATA_DIR / "healthcare_seed_messages.csv"
COMBINED_DATA_PATH = PROCESSED_DATA_DIR / "combined_messages.csv"
MODEL_PATH = MODEL_DIR / "healthcare_scam_detector.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"

RANDOM_STATE = 42
SCAM_RECALL_PRIORITY_WEIGHT = 2.0

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
}
