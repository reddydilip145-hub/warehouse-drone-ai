from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.src.dataset import generate_dataset
from ml.src.inference import infer_rack_state
from ml.src.train import train_centroid_model
from services.replenishment_api.engine import create_recommendation


def main() -> None:
    tmp_dir = ROOT / "data" / "runtime" / "smoke"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    dataset = tmp_dir / "dataset.jsonl"
    model_path = tmp_dir / "model.json"
    rows = generate_dataset(dataset, rows=100, seed=11)
    model = train_centroid_model(dataset, model_path)
    prediction = infer_rack_state(model, rows[0])
    assert prediction["fill_state"] in {"empty", "low", "full", "blocked"}

    recommendation = create_recommendation(
        {
            "inspection_id": "insp-smoke",
            "facility_id": "cs-facility-001",
            "location_id": "A01-R01-B01-L01",
            "fill_state": "empty",
            "fill_percentage": 0,
            "confidence_score": 0.94,
        },
        {"sku_id": "SKU-10001", "max_capacity": "24", "min_threshold": "8"},
        {"sku_id": "SKU-10001", "case_pack": "12", "handling_class": "standard_case", "case_weight": "7.5"},
        [{"source_location_id": "RESERVE-A09-B01", "sku_id": "SKU-10001", "available_quantity": "120", "reserved_quantity": "0"}],
    )
    assert recommendation["recommended_quantity"] == 24
    print("smoke test passed")


if __name__ == "__main__":
    main()
