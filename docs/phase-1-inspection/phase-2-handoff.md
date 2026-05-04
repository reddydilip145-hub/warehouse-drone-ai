# Phase 2 Handoff

## Purpose

Phase 2 starts after Phase 1 can reliably identify inventory exceptions. The handoff converts approved inspection events into replenishment decision inputs.

## Handoff Data

Each approved candidate should provide:

- inspection_id.
- facility_id.
- zone_id.
- location_id.
- expected_sku.
- detected_sku.
- fill_state.
- fill_percentage.
- confidence_score.
- image evidence reference.
- review decision.
- reviewer_id if reviewed.
- model_version_id.
- event severity.
- created_at.

## Candidate Rules

Send to Phase 2 when:

- event_type is empty_location or low_stock.
- review_status is approved or auto_accepted.
- location is active.
- location allows replenishment.
- expected SKU is known.

Do not send when:

- review_status is pending.
- fill_state is blocked or unknown.
- location_id is missing.
- safety hold exists for the zone.
- SKU mismatch is unresolved.

## Phase 2 Inputs Needed

Phase 2 will need additional data:

- Source inventory locations.
- Available quantity.
- Replenishment priority rules.
- Product dimensions and weight.
- Handling class.
- Labor/robot/forklift availability.
- WMS task creation method.
- Approval thresholds.

## Phase 2 Readiness Gate

Proceed only when:

- Phase 1 detection quality is accepted.
- Replenishment candidate format is approved.
- WMS/task integration is ready for controlled testing.
- Human approval process is defined.
- Product movement method is selected by SKU class.

