param(
  [string]$ProjectId = "model-journal-431911-h3"
)

gcloud config set project $ProjectId
gcloud services enable aiplatform.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com storage.googleapis.com --project $ProjectId
