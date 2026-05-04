# Test And Acceptance Plan

## Unit Tests

- Candidate eligibility.
- Duplicate open recommendation prevention.
- Quantity recommendation.
- Priority scoring.
- Execution method selection.
- Approval state transitions.
- WMS payload mapping.
- Verification status transitions.

## Integration Tests

- Approved Phase 1 event creates candidate.
- Candidate generates recommendation with source inventory.
- Duplicate candidate links to existing open recommendation.
- Human approval creates approved recommendation.
- Approved recommendation creates WMS task.
- WMS task status sync updates internal task.
- Completed task requests verification.
- Failed verification reopens recommendation.

## Field Tests

- Run Phase 1 inspection.
- Approve selected empty/low-stock events.
- Generate replenishment recommendations.
- Have supervisor approve tasks.
- Create WMS tasks in controlled mode.
- Execute tasks manually or with existing warehouse process.
- Trigger completion verification inspection.
- Compare verification result with task outcome.

## Acceptance Metrics

| Metric | Pilot Target |
| --- | --- |
| Eligible approved events converted to candidates | >= 95% |
| Duplicate task prevention | 100% |
| Recommendations with valid source inventory | >= 95% |
| WMS task creation success | >= 98% after retries |
| Approval audit completeness | 100% |
| Task status traceability | 100% |
| Verification requested after completion | >= 95% |
| Safety incidents from recommendation flow | 0 |

## Phase 2 Exit Criteria

Phase 2 is complete when:

- Approved inspection events reliably create replenishment candidates.
- Replenishment recommendations include quantity, priority, source, and method.
- Human approval workflow is usable and audited.
- WMS task creation works in controlled mode.
- Task lifecycle is traceable.
- Completion verification loop is working.
- Phase 3 execution contracts are approved.

