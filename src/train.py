"""Train and persist the healthcare scam detector."""

from __future__ import annotations

import argparse
import json
import logging

import joblib

from src.config import METRICS_PATH, MODEL_DIR, MODEL_PATH
from src.data import build_combined_dataset, load_training_data
from src.modeling import train_and_select_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train healthcare scam detector models.")
    parser.add_argument("--rebuild-data", action="store_true", help="Rebuild the combined dataset before training.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s - %(message)s")
    frame = build_combined_dataset() if args.rebuild_data else load_training_data()
    result = train_and_select_model(frame)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(result.estimator, MODEL_PATH)
    payload = {
        "selected_model": result.name,
        "test_metrics": result.test_metrics,
        "comparison": result.comparison.to_dict(orient="records"),
        "rows": int(len(frame)),
        "class_balance": frame["label"].value_counts().to_dict(),
    }
    METRICS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
