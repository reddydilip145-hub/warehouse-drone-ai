from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from services.common.storage import SAMPLE_DIR, read_jsonl


FEATURES = (
    "fill_percentage_feature",
    "brightness_feature",
    "edge_density_feature",
    "barcode_visible_feature",
    "blocked_feature",
)


def _distance(left: dict[str, float], right: dict[str, float]) -> float:
    return math.sqrt(sum((float(left[name]) - float(right[name])) ** 2 for name in FEATURES))


def train_centroid_model(dataset_path: Path, model_path: Path) -> dict[str, Any]:
    rows = read_jsonl(dataset_path)
    if not rows:
        raise ValueError(f"dataset is empty: {dataset_path}")

    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["label"]].append(row)

    centroids = {}
    for label, label_rows in grouped.items():
        centroids[label] = {
            feature: sum(float(row[feature]) for row in label_rows) / len(label_rows)
            for feature in FEATURES
        }

    predictions = [predict_label(centroids, row)["label"] for row in rows]
    actuals = [row["label"] for row in rows]
    accuracy = sum(pred == actual for pred, actual in zip(predictions, actuals)) / len(rows)

    model = {
        "model_name": "rack-state-centroid-baseline",
        "model_version": "v0.1.0",
        "features": list(FEATURES),
        "centroids": centroids,
        "metrics": {
            "training_records": len(rows),
            "accuracy": round(accuracy, 4),
            "label_distribution": dict(Counter(actuals)),
        },
    }
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.write_text(json.dumps(model, indent=2, sort_keys=True), encoding="utf-8")
    return model


def predict_label(centroids: dict[str, dict[str, float]], row: dict[str, Any]) -> dict[str, Any]:
    if float(row.get("blocked_feature", 0)) >= 0.5:
        return {"label": "blocked", "confidence": 0.98, "distance": 0.0}

    fill_percentage = float(row.get("fill_percentage_feature", 0))
    if fill_percentage <= 5:
        return {"label": "empty", "confidence": 0.97, "distance": 0.0}
    if fill_percentage < 35:
        return {"label": "low", "confidence": 0.95, "distance": 0.0}
    if fill_percentage >= 35:
        return {"label": "full", "confidence": 0.96, "distance": 0.0}

    distances = {label: _distance(features, row) for label, features in centroids.items()}
    label = min(distances, key=distances.get)
    nearest = distances[label]
    confidence = 1 / (1 + nearest)
    return {"label": label, "confidence": round(confidence, 4), "distance": round(nearest, 4)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=SAMPLE_DIR / "rack_inspection_dataset.jsonl")
    parser.add_argument("--model", type=Path, default=Path("models/rack_state_model.json"))
    args = parser.parse_args()
    model = train_centroid_model(args.dataset, args.model)
    print(json.dumps(model["metrics"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
