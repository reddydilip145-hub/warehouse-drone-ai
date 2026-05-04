from __future__ import annotations

from fastapi import FastAPI, HTTPException

from services.common.storage import RUNTIME_DIR, SAMPLE_DIR, ensure_runtime, read_csv, read_jsonl, write_jsonl
from services.replenishment_api.engine import create_recommendation
from services.replenishment_api.schemas import ApprovalRequest, ReplenishmentCandidateRequest


app = FastAPI(title="Warehouse Drone AI Replenishment API", version="0.1.0")
RECOMMENDATIONS_PATH = RUNTIME_DIR / "replenishment_recommendations.jsonl"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "replenishment-api"}


@app.post("/v1/replenishment/recommendations")
def generate_recommendation(payload: ReplenishmentCandidateRequest) -> dict:
    ensure_runtime()
    sku_plan = {row["location_id"]: row for row in read_csv(SAMPLE_DIR / "location_sku_plan.csv")}
    sku_master = {row["sku_id"]: row for row in read_csv(SAMPLE_DIR / "sku_master.csv")}
    inventory = read_csv(SAMPLE_DIR / "source_inventory.csv")

    if payload.target_location_id not in sku_plan:
        raise HTTPException(status_code=422, detail="target location is not replenishment planned")
    plan = sku_plan[payload.target_location_id]
    if plan["sku_id"] != payload.sku_id:
        raise HTTPException(status_code=422, detail="candidate SKU does not match location plan")

    event = {
        "inspection_id": payload.inspection_id,
        "facility_id": payload.facility_id,
        "location_id": payload.target_location_id,
        "fill_state": payload.fill_state,
        "fill_percentage": payload.fill_percentage,
        "confidence_score": payload.confidence_score,
    }
    recommendation = create_recommendation(event, plan, sku_master[payload.sku_id], inventory)
    rows = read_jsonl(RECOMMENDATIONS_PATH)
    duplicate = next(
        (
            row
            for row in rows
            if row["target_location_id"] == recommendation["target_location_id"]
            and row["sku_id"] == recommendation["sku_id"]
            and row["recommendation_status"] not in {"rejected", "completed", "cancelled"}
        ),
        None,
    )
    if duplicate:
        return duplicate
    rows.append(recommendation)
    write_jsonl(RECOMMENDATIONS_PATH, rows)
    return recommendation


@app.get("/v1/replenishment/recommendations")
def list_recommendations() -> list[dict]:
    return read_jsonl(RECOMMENDATIONS_PATH)


@app.post("/v1/replenishment/recommendations/{recommendation_id}/approval")
def approve_recommendation(recommendation_id: str, payload: ApprovalRequest) -> dict:
    rows = read_jsonl(RECOMMENDATIONS_PATH)
    for row in rows:
        if row["recommendation_id"] == recommendation_id:
            row["recommendation_status"] = "approved" if payload.decision == "approved" else "rejected"
            row["approved_by"] = payload.approver_id
            row["approval_notes"] = payload.notes
            write_jsonl(RECOMMENDATIONS_PATH, rows)
            return row
    raise HTTPException(status_code=404, detail="recommendation not found")

