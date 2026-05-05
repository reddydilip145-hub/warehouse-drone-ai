param(
  [string]$Region = "asia-south1",
  [string]$EndpointDisplayName = "rack-state-endpoint",
  [switch]$DeleteEndpoint
)

$ErrorActionPreference = "Stop"
$EndpointId = gcloud ai endpoints list --region=$Region --filter="displayName=$EndpointDisplayName" --format="value(name)" | Select-Object -First 1

if (-not $EndpointId) {
  Write-Host "Endpoint not found: $EndpointDisplayName"
  exit 0
}

$DeployedModelIds = gcloud ai endpoints describe $EndpointId --region=$Region --format="value(deployedModels.id)"
foreach ($DeployedModelId in $DeployedModelIds) {
  if ($DeployedModelId) {
    gcloud ai endpoints undeploy-model $EndpointId `
      --region=$Region `
      --deployed-model-id=$DeployedModelId `
      --quiet
  }
}

if ($DeleteEndpoint) {
  gcloud ai endpoints delete $EndpointId --region=$Region --quiet
}
