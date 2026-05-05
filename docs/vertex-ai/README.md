# Vertex AI Hands-On

This path adds Vertex AI to the same `warehouse-drone-ai` project. GKE still runs the warehouse APIs and drone coordination services; Vertex AI hosts the rack-state model endpoint.

## Target Flow

```text
Drone image/features
  -> inspection-api on GKE
  -> Vertex AI endpoint
  -> rack state prediction
  -> replenishment-api on GKE
  -> replenishment task
```

## One-Time Setup

Run from the repo root in PowerShell.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\vertex_ai\00_enable_vertex_ai.ps1
```

## Build Predictor Container

```powershell
powershell -ExecutionPolicy Bypass -File scripts\vertex_ai\01_build_predictor_image.ps1
```

## Upload And Register Model

```powershell
powershell -ExecutionPolicy Bypass -File scripts\vertex_ai\02_upload_and_register_model.ps1
```

This uploads `models/rack_state_model.json` to Cloud Storage and registers it in Vertex AI Model Registry with the custom prediction container.

## Create Endpoint And Deploy

```powershell
powershell -ExecutionPolicy Bypass -File scripts\vertex_ai\03_create_endpoint.ps1
powershell -ExecutionPolicy Bypass -File scripts\vertex_ai\04_deploy_model.ps1
```

## Test Prediction

```powershell
powershell -ExecutionPolicy Bypass -File scripts\vertex_ai\05_predict.ps1
```

Expected result: Vertex AI returns `predictions` with `fill_state`, `confidence_score`, `fill_percentage`, and `model_version_id`.

## Cleanup To Stop Endpoint Cost

When the hands-on demo is finished, undeploy the model from the online endpoint:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\vertex_ai\06_cleanup_endpoint.ps1
```

To also delete the endpoint shell after undeploying:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\vertex_ai\06_cleanup_endpoint.ps1 -DeleteEndpoint
```

## Console Checks

- Vertex AI -> Model Registry -> `rack-state-centroid-baseline`
- Vertex AI -> Online prediction -> `rack-state-endpoint`
- Artifact Registry -> `warehouse-drone-ai/vertex-rack-predictor`
