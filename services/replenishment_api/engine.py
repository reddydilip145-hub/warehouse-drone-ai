from __future__ import annotations

import math
import uuid
from typing import Any


def round_to_case_pack(quantity: int, case_pack: int) -> int:
    if case_pack <= 0:
        return quantity
    return int(math.ceil(quantity / case_pack) * case_pack)


def priority_from_score(score: int) -> str:
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def select_execution_method(sku: dict[str, Any]) -> str:
    handling_class = sku.get("handling_class", "standard_case")
    weight = float(sku.get("case_weight", 0) or 0)
    if handling_class in {"hazardous", "frozen", "chilled"}:
        return "human_specialized"
    if handling_class in {"heavy", "liquid"} or weight >= 14:
        return "forklift"
    if handling_class == "fragile":
        return "human"
    if weight <= 5:
        return "amr_or_drone_candidate"
    return "human"


def select_source_inventory(sku_id: str, inventory_rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    candidates = [
        row
        for row in inventory_rows
        if row["sku_id"] == sku_id and int(row["available_quantity"]) - int(row["reserved_quantity"]) > 0
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda row: int(row["available_quantity"]) - int(row["reserved_quantity"]))


def create_recommendation(
    event: dict[str, Any],
    location_plan: dict[str, Any],
    sku: dict[str, Any],
    inventory_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    max_capacity = int(location_plan["max_capacity"])
    current_quantity = int(max_capacity * float(event.get("fill_percentage", 0)) / 100)
    needed_quantity = max(max_capacity - current_quantity, 0)
    recommended_quantity = round_to_case_pack(needed_quantity, int(sku.get("case_pack", 1) or 1))
    source = select_source_inventory(sku["sku_id"], inventory_rows)
    source_available = source is not None

    score = 25 if event["fill_state"] == "empty" else 15
    score += 20 if source_available else 0
    score += 15 if float(event["confidence_score"]) >= 0.85 else 5
    score += 10 if recommended_quantity > 0 else 0
    score += 10 if sku.get("handling_class") in {"standard_case", "fragile"} else 5
    priority_score = min(score, 100)

    return {
        "recommendation_id": str(uuid.uuid4()),
        "inspection_id": event["inspection_id"],
        "facility_id": event["facility_id"],
        "target_location_id": event["location_id"],
        "source_location_id": source["source_location_id"] if source else None,
        "sku_id": sku["sku_id"],
        "recommended_quantity": recommended_quantity,
        "priority_score": priority_score,
        "priority": priority_from_score(priority_score),
        "execution_method": select_execution_method(sku),
        "recommendation_status": "pending_approval" if source_available else "pending_inventory_check",
        "decision_reasons": [
            f"Inspection detected {event['fill_state']}",
            f"Recommended quantity is {recommended_quantity}",
            "Source inventory available" if source_available else "Source inventory unavailable",
        ],
    }

