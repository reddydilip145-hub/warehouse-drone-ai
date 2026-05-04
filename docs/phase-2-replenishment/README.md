# Phase 2 Replenishment Decision Engine

## Purpose

Phase 2 converts approved Phase 1 inspection events into controlled replenishment recommendations and tasks. It decides what product is needed, how urgent it is, where inventory should come from, and which execution method should be used.

Phase 2 still does not require fully autonomous product movement. It creates decision-ready replenishment tasks that can be routed to humans, forklifts, AMRs, drones, or other warehouse systems based on safety and feasibility.

## Scope

Included:

- Consume approved inspection events from Phase 1.
- Validate expected SKU and target location.
- Check source inventory availability.
- Prioritize replenishment needs.
- Select recommended execution method.
- Create replenishment recommendation records.
- Route recommendations through human approval.
- Integrate with WMS/task management in controlled mode.
- Track task status and completion evidence.

Excluded:

- Fully autonomous drone/robot movement without approval.
- Direct inventory quantity mutation unless WMS owner approves.
- Freezer/chilled/hazardous automation unless separately certified.
- Pallet movement automation without forklift/AGV safety design.

## System Flow

```text
Approved inspection event
-> Candidate validation
-> Source inventory lookup
-> Priority scoring
-> Execution method selection
-> Human approval gate
-> WMS/task creation
-> Task status tracking
-> Completion verification request
```

## Phase 2 Success Criteria

- Approved Phase 1 events are converted into replenishment recommendations.
- Recommendations include SKU, target location, source location, priority, quantity, and execution method.
- Human users can approve, reject, or modify recommendations.
- WMS/task integration can create controlled replenishment tasks.
- Duplicate recommendations are prevented for the same unresolved need.
- Task status is traceable from inspection event to closure.
- Completion verification can be requested from Phase 1 inspection.
- Phase 3 receives clean execution-ready task contracts.

## Core Services

| Service | Responsibility |
| --- | --- |
| Candidate consumer | Reads approved Phase 1 inspection events |
| Inventory adapter | Reads WMS/source inventory and SKU-location data |
| Replenishment engine | Scores priority and recommends quantity |
| Execution selector | Chooses human, forklift, AMR, drone, or ASRS path |
| Approval service | Manages approval workflow |
| WMS connector | Creates or updates external tasks |
| Task tracker | Tracks lifecycle and status |
| Verification requester | Requests post-task inspection evidence |

## Deliverables

- Replenishment architecture.
- Decision rules.
- Database extension schema.
- API contract.
- WMS integration contract.
- Approval workflow.
- Execution method matrix.
- Testing and acceptance plan.
- Phase 3 handoff.

