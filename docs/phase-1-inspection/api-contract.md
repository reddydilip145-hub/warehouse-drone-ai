# API Contract

## Principles

- Every drone upload must be idempotent.
- Every image must include enough metadata to map it to a warehouse location or quarantine it.
- API responses should be explicit about accepted, rejected, and pending states.
- Ingestion should accept evidence before inference is available.

## Endpoints

### Create Inspection Batch

```http
POST /v1/inspection-batches
```

Request:

```json
{
  "facility_id": "cs-facility-001",
  "zone_id": "dry-zone-a",
  "drone_id": "drone-001",
  "route_id": "route-dry-a-001",
  "started_at": "2026-05-04T10:00:00Z",
  "planned_location_count": 250
}
```

Response:

```json
{
  "batch_id": "7e278ae9-3c23-42c4-a17e-b17c2e518001",
  "status": "running"
}
```

### Register Image Capture

```http
POST /v1/image-captures
```

Request:

```json
{
  "batch_id": "7e278ae9-3c23-42c4-a17e-b17c2e518001",
  "facility_id": "cs-facility-001",
  "location_id": "A01-R02-B03-L04",
  "drone_id": "drone-001",
  "idempotency_key": "drone-001-route-dry-a-001-A01-R02-B03-L04-20260504T100102Z",
  "raw_object_key": "raw/cs-facility-001/dry-zone-a/2026/05/04/batch-001/image-001.jpg",
  "captured_at": "2026-05-04T10:01:02Z",
  "camera_angle": "front",
  "metadata": {
    "battery_percentage": 78,
    "altitude_m": 3.2,
    "signal_strength": "good"
  }
}
```

Response:

```json
{
  "image_id": "537dbdc0-7d49-45d0-97fb-98b82e0537c8",
  "status": "accepted",
  "inference_status": "queued"
}
```

### Get Inspection Event

```http
GET /v1/inspection-events/{inspection_id}
```

Response:

```json
{
  "inspection_id": "72f589fc-9cb4-4ef5-9d9f-24c34192a28d",
  "location_id": "A01-R02-B03-L04",
  "event_type": "empty_location",
  "severity": "high",
  "review_status": "pending",
  "evidence": {
    "image_id": "537dbdc0-7d49-45d0-97fb-98b82e0537c8",
    "raw_object_key": "raw/cs-facility-001/dry-zone-a/2026/05/04/batch-001/image-001.jpg"
  },
  "detection": {
    "fill_state": "empty",
    "fill_percentage": 0,
    "confidence_score": 0.94,
    "model_version_id": "rack-detector-v0.3.1"
  }
}
```

### Submit Review Decision

```http
POST /v1/inspection-events/{inspection_id}/reviews
```

Request:

```json
{
  "reviewer_id": "inventory-supervisor-01",
  "decision": "approved",
  "corrected_fill_state": "empty",
  "notes": "Confirmed empty during manual audit."
}
```

Response:

```json
{
  "review_id": "6016368d-d4d6-40af-ad69-e45fc1595000",
  "review_status": "approved"
}
```

## Error Codes

| Code | Meaning |
| --- | --- |
| 400 | Missing or invalid metadata |
| 401 | Unauthenticated device/user |
| 403 | Device not authorized for facility/zone |
| 404 | Batch or location not found |
| 409 | Duplicate idempotency key |
| 422 | Known location but inspection is not allowed |
| 503 | Ingestion temporarily unavailable |

