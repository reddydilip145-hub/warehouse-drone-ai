# Phase 2 Architecture

## Logical Architecture

```text
Phase 1 inspection_event
-> replenishment_candidate_consumer
-> replenishment_engine
-> inventory_adapter
-> execution_selector
-> approval_service
-> wms_connector
-> task_tracker
-> verification_requester
```

## Component Responsibilities

| Component | Responsibility |
| --- | --- |
| Candidate consumer | Accepts approved empty/low-stock events and prevents duplicate processing |
| Inventory adapter | Reads source inventory, expected SKU, available quantity, and handling data |
| Replenishment engine | Calculates required quantity and priority |
| Execution selector | Chooses the safest and most practical execution method |
| Approval service | Routes recommendations to inventory/operations users |
| WMS connector | Creates WMS replenishment tasks in approved mode |
| Task tracker | Tracks task states and syncs status from WMS |
| Verification requester | Asks Phase 1 to re-inspect completed target locations |

## Deployment

Use the same platform direction as Phase 1.

```text
Docker
-> Helm
-> Argo CD
-> Kubernetes namespace: warehouse-replenishment
```

Recommended services:

- replenishment-api.
- replenishment-worker.
- inventory-adapter.
- wms-connector.
- approval-service.
- task-status-worker.

## Event-Driven Design

Phase 2 should use event queues so warehouse operations are not blocked by temporary WMS or network failures.

Recommended events:

- inspection_event_approved.
- replenishment_candidate_created.
- replenishment_recommendation_created.
- replenishment_recommendation_approved.
- wms_task_created.
- replenishment_task_started.
- replenishment_task_completed.
- verification_requested.
- verification_passed.
- verification_failed.

## Idempotency

Use idempotency keys to prevent duplicate replenishment tasks.

Recommended key:

```text
{facility_id}:{location_id}:{sku_id}:{inspection_id}
```

For ongoing low-stock conditions, also enforce one open recommendation per:

```text
{facility_id}:{location_id}:{sku_id}
```

## Failure Handling

| Failure | Handling |
| --- | --- |
| Source inventory unavailable | Recommendation remains pending_inventory_check |
| WMS API unavailable | Retry and alert after threshold |
| Duplicate candidate | Link to existing open recommendation |
| SKU mismatch unresolved | Hold recommendation |
| Safety hold on zone | Block task creation |
| Human rejection | Close recommendation with reason |
| Task not completed | Escalate to supervisor |
| Verification fails | Reopen recommendation or create exception |

