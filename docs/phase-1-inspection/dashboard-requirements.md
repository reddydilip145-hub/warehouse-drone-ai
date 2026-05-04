# Review Dashboard Requirements

## Dashboard Purpose

The dashboard lets inventory and operations users review drone inspection results before any replenishment action is executed.

## Primary Views

### Inspection Run Summary

Show:

- Batch ID.
- Route ID.
- Drone ID.
- Zone.
- Start and completion time.
- Planned vs captured locations.
- Pending inference count.
- Exception count.
- Recapture count.
- Flight status.

### Exception Review Queue

Show:

- Location ID.
- Expected SKU.
- Detected SKU if available.
- Fill state.
- Confidence score.
- Exception type.
- Severity.
- Image thumbnail.
- Review status.

Actions:

- Approve.
- Reject.
- Mark needs recapture.
- Correct fill state.
- Correct SKU.
- Add note.

### Location Detail

Show:

- Latest image evidence.
- Inspection history.
- Expected SKU and capacity.
- Detection timeline.
- Reviewer decisions.
- Model version history.

### KPI View

Show:

- Capture completion rate.
- Empty locations detected.
- Low-stock locations detected.
- False positives.
- False negatives from audit sample.
- Average inference latency.
- Average review time.
- Recapture rate.

## Roles

| Role | Permissions |
| --- | --- |
| Viewer | Read inspection results |
| Reviewer | Approve/reject events |
| Supervisor | Override decisions and close batches |
| Admin | Manage zones, routes, users, and thresholds |
| Auditor | View evidence and decisions |

## UX Requirements

- Image evidence must be visible beside the model decision.
- Confidence and model version must be visible.
- Users must be able to filter by aisle, rack, exception type, and status.
- Review actions must be captured with user and timestamp.
- Dashboard should never hide low-confidence results.

