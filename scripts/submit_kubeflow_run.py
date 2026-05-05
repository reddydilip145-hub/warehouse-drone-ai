from pathlib import Path

import kfp


ROOT = Path(__file__).resolve().parents[1]
PIPELINE_PACKAGE = ROOT / "dist" / "warehouse-drone-ai-rack-training.yaml"


if __name__ == "__main__":
    client = kfp.Client(host="http://localhost:8888")
    run = client.create_run_from_pipeline_package(
        pipeline_file=str(PIPELINE_PACKAGE),
        arguments={"rows": 100000},
        experiment_name="warehouse-drone-ai",
        run_name="warehouse-drone-ai-100k-rack-training",
    )
    print(f"run_id={run.run_id}")

