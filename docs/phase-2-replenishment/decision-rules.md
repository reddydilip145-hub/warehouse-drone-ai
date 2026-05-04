# Replenishment Decision Rules

## Candidate Eligibility

Create a replenishment candidate only when:

- Phase 1 event is approved or auto_accepted.
- Event type is empty_location or low_stock.
- Target location is active.
- Target location is replenishment eligible.
- Expected SKU is known.
- No unresolved SKU mismatch exists.
- No safety hold exists for the zone.

Reject or hold when:

- Image is blocked or unknown.
- Review status is pending.
- Expected SKU is missing.
- Location has already been replenished.
- Another open recommendation exists for the same location and SKU.

## Quantity Recommendation

Recommended quantity should be based on:

- Target location max capacity.
- Estimated fill percentage.
- Minimum threshold.
- Case pack size.
- Available source inventory.
- Current wave/order demand if available.
- Handling constraints.

Suggested simple pilot formula:

```text
needed_quantity = max_capacity - estimated_current_quantity
recommended_quantity = round_to_case_pack(needed_quantity)
```

For empty locations:

```text
estimated_current_quantity = 0
```

For low-stock locations:

```text
estimated_current_quantity = max_capacity * fill_percentage / 100
```

## Priority Scoring

Score each recommendation from 0 to 100.

| Factor | Example Weight |
| --- | --- |
| Empty vs low-stock | 25 |
| SKU demand velocity | 20 |
| Current order impact | 20 |
| Time since detection | 10 |
| Source inventory availability | 10 |
| Location criticality | 10 |
| Manual override | 5 |

Priority bands:

| Score | Priority |
| --- | --- |
| 80-100 | critical |
| 60-79 | high |
| 40-59 | medium |
| 0-39 | low |

## Approval Rules

Auto-approval may be allowed only when all are true:

- Detection confidence is above approved threshold.
- SKU is confirmed.
- Quantity is below configured limit.
- Execution method is human or standard WMS task.
- No safety hold exists.
- Location has no open exception.

Human approval is required when:

- Confidence is below auto-approval threshold.
- SKU mismatch is suspected.
- Product is heavy, fragile, liquid, refrigerated, frozen, or hazardous.
- Task requires drone/robot/forklift execution.
- Recommendation is critical and affects a high-value zone.
- Source inventory conflict exists.

## Execution Method Selection

Use product and operational constraints to select method.

| Condition | Recommended Method |
| --- | --- |
| Standard case goods | Human or forklift task |
| Pallet-level movement | Forklift or AGV |
| Small lightweight item | Drone or AMR candidate |
| Heavy case | Forklift, AMR, or human team |
| Fragile product | Human or soft-grip robotics |
| Liquid cases | Human, forklift, or AMR |
| Frozen/chilled | Specialized workflow only |
| Hazardous | Exclude from automation pilot |
| High human traffic | Human task or delayed automation |

## Completion Verification

After a task is marked complete:

- Request Phase 1 re-inspection for target location.
- Compare expected fill state against actual result.
- Mark verification passed, failed, or needs review.
- Feed verification failures back into the recommendation queue.

