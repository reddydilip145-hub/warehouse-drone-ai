# Warehouse Mapping Plan

## Location Hierarchy

Use a stable hierarchy that can support drones, WMS integration, and future replenishment automation.

Recommended hierarchy:

```text
Facility
-> Building/Area
-> Temperature Zone
-> Aisle
-> Rack
-> Bay
-> Shelf Level
-> Bin/Slot
-> Facing/Position
```

## Core Location Fields

| Field | Purpose |
| --- | --- |
| facility_id | Identifies warehouse site |
| zone_id | Groups dry, chilled, freezer, staging, dock, or restricted zones |
| aisle_id | Main navigation unit |
| rack_id | Physical rack identifier |
| bay_id | Horizontal rack section |
| shelf_level | Vertical shelf position |
| bin_id | Operational pick/storage location |
| expected_sku | SKU expected at this location |
| max_capacity | Expected physical capacity |
| coordinate_x | Digital twin x-coordinate |
| coordinate_y | Digital twin y-coordinate |
| coordinate_z | Height or shelf elevation |
| qr_marker_id | Visual marker for localization if used |
| rfid_zone_id | RFID zone reference if used |
| flight_allowed | Whether drone flight is permitted |
| inspection_required | Whether this location belongs to inspection scope |

## Zone Categories

Classify every warehouse area.

| Zone Type | Automation Recommendation |
| --- | --- |
| Dry grocery | Best starting pilot |
| Refrigerated | Later phase after battery and condensation validation |
| Freezer | Later phase; higher risk and special equipment needed |
| Chemical or hazardous | Exclude from pilot |
| Dock/staging | Use only for observation; high movement variability |
| Forklift-heavy aisle | Avoid in first pilot unless flights happen during controlled windows |
| Human picking zone | Require stricter safety rules |
| Charging area | Required for drone operation |
| Emergency exit/safety equipment | No-fly and no-obstruction zone |

## Mapping Tasks

1. Collect existing CAD drawings, WMS location files, rack lists, and aisle maps.
2. Validate the physical location structure against actual warehouse labels.
3. Identify missing, duplicate, or inconsistent location IDs.
4. Capture aisle width, rack height, shelf depth, lighting, and obstructions.
5. Assign each rack/bin to a coordinate model.
6. Mark no-fly zones and controlled flight corridors.
7. Select pilot zone candidates.
8. Validate pilot zone with operations, safety, and IT.

## Pilot Zone Scoring

Score each candidate zone from 1 to 5.

| Criterion | Weight |
| --- | --- |
| Safety simplicity | High |
| Rack label quality | High |
| Lighting quality | High |
| SKU visibility | High |
| Operational value | High |
| Low disruption risk | Medium |
| Wi-Fi/network quality | Medium |
| Manual validation ease | Medium |
| Future scalability | Medium |

## Mapping Deliverables

- Location master file.
- Pilot-zone map.
- No-fly zone map.
- Flight corridor assumptions.
- Rack/bin photo reference set.
- Data quality issue log.
