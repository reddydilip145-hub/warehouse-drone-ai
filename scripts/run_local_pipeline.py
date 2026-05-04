from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.pipelines.local_phase_0_1_2_pipeline import run_pipeline


if __name__ == "__main__":
    result = run_pipeline()
    for key, value in result.items():
        print(f"{key}: {value}")
