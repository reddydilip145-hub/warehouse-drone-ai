# Data And Database Plan

## Data Storage Recommendation

Use Cloud SQL for structured inspection, inventory, and task events. Store images and videos in object storage, then keep URLs or object keys in Cloud SQL.

Recommended split:

```text
Object Storage
-> Raw drone images
-> Processed images
-> Annotation files
-> Model training datasets

Cloud SQL
-> Facilities
-> Zones
-> Rack/bin locations
-> SKU master references
-> Inspection events
-> Detection results
-> Replenishment recommendations
-> Human review status
```

## Key Entities

### facility

| Field | Notes |
| --- | --- |
| facility_id | Primary identifier |
| name | Warehouse/site name |
| address | Optional |
| timezone | Needed for operations and audits |
| status | active/inactive |

### warehouse_location

| Field | Notes |
| --- | --- |
| location_id | Stable bin/rack location ID |
| facility_id | Parent facility |
| zone_id | Temperature or operational zone |
| aisle_id | Aisle |
| rack_id | Rack |
| bay_id | Bay |
| shelf_level | Shelf level |
| bin_id | Bin/slot |
| coordinate_x | Digital twin coordinate |
| coordinate_y | Digital twin coordinate |
| coordinate_z | Height |
| flight_allowed | Safety control |
| active | Current operational status |

### sku_master

| Field | Notes |
| --- | --- |
| sku_id | SKU identifier |
| upc | Barcode/UPC where available |
| description | Product name |
| category | Dry, chilled, frozen, etc. |
| case_weight | Needed for movement automation |
| dimensions | Needed for capacity and handling |
| handling_class | fragile, liquid, frozen, heavy, etc. |

### inspection_event

| Field | Notes |
| --- | --- |
| inspection_id | Primary event ID |
| facility_id | Site |
| location_id | Rack/bin inspected |
| drone_id | Inspecting drone |
| image_object_key | Object storage reference |
| captured_at | Image timestamp |
| expected_sku | From WMS/location plan |
| detected_sku | From AI/OCR/barcode if available |
| fill_state | empty/low/full/blocked/unknown |
| fill_percentage | Estimated quantity level |
| confidence_score | AI confidence |
| exception_type | empty, mismatch, damage, blocked, safety |
| review_status | pending/approved/rejected/auto_accepted |
| created_at | Event creation timestamp |

### replenishment_recommendation

| Field | Notes |
| --- | --- |
| recommendation_id | Primary ID |
| inspection_id | Source inspection |
| location_id | Target location |
| sku_id | SKU needed |
| priority | low/medium/high/critical |
| recommended_quantity | Quantity suggested |
| execution_method | human, forklift, AMR, drone, ASRS |
| approval_status | pending/approved/rejected |
| created_at | Timestamp |

## Dataset Versioning

Use explicit dataset versions:

```text
dataset-rack-inspection-v0.1
dataset-rack-inspection-v0.2
dataset-rack-inspection-v1.0
```

Each version should record:

- Source zone.
- Date range.
- Number of images.
- Label distribution.
- Annotation owner.
- Model training usage.
- Known bias or quality issues.

## Data Governance

- Do not store raw images in SQL.
- Retain raw images based on client policy.
- Blur or restrict images containing workers if required.
- Encrypt data in transit and at rest.
- Log access to inspection evidence.
- Keep model predictions auditable.
- Never overwrite inspection events; append corrections as review records.
