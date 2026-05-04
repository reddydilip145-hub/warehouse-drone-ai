from __future__ import annotations

import argparse
import random
import uuid
from pathlib import Path

from services.common.storage import SAMPLE_DIR, write_jsonl
from ml.src.config import DATASET_SCALE_TIERS, DEFAULT_DATASET_TIER


LABELS = ("empty", "low", "full", "blocked")


def label_from_fill(fill_percentage: float, blocked: bool) -> str:
    if blocked:
        return "blocked"
    if fill_percentage <= 5:
        return "empty"
    if fill_percentage < 35:
        return "low"
    return "full"


def generate_dataset(output: Path, rows: int, seed: int = 42) -> list[dict]:
    random.seed(seed)
    locations = [
        "A01-R01-B01-L01",
        "A01-R01-B02-L01",
        "A01-R02-B01-L02",
        "A02-R01-B01-L01",
        "A02-R02-B02-L03",
    ]
    records: list[dict] = []
    for index in range(rows):
        blocked = random.random() < 0.08
        fill = random.choice([0, random.uniform(1, 34), random.uniform(35, 100)])
        brightness = random.uniform(0.35, 0.95)
        edge_density = max(0.01, min(1.0, fill / 100 + random.uniform(-0.12, 0.12)))
        barcode_visible = random.random() > 0.15
        records.append(
            {
                "image_id": str(uuid.uuid4()),
                "facility_id": "cs-facility-001",
                "zone_id": "dry-zone-a",
                "location_id": random.choice(locations),
                "object_key": f"synthetic/rack-image-{index:05d}.jpg",
                "fill_percentage_feature": round(fill, 2),
                "brightness_feature": round(brightness, 3),
                "edge_density_feature": round(edge_density, 3),
                "barcode_visible_feature": int(barcode_visible),
                "blocked_feature": int(blocked),
                "label": label_from_fill(fill, blocked),
            }
        )
    write_jsonl(output, records)
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=SAMPLE_DIR / "rack_inspection_dataset.jsonl")
    parser.add_argument("--rows", type=int, default=None)
    parser.add_argument("--tier", choices=DATASET_SCALE_TIERS.keys(), default=DEFAULT_DATASET_TIER)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    row_count = args.rows if args.rows is not None else DATASET_SCALE_TIERS[args.tier]
    rows = generate_dataset(args.output, row_count, args.seed)
    print(f"generated {len(rows)} records at {args.output}")


if __name__ == "__main__":
    main()
