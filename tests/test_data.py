import pandas as pd

from src.data import normalize_label, validate_dataset


def test_normalize_label_maps_supported_labels():
    assert normalize_label("ham") == "legit"
    assert normalize_label("phishing") == "scam"
    assert normalize_label("Smishing") == "scam"


def test_validate_dataset_removes_duplicates_and_keeps_classes():
    frame = pd.DataFrame(
        {
            "text": ["Your appointment is confirmed", "Your appointment is confirmed", "Click to verify SSN"],
            "label": ["legit", "legit", "scam"],
        }
    )
    validated = validate_dataset(frame)
    assert len(validated) == 2
    assert set(validated["label"]) == {"legit", "scam"}
