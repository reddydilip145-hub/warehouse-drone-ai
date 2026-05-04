# API Contract

## Create Candidate From Inspection

```http
POST /v1/replenishment/candidates
```

Request:

```json
{
  "inspection_id": "72f589fc-9cb4-4ef5-9d9f-24c34192a28d",
  "facility_id": "cs-facility-001",
  "target_location_id": "A01-R02-B03-L04",
  "sku_id": "SKU-10001",
  "fill_state": "empty",
  "fill_percentage": 0,
  "confidence_score": 0.94,
  "idempotency_key": "cs-facility-001:A01-R02-B03-L04:SKU-10001:72f589fc-9cb4-4ef5-9d9f-24c34192a28d"
}
```

Response:

```json
{
  "candidate_id": "17fd45d2-2242-46a7-9097-fb861d200001",
  "candidate_status": "new"
}
```

## Generate Recommendation

```http
POST /v1/replenishment/candidates/{candidate_id}/recommendation
```

Response:

```json
{
  "recommendation_id": "0e21d219-7fcb-4afa-a51c-f9144e200001",
  "sku_id": "SKU-10001",
  "target_location_id": "A01-R02-B03-L04",
  "source_location_id": "RESERVE-A09-B02",
  "recommended_quantity": 24,
  "priority_score": 82,
  "priority": "critical",
  "execution_method": "forklift",
  "recommendation_status": "pending_approval",
  "decision_reasons": [
    "Target location detected empty",
    "SKU has active demand",
    "Source inventory available",
    "Case weight requires forklift execution"
  ]
}
```

## Approve Recommendation

```http
POST /v1/replenishment/recommendations/{recommendation_id}/approvals
```

Request:

```json
{
  "approver_id": "inventory-supervisor-01",
  "decision": "approved",
  "modified_quantity": 24,
  "modified_execution_method": "forklift",
  "notes": "Approved for controlled WMS task creation."
}
```

Response:

```json
{
  "approval_id": "31f3708e-8683-465e-a4c8-026627200001",
  "recommendation_status": "approved"
}
```

## Create WMS Task

```http
POST /v1/replenishment/recommendations/{recommendation_id}/tasks
```

Response:

```json
{
  "task_id": "956f551d-ce51-46ab-99dd-b5a275200001",
  "external_task_id": "WMS-REPL-900001",
  "task_status": "created"
}
```

## Update Task Status

```http
PATCH /v1/replenishment/tasks/{task_id}
```

Request:

```json
{
  "task_status": "completed",
  "completed_at": "2026-05-04T12:42:00Z",
  "assigned_to": "forklift-operator-14"
}
```

Response:

```json
{
  "task_id": "956f551d-ce51-46ab-99dd-b5a275200001",
  "task_status": "completed",
  "verification_status": "requested"
}
```

## Error Codes

| Code | Meaning |
| --- | --- |
| 400 | Invalid request |
| 401 | Unauthenticated caller |
| 403 | Caller cannot approve or create tasks |
| 404 | Candidate, recommendation, or task not found |
| 409 | Duplicate open recommendation exists |
| 422 | Candidate is not eligible for replenishment |
| 503 | WMS or inventory adapter unavailable |

