param(
  [string]$Region = "asia-south1",
  [string]$ModelDisplayName = "rack-state-centroid-baseline",
  [string]$EndpointDisplayName = "rack-state-endpoint",
  [string]$MachineType = "n1-standard-2"
)

$ErrorActionPreference = "Stop"

$ModelId = gcloud ai models list --region=$Region --filter="displayName=$ModelDisplayName" --format="value(name)" | Select-Object -First 1
$EndpointId = gcloud ai endpoints list --region=$Region --filter="displayName=$EndpointDisplayName" --format="value(name)" | Select-Object -First 1

if (-not $ModelId) { throw "Model not found: $ModelDisplayName" }
if (-not $EndpointId) { throw "Endpoint not found: $EndpointDisplayName" }

gcloud ai endpoints deploy-model $EndpointId `
  --region=$Region `
  --model=$ModelId `
  --display-name="$ModelDisplayName-deployed" `
  --machine-type=$MachineType `
  --min-replica-count=1 `
  --max-replica-count=1 `
  --traffic-split=0=100
