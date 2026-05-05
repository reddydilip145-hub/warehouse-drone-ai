from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ml.src.inference import infer_rack_state


class PredictionRequest(BaseModel):
    instances: list[dict[str, Any]]


app = FastAPI(title="Warehouse Drone AI Vertex Predictor")
_MODEL: dict[str, Any] | None = None


def _download_gcs_model(storage_uri: str, target_dir: Path) -> Path:
    from google.cloud import storage

    if not storage_uri.startswith("gs://"):
        raise ValueError(f"unsupported model URI: {storage_uri}")

    bucket_name, _, prefix = storage_uri[5:].partition("/")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    model_blob = bucket.blob(f"{prefix.rstrip('/')}/model.json")
    target_path = target_dir / "model.json"
    model_blob.download_to_filename(target_path)
    return target_path


def _load_model() -> dict[str, Any]:
    global _MODEL
    if _MODEL is not None:
        return _MODEL

    storage_uri = os.getenv("AIP_STORAGE_URI")
    if storage_uri:
        with TemporaryDirectory() as tmp:
            model_path = _download_gcs_model(storage_uri, Path(tmp))
            _MODEL = json.loads(model_path.read_text(encoding="utf-8"))
            return _MODEL

    local_path = Path(os.getenv("MODEL_PATH", "models/rack_state_model.json"))
    _MODEL = json.loads(local_path.read_text(encoding="utf-8"))
    return _MODEL


@app.get("/health")
def health() -> dict[str, str]:
    _load_model()
    return {"status": "ok", "service": "vertex-rack-state-predictor"}


@app.post("/predict")
def predict(payload: PredictionRequest) -> dict[str, list[dict[str, Any]]]:
    if not payload.instances:
        raise HTTPException(status_code=400, detail="instances must not be empty")

    model = _load_model()
    predictions = [infer_rack_state(model, instance) for instance in payload.instances]
    return {"predictions": predictions}
