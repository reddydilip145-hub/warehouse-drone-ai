# Execution Method Matrix

## Purpose

Phase 2 recommends how replenishment should be executed. It does not assume drones are the right movement method for every grocery product.

## Method Selection Matrix

| Product/Location Condition | Human | Forklift | AMR | Drone | ASRS/Conveyor |
| --- | --- | --- | --- | --- | --- |
| Small lightweight SKU | Allowed | Usually unnecessary | Allowed | Candidate | If available |
| Standard case goods | Allowed | Allowed | Candidate | Usually not allowed | If available |
| Heavy case | Team lift only | Preferred | Candidate if rated | Not allowed | If available |
| Pallet movement | Not preferred | Preferred | AGV candidate | Not allowed | If available |
| Fragile product | Preferred | Allowed with care | Candidate | Usually not allowed | Case-by-case |
| Liquid cases | Allowed | Preferred | Candidate | Not allowed | Case-by-case |
| Frozen/chilled | Specialized | Specialized | Specialized | Not in pilot | If available |
| Hazardous | Restricted | Restricted | Restricted | Not allowed | Restricted |
| High traffic aisle | Preferred | Controlled window | Controlled window | Not allowed | If available |

## Drone Movement Guardrails

Drone movement should be considered only when:

- Product is lightweight.
- Product is safe to carry.
- Package is stable.
- Flight path avoids workers and forklifts.
- Drop-off/pick-up mechanism is validated.
- Safety owner approves movement mode.
- Verification loop is active.

For grocery warehouses, most Phase 2 tasks should route to human, forklift, AMR, or WMS-controlled workflows. Drone product movement belongs in Phase 3 and only for narrow SKU classes.

## AMR/Forklift Guardrails

AMR or forklift execution requires:

- Source and target location coordinates.
- Weight and dimension validation.
- Traffic management.
- Worker separation.
- WMS task compatibility.
- Completion scan or confirmation.

