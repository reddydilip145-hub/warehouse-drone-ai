from pathlib import Path

from ml.src.dataset import generate_dataset
from ml.src.inference import infer_rack_state
from ml.src.train import train_centroid_model


def test_training_and_inference(tmp_path: Path) -> None:
    dataset = tmp_path / "dataset.jsonl"
    model_path = tmp_path / "model.json"
    rows = generate_dataset(dataset, rows=30, seed=7)
    model = train_centroid_model(dataset, model_path)
    prediction = infer_rack_state(model, rows[0])
    assert model_path.exists()
    assert prediction["fill_state"] in {"empty", "low", "full", "blocked"}
    assert 0 <= prediction["confidence_score"] <= 1

