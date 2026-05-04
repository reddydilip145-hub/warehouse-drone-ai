from __future__ import annotations

import json
import uuid
from pathlib import Path

from ml.src.dataset import generate_dataset
from ml.src.inference import infer_rack_state, load_model
from ml.src.train import train_centroid_model
from services.common.storage import ROOT, SAMPLE_DIR, ensure_runtime, read_csv, read_jsonl, write_jsonl
from services.replenishment_api.engine import create_recommendation


def run_pipeline() -> dict:
    runtime = ensure_runtime()

    # Phase 0: validate master data exists.
    locations = read_csv(SAMPLE_DIR / "warehouse_locations.csv")
    sku_plan = read_csv(SAMPLE_DIR / "location_sku_plan.csv")
    skus = read_csv(SAMPLE_DIR / "sku_master.csv")
    inventory = read_csv(SAMPLE_DIR / "source_inventory.csv")

    # Phase 1: create dataset, train baseline, infer inspection events.
    dataset_path = SAMPLE_DIR / "rack_inspection_dataset.jsonl"
    generate_dataset(dataset_path, rows=250)
    model_path = ROOT / "models" / "rack_state_model.json"
    train_centroid_model(dataset_path, model_path)
    model = load_model(model_path)

    sample_images = read_jsonl(dataset_path)[:25]
    events = []
    for image in sample_images:
        result = infer_rack_state(model, image)
        event_type = result["exception_type"] or "normal"
        events.append(
            {
                "inspection_id": str(uuid.uuid4()),
                "image_id": image["image_id"],
                "facility_id": image["facility_id"],
                "zone_id": image["zone_id"],
                "location_id": image["location_id"],
                "event_type": event_type,
                "fill_state": result["fill_state"],
                "fill_percentage": result["fill_percentage"],
                "confidence_score": result["confidence_score"],
                "review_status": "approved" if event_type in {"empty_location", "low_location"} else "auto_accepted",
                "model_version_id": result["model_version_id"],
            }
        )
    write_jsonl(runtime / "inspection_events.jsonl", events)

    # Phase 2: convert approved events into recommendations.
    recommendations = []
    sku_by_location = {row["location_id"]: row for row in sku_plan}
    sku_master = {row["sku_id"]: row for row in skus}
    for event in events:
        if event["event_type"] not in {"empty_location", "low_location"}:
            continue
        plan = sku_by_location[event["location_id"]]
        recommendation = create_recommendation(event, plan, sku_master[plan["sku_id"]], inventory)
        recommendations.append(recommendation)
    write_jsonl(runtime / "replenishment_recommendations.jsonl", recommendations)

    return {
        "locations": len(locations),
        "dataset_records": len(read_jsonl(dataset_path)),
        "inspection_events": len(events),
        "replenishment_recommendations": len(recommendations),
        "model_path": str(model_path),
    }


if __name__ == "__main__":
    print(json.dumps(run_pipeline(), indent=2, sort_keys=True))

