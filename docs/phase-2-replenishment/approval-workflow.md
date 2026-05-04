# Approval Workflow

## Purpose

The approval workflow ensures Phase 2 makes operationally useful recommendations without creating unsafe or incorrect replenishment work.

## Recommendation States

```text
new
-> pending_inventory_check
-> pending_approval
-> approved
-> task_created
-> in_progress
-> completed
-> verification_requested
-> verification_passed
```

Exception states:

```text
rejected
blocked
cancelled
verification_failed
needs_review
```

## Reviewer Actions

Users can:

- Approve recommendation.
- Reject recommendation.
- Modify quantity.
- Modify execution method.
- Change priority.
- Put recommendation on hold.
- Request recapture.
- Add notes.

## Auto-Approval Guardrails

Auto-approval should be disabled at the start of the pilot unless the client explicitly approves it.

When enabled, it should be limited by:

- Zone.
- SKU category.
- Confidence threshold.
- Maximum quantity.
- Execution method.
- Time window.
- Daily task count.

## Escalation Rules

Escalate to supervisor when:

- Critical SKU is empty.
- Source inventory is unavailable.
- WMS rejects task creation.
- Task remains open beyond SLA.
- Verification fails after completion.
- Duplicate exception occurs repeatedly at the same location.

## Audit Trail

Each decision must store:

- User ID.
- Decision.
- Original recommendation.
- Modified recommendation if changed.
- Notes.
- Timestamp.
- Source evidence.

