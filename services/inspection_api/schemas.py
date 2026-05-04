from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ImageCaptureRequest(BaseModel):
    batch_id: str
    facility_id: str
    zone_id: str
    location_id: str
    drone_id: str
    idempotency_key: str
    raw_object_key: str
    captured_at: datetime
    camera_angle: str = "front"
    features: dict[str, Any] = Field(default_factory=dict)


class InspectionEvent(BaseModel):
    inspection_id: str
    image_id: str
    facility_id: str
    zone_id: str
    location_id: str
    drone_id: str
    event_type: str
    fill_state: str
    fill_percentage: float
    confidence_score: float
    review_status: str
    model_version_id: str

