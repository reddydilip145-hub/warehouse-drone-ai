from pathlib import Path
import sys

from kfp import compiler


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.pipelines.kubeflow_pipeline import warehouse_drone_ai_pipeline


if __name__ == "__main__":
    output = ROOT / "dist" / "warehouse-drone-ai-rack-training.yaml"
    output.parent.mkdir(parents=True, exist_ok=True)
    compiler.Compiler().compile(
        pipeline_func=warehouse_drone_ai_pipeline,
        package_path=str(output),
    )
    print(output)

