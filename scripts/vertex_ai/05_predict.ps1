param(
  [string]$Region = "asia-south1",
  [string]$EndpointDisplayName = "rack-state-endpoint",
  [string]$RequestPath = "docs\vertex-ai\sample_prediction_request.json"
)

$ErrorActionPreference = "Stop"
$EndpointId = gcloud ai endpoints list --region=$Region --filter="displayName=$EndpointDisplayName" --format="value(name)" | Select-Object -First 1

if (-not $EndpointId) { throw "Endpoint not found: $EndpointDisplayName" }

gcloud ai endpoints predict $EndpointId `
  --region=$Region `
  --json-request=$RequestPath
