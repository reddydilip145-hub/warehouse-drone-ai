# Warehouse Automation Documentation

## Program Structure

This documentation package defines the warehouse automation plan for a grocery warehouse pilot.

| Phase | Package | Purpose |
| --- | --- | --- |
| Phase 0 | [phase-0-discovery](phase-0-discovery/README.md) | Discovery, warehouse mapping, safety, integration, and readiness gate |
| Phase 1 | [phase-1-inspection](phase-1-inspection/README.md) | Drone rack inspection, image upload, vision inference, Cloud SQL events, and review workflow |
| Phase 2 | [phase-2-replenishment](phase-2-replenishment/README.md) | Replenishment recommendations, approval workflow, WMS task creation, and completion tracking |

## Implementation Packages

| Area | Path | Purpose |
| --- | --- | --- |
| Sample data | `data/sample` | Phase 0 master data and source inventory seed files |
| ML pipeline | `ml` | Dataset generator, baseline trainer, inference, and Kubeflow DAG shape |
| Inspection service | `services/inspection_api` | Phase 1 image capture registration and inspection event API |
| Replenishment service | `services/replenishment_api` | Phase 2 recommendation and approval API |
| Terraform | `infra/terraform/gcp` | GCP buckets, Cloud SQL, and service account starter |
| Helm | `infra/helm/warehouse-drone-ai` | Kubernetes deployment templates |
| Local scripts | `scripts` | Smoke test and local Phase 0-1-2 pipeline |

## Recommended Execution Order

1. Complete Phase 0 discovery and sign-offs.
2. Use Phase 1 to build the controlled inspection pilot.
3. Use Phase 2 to convert approved inspection events into replenishment recommendations and controlled WMS tasks.
4. Move to Phase 3 only after task decisions, approvals, and completion verification are stable.

## Current Technical Direction

```text
Drone/edge uploader
-> Cloud object storage
-> Ingestion API
-> Vision inference service
-> Cloud SQL
-> Review dashboard
-> Phase 2 replenishment candidate queue
-> Replenishment decision engine
-> WMS/task management
```

Recommended deployment stack:

```text
Docker + Kubernetes + Helm + Argo CD + Terraform + MLflow
```
