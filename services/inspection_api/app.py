from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException

from ml.src.inference import infer_rack_state, load_model
from services.common.storage import ROOT, RUNTIME_DIR, ensure_runtime, read_jsonl, write_jsonl
from services.inspection_api.schemas import ImageCaptureRequest, InspectionEvent


app = FastAPI(title="Warehouse Drone AI Inspection API", version="0.1.0")
MODEL_PATH = ROOT / "models" / "rack_state_model.json"
EVENTS_PATH = RUNTIME_DIR / "inspection_events.jsonl"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "inspection-api"}


@app.post("/v1/image-captures", response_model=InspectionEvent)
def register_image_capture(payload: ImageCaptureRequest) -> InspectionEvent:
    ensure_runtime()
    if not MODEL_PATH.exists():
        raise HTTPException(status_code=503, detail="model is not trained yet")

    events = read_jsonl(EVENTS_PATH)
    for event in events:
        if event.get("idempotency_key") == payload.idempotency_key:
            return InspectionEvent(**{k: event[k] for k in InspectionEvent.model_fields})

    model = load_model(MODEL_PATH)
    result = infer_rack_state(model, payload.features)
    event_type = result["exception_type"] or "normal"
    event = {
        "inspection_id": str(uuid.uuid4()),
        "image_id": str(uuid.uuid4()),
        "facility_id": payload.facility_id,
        "zone_id": payload.zone_id,
        "location_id": payload.location_id,
        "drone_id": payload.drone_id,
        "event_type": event_type,
        "fill_state": result["fill_state"],
        "fill_percentage": result["fill_percentage"],
        "confidence_score": result["confidence_score"],
        "review_status": "pending" if event_type != "normal" else "auto_accepted",
        "model_version_id": result["model_version_id"],
        "idempotency_key": payload.idempotency_key,
        "raw_object_key": payload.raw_object_key,
    }
    events.append(event)
    write_jsonl(EVENTS_PATH, events)
    return InspectionEvent(**{k: event[k] for k in InspectionEvent.model_fields})


@app.get("/v1/inspection-events")
def list_inspection_events() -> list[dict]:
    return read_jsonl(EVENTS_PATH)

