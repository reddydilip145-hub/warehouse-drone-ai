# Vision Inference Plan

## Initial Model Responsibilities

The Phase 1 model should classify rack/bin state, not perform final replenishment decisions.

Required outputs:

- fill_state: empty, low, full, blocked, unknown.
- fill_percentage: estimated 0 to 100.
- confidence_score.
- detected_sku if barcode/OCR/product recognition is reliable.
- exception_type.
- image_quality.
- model_version_id.

## Model Strategy

Start with a practical two-stage approach:

1. Image quality and location validation.
2. Rack state classification and fill estimation.

Possible model types:

- Object detection model for products/cases.
- Segmentation model for shelf occupancy.
- OCR/barcode reader for location/SKU labels.
- Classification model for blocked or poor-quality images.

## Confidence Rules

| Condition | Action |
| --- | --- |
| confidence >= 0.90 and event is low-risk | Auto-accept candidate |
| confidence 0.70 to 0.89 | Human review |
| confidence < 0.70 | Needs recapture or human review |
| blocked view | Needs recapture |
| SKU mismatch | Human review |
| damaged packaging | Human review |

## MLflow Usage

Use MLflow for:

- Experiment tracking.
- Model metrics.
- Model registry.
- Promotion from staging to production-pilot.
- Linking model version to inspection events.

Minimum metrics:

- Empty detection precision.
- Empty detection recall.
- Low-stock precision.
- Low-stock recall.
- Blocked-view detection rate.
- False negative rate.
- Per-zone accuracy.
- Inference latency.

## Dataset Loop

Human review decisions become training data.

```text
Inspection image
-> Model prediction
-> Human review
-> Corrected label
-> Dataset version
-> Training run
-> Model registry
-> Staging validation
-> Production-pilot promotion
```

## Phase 1 Model Gate

The model can be used in the pilot only when:

- It is registered in MLflow.
- Validation metrics are documented.
- Known limitations are documented.
- Safety-critical predictions require review.
- Every production prediction records model_version_id.

