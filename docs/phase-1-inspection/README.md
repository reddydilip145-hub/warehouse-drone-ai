# Phase 1 Drone Rack Inspection

## Purpose

Phase 1 builds the first working inspection system. Drones capture rack/bin images in the approved pilot zone, upload image evidence to cloud storage, run computer vision inference, and write structured inspection events to Cloud SQL for review.

Phase 1 does not automatically move products. Its job is to prove that the platform can safely and accurately detect empty, low-stock, blocked, damaged, or mismatched rack/bin conditions.

## Scope

Included:

- Controlled drone inspection routes for the selected dry grocery pilot zone.
- Image capture and edge upload.
- Cloud object storage for raw and processed images.
- Vision inference service for rack state detection.
- Cloud SQL inspection event database.
- Human review workflow for uncertain or high-impact detections.
- Dashboard/API surface for inspection results.
- Accuracy, latency, safety, and operational KPI reporting.

Excluded:

- Automated replenishment movement.
- Direct WMS inventory mutation without human approval.
- Freezer/chilled/hazardous zones.
- Fully autonomous drone route generation.
- Multi-warehouse rollout.

## Success Criteria

Phase 1 is successful when:

- Drone flights complete the pilot route safely across approved flight windows.
- At least 95% of planned rack/bin locations are captured per inspection run.
- Empty/low-stock detection reaches the agreed pilot accuracy target.
- False negatives are low enough for operations approval.
- Every inspection event has image evidence.
- Cloud SQL records are traceable to location, drone, timestamp, and model version.
- Human reviewers can approve/reject exceptions.
- The system produces a replenishment recommendation candidate without executing movement.
- Phase 2 stakeholders approve the readiness gate.

## System Flow

```text
Pilot route schedule
-> Drone flight client
-> Edge capture and metadata tagging
-> Cloud object storage upload
-> Ingestion API
-> Vision inference service
-> Cloud SQL inspection event
-> Human review dashboard
-> Phase 2 replenishment candidate queue
```

## Phase 1 Workstreams

### 1. Edge Drone Inspection

- Configure pilot route.
- Capture rack/bin images.
- Attach metadata before upload.
- Buffer images during network issues.
- Retry failed uploads.
- Record drone health and flight status.

### 2. Cloud Ingestion

- Accept image metadata.
- Validate facility, zone, and location IDs.
- Store image object keys.
- Create inspection batch records.
- Trigger inference jobs.

### 3. Vision Inference

- Detect rack fill state.
- Estimate fill percentage.
- Detect blocked views and poor image quality.
- Detect visible labels/barcodes where possible.
- Attach model version and confidence score.

### 4. Review And Audit

- Show image evidence.
- Allow approve/reject/needs-recapture.
- Track reviewer decisions.
- Store correction labels for model improvement.

### 5. Reporting

- Inspection completion rate.
- Empty/low/full distribution.
- False positive/false negative tracking.
- Locations needing recapture.
- Drone flight reliability.
- Model confidence distribution.

## Phase 1 Deliverables

- Architecture design.
- Cloud SQL schema.
- Object storage layout.
- API contract.
- Edge drone workflow.
- Vision inference plan.
- Dashboard requirements.
- Test and acceptance plan.
- Phase 2 handoff checklist.

