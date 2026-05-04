from __future__ import annotations

from pydantic import BaseModel


class ReplenishmentCandidateRequest(BaseModel):
    inspection_id: str
    facility_id: str
    target_location_id: str
    sku_id: str
    fill_state: str
    fill_percentage: float
    confidence_score: float


class ApprovalRequest(BaseModel):
    approver_id: str
    decision: str
    notes: str = ""

