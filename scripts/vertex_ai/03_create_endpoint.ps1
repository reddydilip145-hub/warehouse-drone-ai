param(
  [string]$Region = "asia-south1",
  [string]$EndpointDisplayName = "rack-state-endpoint"
)

$ExistingEndpoint = gcloud ai endpoints list --region=$Region --filter="displayName=$EndpointDisplayName" --format="value(name)" | Select-Object -First 1
if (-not $ExistingEndpoint) {
  gcloud ai endpoints create `
    --region=$Region `
    --display-name=$EndpointDisplayName
} else {
  Write-Host "Endpoint already exists: $ExistingEndpoint"
}

gcloud ai endpoints list --region=$Region --filter="displayName=$EndpointDisplayName"
