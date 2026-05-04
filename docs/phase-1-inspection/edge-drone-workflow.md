# Edge Drone Workflow

## Pre-Flight Checklist

- Drone battery is above approved threshold.
- Camera lens is clean.
- Route is approved for current flight window.
- No active safety hold exists for the zone.
- Network connection is available or offline buffer is enabled.
- Local storage has enough capacity.
- Emergency stop method is available.
- Operator/supervisor acknowledges flight start if required.

## Flight Workflow

1. Start inspection batch.
2. Load approved route.
3. Navigate to first capture point.
4. Capture image.
5. Attach location and telemetry metadata.
6. Save local copy with checksum.
7. Upload image to object storage.
8. Register image capture through ingestion API.
9. Continue through route.
10. Mark batch complete.
11. Upload flight summary.

## Metadata Captured At Edge

- drone_id.
- route_id.
- batch_id.
- facility_id.
- zone_id.
- expected location_id.
- timestamp.
- battery percentage.
- camera angle.
- altitude or shelf height.
- signal strength.
- local image checksum.
- capture attempt number.

## Offline Behavior

If connectivity fails:

- Continue capturing only if safety policy allows.
- Store images locally.
- Queue ingestion requests locally.
- Retry upload with exponential backoff.
- Mark late uploads with original captured_at timestamp.
- Alert operator if buffer capacity approaches limit.

## Recapture Rules

Trigger recapture when:

- Image is blurred.
- Rack/bin is blocked.
- Location marker is not visible.
- Model returns unknown or low confidence.
- Expected location cannot be validated.
- Human reviewer requests recapture.

