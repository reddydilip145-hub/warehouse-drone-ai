param(
  [string]$ProjectId = "model-journal-431911-h3",
  [string]$Region = "asia-south1",
  [string]$BucketName = "warehouse-drone-ai-vertex-models-model-journal-431911-h3",
  [string]$ModelDisplayName = "rack-state-centroid-baseline",
  [string]$ModelVersion = "v0.1.0"
)

$ErrorActionPreference = "Stop"
$ArtifactUri = "gs://$BucketName/$ModelDisplayName/$ModelVersion"
$ImageUri = "$Region-docker.pkg.dev/$ProjectId/warehouse-drone-ai/vertex-rack-predictor:latest"

gcloud config set project $ProjectId

$ExistingBucket = gcloud storage buckets list --project=$ProjectId --filter="name=$BucketName" --format="value(name)" | Select-Object -First 1
if (-not $ExistingBucket) {
  gcloud storage buckets create "gs://$BucketName" --location=$Region --uniform-bucket-level-access --project=$ProjectId
}

gcloud storage cp models\rack_state_model.json "$ArtifactUri/model.json" --project=$ProjectId

gcloud ai models upload `
  --region=$Region `
  --display-name=$ModelDisplayName `
  --artifact-uri=$ArtifactUri `
  --container-image-uri=$ImageUri `
  --container-ports=8080 `
  --container-health-route=/health `
  --container-predict-route=/predict
