# Test And Acceptance Plan

## Test Levels

### Unit Tests

- Metadata validation.
- Idempotency key handling.
- Object key generation.
- SQL repository operations.
- Confidence rule classification.
- Review status transitions.

### Integration Tests

- Image registration creates database records.
- Duplicate upload does not create duplicate captures.
- Unknown location is rejected or quarantined.
- Inference result creates detection and inspection event.
- Human review updates review status.
- Object storage signed URL access is role-controlled.

### Field Tests

- Drone completes approved route.
- Edge uploader handles weak network.
- Image capture covers target rack/bin locations.
- Recapture is triggered for blocked or blurred images.
- Manual audit confirms accuracy sample.
- Emergency stop process is demonstrated.

## Acceptance Metrics

| Metric | Pilot Target |
| --- | --- |
| Planned location capture rate | >= 95% |
| Image upload success rate | >= 98% after retries |
| Empty detection precision | Target agreed in Phase 0 |
| Empty detection recall | Target agreed in Phase 0 |
| False negative rate | Below operations threshold |
| Inference latency | Within dashboard SLA |
| Review decision traceability | 100% |
| Inspection events with image evidence | 100% |
| Safety incidents | 0 |

## Pilot Runbook

1. Confirm safety approval for flight window.
2. Start inspection batch.
3. Run drone route.
4. Confirm upload completion.
5. Run inference.
6. Review exceptions.
7. Sample manual audit locations.
8. Record precision/recall.
9. Export Phase 1 KPI report.
10. Decide whether to repeat, tune model, or move to Phase 2.

## Phase 1 Exit Criteria

Phase 1 is complete when:

- Inspection pipeline runs end to end in the pilot zone.
- Cloud SQL contains traceable inspection records.
- Image evidence is available for every event.
- Review dashboard supports operational approval.
- Accuracy and safety metrics are reviewed by stakeholders.
- Replenishment candidates can be produced for Phase 2.
- No direct automated product movement occurs before Phase 2 approval.

