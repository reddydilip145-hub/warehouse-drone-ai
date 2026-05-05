param(
  [string]$ProjectId = "model-journal-431911-h3",
  [string]$Region = "asia-south1"
)

gcloud config set project $ProjectId
gcloud builds submit `
  --region=$Region `
  --default-buckets-behavior=regional-user-owned-bucket `
  --config infra\cloudbuild\vertex-predictor.yaml `
  .
