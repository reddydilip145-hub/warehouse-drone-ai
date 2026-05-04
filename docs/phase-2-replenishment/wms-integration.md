# WMS Integration

## Integration Goal

Phase 2 should create replenishment tasks in the WMS or task-management system only after recommendations are approved. During the pilot, WMS integration should start in controlled mode.

## Integration Modes

| Mode | Description | Recommended Use |
| --- | --- | --- |
| read_only | Read SKU, location, inventory, and task status | Start here |
| task_draft | Create draft tasks requiring WMS user confirmation | Early pilot |
| controlled_create | Create approved tasks with limited zones/SKUs | Phase 2 target |
| full_create | Create tasks across approved scope | Later rollout |
| inventory_mutation | Direct quantity updates | Avoid until mature |

## Data To Read From WMS

- SKU master.
- Location master.
- SKU-location plan.
- Source inventory availability.
- Case pack and handling rules.
- Existing open replenishment tasks.
- Task status updates.
- Zone safety or operational holds if available.

## Data To Write To WMS

For controlled task creation:

- target_location_id.
- source_location_id.
- sku_id.
- quantity.
- priority.
- execution_method.
- external reference to recommendation_id.
- evidence reference or dashboard URL.

## Task Status Mapping

| Internal Status | WMS Status Example |
| --- | --- |
| created | created/released |
| assigned | assigned |
| started | in_progress |
| blocked | held/exception |
| completed | complete |
| cancelled | cancelled |
| failed | exception |

## Safety And Control Gates

Before writing tasks to WMS:

- Recommendation must be approved.
- Zone must allow replenishment.
- SKU must be eligible.
- Source inventory must be available.
- No duplicate open WMS task should exist.
- Execution method must be allowed for product class.
- Pilot limits must not be exceeded.

## Audit Requirements

Every WMS task must be traceable back to:

- inspection_id.
- candidate_id.
- recommendation_id.
- approver_id.
- image evidence.
- model_version_id.
- source inventory snapshot.

