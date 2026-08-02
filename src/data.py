"""Data loading, validation, and preparation utilities."""

from __future__ import annotations

import logging
import re
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

from src.config import COMBINED_DATA_PATH, HEALTHCARE_SEED_PATH, RAW_DATA_DIR

LOGGER = logging.getLogger(__name__)
UCI_SMS_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"


def clean_text(text: str) -> str:
    """Normalize whitespace while preserving wording useful for detection."""
    text = str(text).replace("\x00", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_label(label: str) -> str:
    """Map compatible labels to the project labels."""
    value = str(label).strip().lower()
    if value in {"ham", "legitimate", "legit", "safe"}:
        return "legit"
    if value in {"spam", "smishing", "phishing", "scam", "fraud"}:
        return "scam"
    raise ValueError(f"Unsupported label: {label!r}")


def validate_dataset(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate required columns and remove unusable rows."""
    required = {"text", "label"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Dataset missing columns: {sorted(missing)}")

    validated = frame.copy()
    validated["text"] = validated["text"].map(clean_text)
    validated["label"] = validated["label"].map(normalize_label)
    validated = validated[validated["text"].str.len() >= 8]
    validated = validated.drop_duplicates(subset=["text"]).reset_index(drop=True)
    if validated["label"].nunique() < 2:
        raise ValueError("Dataset must contain both legit and scam examples.")
    return validated


def download_uci_sms_dataset(raw_dir: Path = RAW_DATA_DIR) -> Path | None:
    """Download the UCI SMS Spam Collection if network access is available."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    zip_path = raw_dir / "sms_spam_collection.zip"
    extracted_path = raw_dir / "SMSSpamCollection"
    if extracted_path.exists():
        return extracted_path

    try:
        LOGGER.info("Downloading UCI SMS Spam Collection from %s", UCI_SMS_URL)
        urllib.request.urlretrieve(UCI_SMS_URL, zip_path)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extract("SMSSpamCollection", raw_dir)
        return extracted_path
    except (urllib.error.URLError, zipfile.BadZipFile, OSError) as exc:
        LOGGER.warning("Could not download UCI SMS dataset: %s", exc)
        return None


def load_uci_sms_dataset() -> pd.DataFrame:
    """Load UCI SMS data, returning an empty frame when unavailable."""
    path = download_uci_sms_dataset()
    if path is None or not path.exists():
        return pd.DataFrame(columns=["text", "label", "source"])

    frame = pd.read_csv(path, sep="\t", names=["label", "text"], encoding="utf-8")
    frame["source"] = "UCI SMS Spam Collection"
    return frame[["text", "label", "source"]]


def load_healthcare_seed_dataset(path: Path = HEALTHCARE_SEED_PATH) -> pd.DataFrame:
    """Load the curated healthcare message seed dataset."""
    return pd.read_csv(path)


def build_combined_dataset(output_path: Path = COMBINED_DATA_PATH) -> pd.DataFrame:
    """Combine public SMS spam data with healthcare-focused examples."""
    frames = [load_healthcare_seed_dataset(), load_uci_sms_dataset()]
    combined = pd.concat(frames, ignore_index=True)
    combined = validate_dataset(combined)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(output_path, index=False)
    LOGGER.info("Prepared %s rows at %s", len(combined), output_path)
    return combined


def load_training_data(path: Path = COMBINED_DATA_PATH) -> pd.DataFrame:
    """Load prepared data, building it first if necessary."""
    if not path.exists():
        return build_combined_dataset(path)
    return validate_dataset(pd.read_csv(path))
