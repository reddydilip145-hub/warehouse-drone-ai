from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ml.src.train import predict_label


def load_model(model_path: Path) -> dict[str, Any]:
    return json.loads(model_path.read_text(encoding="utf-8"))


def infer_rack_state(model: dict[str, Any], features: dict[str, Any]) -> dict[str, Any]:
    prediction = predict_label(model["centroids"], features)
    label = prediction["label"]
    return {
        "fill_state": label,
        "fill_percentage": float(features.get("fill_percentage_feature", 0)),
        "confidence_score": prediction["confidence"],
        "exception_type": None if label == "full" else f"{label}_location",
        "model_version_id": model["model_version"],
    }

