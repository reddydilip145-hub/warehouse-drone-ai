# Object Storage Layout

## Bucket Strategy

Use private buckets. Do not expose warehouse images publicly.

Recommended buckets:

```text
warehouse-inspection-raw
warehouse-inspection-processed
warehouse-inspection-annotations
warehouse-inspection-model-artifacts
```

## Object Key Pattern

Use deterministic object keys so evidence can be traced.

```text
raw/{facility_id}/{zone_id}/{yyyy}/{mm}/{dd}/{batch_id}/{location_id}/{image_id}.jpg
processed/{facility_id}/{zone_id}/{yyyy}/{mm}/{dd}/{batch_id}/{location_id}/{image_id}-thumbnail.jpg
annotations/{dataset_version}/{facility_id}/{zone_id}/{image_id}.json
models/{model_name}/{model_version_id}/artifact
```

## Metadata Tags

Each image object should include:

- facility_id.
- zone_id.
- location_id.
- drone_id.
- batch_id.
- route_id.
- captured_at.
- image_id.
- checksum.
- retention_class.

## Retention

Suggested pilot retention:

- Raw images: 90 to 180 days.
- Processed thumbnails: 180 days.
- Annotation files: retained with dataset version.
- Model artifacts: retained indefinitely or per client policy.
- Images containing workers: stricter retention or masking policy.

## Access Roles

| Role | Access |
| --- | --- |
| edge_uploader | Write raw images only |
| inference_service | Read raw, write processed |
| reviewer | Read signed image URLs through dashboard |
| ml_engineer | Read approved dataset images and annotations |
| auditor | Read evidence through audit workflow |

