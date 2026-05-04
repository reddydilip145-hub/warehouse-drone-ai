# Phase 1 Architecture

## Logical Components

| Component | Responsibility |
| --- | --- |
| Drone flight client | Runs approved routes and captures rack/bin images |
| Edge uploader | Tags metadata, buffers files, and uploads images |
| Ingestion API | Validates uploads and creates inspection records |
| Object storage | Stores raw images, processed images, thumbnails, and annotations |
| Vision inference service | Classifies rack state and creates detection results |
| Cloud SQL | Stores structured inspection, detection, review, and audit records |
| Review dashboard | Lets users inspect exceptions and approve/reject results |
| Notification service | Sends recapture or critical exception alerts |
| WMS read connector | Reads expected SKU/location data for comparison |
| Model registry | Tracks model versions, metrics, and production approval |

## Recommended Deployment

Use Kubernetes for backend services and ML inference.

```text
Docker images
-> Container registry
-> Helm charts
-> Argo CD sync
-> Kubernetes namespace: warehouse-inspection
```

Infrastructure should be provisioned with Terraform:

- Cloud SQL instance.
- Object storage buckets.
- Kubernetes cluster or namespace.
- Service accounts.
- Secrets.
- Network policies.
- Pub/Sub or queue service.

## Runtime Environments

| Environment | Purpose |
| --- | --- |
| local | Developer testing with sample images |
| dev | API/inference integration testing |
| staging | Pilot-zone route and dashboard validation |
| production-pilot | Controlled warehouse pilot |

## Data Flow Detail

1. The drone starts an approved inspection route.
2. The flight client captures rack/bin images at planned positions.
3. The edge uploader adds metadata and stores local copies until upload succeeds.
4. Images are uploaded to object storage.
5. The ingestion API creates an inspection batch and image capture record.
6. A queue message triggers inference.
7. The inference service reads the image, runs the model, and writes detection results.
8. The system writes or updates an inspection event in Cloud SQL.
9. Low-confidence, blocked, mismatch, and critical results go to human review.
10. Approved results are exposed to Phase 2 as replenishment candidates.

## Failure Handling

| Failure | Handling |
| --- | --- |
| Network outage | Edge uploader buffers images and retries |
| Duplicate upload | API uses idempotency key per image capture |
| Unknown location ID | Upload rejected or routed to quarantine |
| Low image quality | Event marked needs_recapture |
| Model unavailable | Queue message retried; event stays pending_inference |
| SQL write failure | Retry with dead-letter queue after threshold |
| Object storage failure | Edge uploader retains local copy |
| Dashboard unavailable | Inspection pipeline continues; reviews wait |

## Security Requirements

- Drone/edge devices use device identity, not shared passwords.
- Upload API requires signed tokens or mutual TLS.
- Object storage uses private buckets.
- SQL is private-network accessible only.
- Image access is role-based and audited.
- Human images are restricted or masked according to client policy.
- Secrets are stored in cloud secret manager.

