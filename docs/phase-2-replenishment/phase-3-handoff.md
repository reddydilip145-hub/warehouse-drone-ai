# Phase 3 Handoff

## Purpose

Phase 3 starts when replenishment decisions are reliable enough to hand tasks to physical execution systems such as drones, AMRs, forklifts, robotic arms, or human-directed workflows.

## Handoff Contract

Each execution-ready task should provide:

- task_id.
- recommendation_id.
- facility_id.
- zone_id.
- source_location_id.
- target_location_id.
- sku_id.
- quantity.
- product weight and dimensions.
- handling class.
- priority.
- execution_method.
- approved_by.
- safety constraints.
- route constraints.
- evidence reference.
- verification requirement.

## Phase 3 Preconditions

Proceed only when:

- Phase 2 task recommendations are accurate and approved.
- WMS/task integration is stable.
- Product classes are mapped to execution methods.
- Safety owner approves physical movement automation scope.
- Completion verification is operational.
- Exception handling and manual fallback are ready.

## Phase 3 Starting Scope

Recommended starting scope:

- Human and forklift tasks first.
- AMR tasks for controlled case movement second.
- Drone product movement only for lightweight and low-risk SKUs.
- No freezer, hazardous, or high-traffic autonomous movement in first Phase 3 pilot.

