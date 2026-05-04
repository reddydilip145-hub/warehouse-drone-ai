# Executive Summary: Phase 0 Discovery

## Recommendation

Start the warehouse automation program with a controlled Phase 0 discovery focused on one dry grocery pilot zone. The first implementation should automate rack visibility and inventory exception detection before attempting automated product movement.

## Why Phase 0 Matters

At C&S grocery scale, the biggest risk is not building a model that can identify an empty rack. The bigger risk is connecting that detection to the wrong location, unsafe flight path, incomplete WMS data, or unrealistic replenishment workflow.

Phase 0 reduces that risk by validating the warehouse map, data ownership, safety boundaries, integration path, and pilot success criteria before implementation begins.

## Proposed Pilot Scope

Recommended starting scope:

- One dry grocery zone.
- 100 to 500 rack/bin locations.
- Scheduled drone inspection windows.
- Read-only WMS/inventory integration.
- Human review before replenishment actions.
- Cloud SQL for structured inspection events.
- Object storage for images and annotation data.

## Phase 0 Deliverables

- Warehouse digital twin baseline.
- Rack/bin location master for pilot zone.
- No-fly and safety zone map.
- Stakeholder sign-off checklist.
- Cloud SQL inspection event schema.
- Dataset and annotation plan.
- Risk register.
- Phase 1 readiness checklist.

## Preferred Technical Direction

Use this stack for the pilot:

```text
Drone/edge uploader
-> Cloud object storage
-> Vision inference service
-> Cloud SQL inspection event database
-> Review dashboard
-> WMS integration after validation
```

Deployment direction:

```text
Docker + Kubernetes + Helm + Argo CD + Terraform + MLflow
```

Kubeflow can be added later if model training and retraining pipelines become complex.

## Phase 0 Decision Gate

Proceed to Phase 1 only when:

- Pilot zone is approved.
- Rack/bin mapping is reliable.
- Safety plan is approved.
- Integration path is confirmed.
- Dataset plan is ready.
- Inspection schema is accepted.
- KPI targets are agreed.
