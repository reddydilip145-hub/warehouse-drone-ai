# Warehouse Drone AI

Warehouse automation planning package for drone-based rack inspection, replenishment decisioning, and phased grocery warehouse automation.

Start here: [docs/README.md](docs/README.md)

## Code Included

- Phase 0 sample master data under `data/sample`.
- Phase 1 dataset generation, model training, inference, and inspection API.
- Phase 2 replenishment decision engine and API.
- Local Phase 0-1-2 pipeline under `scripts/run_local_pipeline.py`.
- Terraform starter for GCP Cloud SQL and object storage.
- Helm/Kubernetes deployment chart for inspection and replenishment services.

## Run Locally

```powershell
python scripts\smoke_test.py
python scripts\run_local_pipeline.py
```

Install API dependencies when you want to run the FastAPI services:

```powershell
pip install -r requirements.txt
uvicorn services.inspection_api.app:app --reload --port 8000
uvicorn services.replenishment_api.app:app --reload --port 8001
```
