# Phase 0 Discovery Package

## Purpose

Phase 0 prepares the warehouse automation program before drones, ML models, or replenishment automation are implemented. The goal is to create a reliable operational, technical, and safety baseline for a C&S-scale grocery warehouse.

Phase 0 answers five questions:

1. What exactly exists in the warehouse today?
2. Where are racks, bins, SKUs, people, forklifts, and restricted zones?
3. Which systems own inventory, tasks, orders, and product master data?
4. What conditions must the drone inspection system handle safely?
5. What evidence proves the pilot is ready for Phase 1?

## Phase 0 Outcomes

By the end of Phase 0, the project should have:

- Warehouse digital twin baseline.
- Rack, aisle, shelf, bin, SKU, and zone master data.
- Safety map with no-fly zones and controlled flight paths.
- WMS, ERP, inventory, and identity integration inventory.
- Pilot-zone selection and success criteria.
- Initial dataset strategy for rack images, labels, and inspection events.
- Architecture baseline for Phase 1 drone inspection.
- Risk register and compliance checklist.
- Approval gate to proceed into implementation.

## Recommended Duration

For a large grocery warehouse, Phase 0 should usually run for 3 to 6 weeks.

Suggested split:

- Week 1: Stakeholder interviews and current process mapping.
- Week 2: Warehouse mapping and system inventory.
- Week 3: Pilot-zone selection and data model design.
- Week 4: Safety review, integration design, and approval gate.
- Weeks 5-6: Optional deeper site validation for large or high-risk facilities.

## Workstreams

### 1. Business And Operations Discovery

Capture the current replenishment and inventory audit process.

Key questions:

- How are empty racks identified today?
- Who responds when stock is missing?
- How often are rack audits performed?
- What are the most expensive stockout scenarios?
- Which product categories are most suitable for the pilot?
- Which shifts, aisles, and zones create the least operational disruption?
- What KPIs does the client already track?

Deliverables:

- Current-state workflow.
- Pain-point summary.
- Pilot business case.
- KPI baseline.

### 2. Warehouse Mapping

Create a location model that drones and software can understand.

Required mapping:

- Facility.
- Temperature zone.
- Aisle.
- Rack.
- Bay.
- Shelf level.
- Bin or slot.
- Product facing.
- Dock doors.
- Staging areas.
- Charging/docking stations.
- Forklift routes.
- Human walking lanes.
- No-fly zones.
- Emergency exits and safety equipment.

Deliverables:

- Warehouse coordinate map.
- Rack/bin location master.
- Zone classification.
- Pilot-zone candidate list.

### 3. Systems And Integration Discovery

Identify where the system needs to read, write, or synchronize data.

Systems to inspect:

- WMS.
- ERP.
- Inventory service or database.
- Product/SKU master.
- Order management.
- Labor/task management.
- Identity and access management.
- BI/reporting tools.
- Existing barcode, QR, RFID, or scanner systems.

Deliverables:

- Integration inventory.
- API/file/database access notes.
- Data ownership matrix.
- Security and access requirements.

### 4. Drone And Safety Feasibility

Validate that indoor drone operations are physically and operationally realistic.

Assess:

- Ceiling height.
- Rack height.
- Aisle width.
- Lighting quality.
- Airflow and fans.
- Wi-Fi coverage.
- Obstructions.
- Human traffic.
- Forklift traffic.
- Battery charging locations.
- Emergency landing locations.
- Cold or freezer zones.
- Insurance and safety requirements.

Deliverables:

- Flight feasibility report.
- Safety zone map.
- Drone operating constraints.
- Pilot flight route assumptions.

### 5. Dataset And ML Readiness

Plan the dataset before collecting images.

Required dataset classes:

- Empty rack/bin.
- Low-stock rack/bin.
- Full rack/bin.
- Wrong SKU at location.
- Damaged packaging.
- Blocked view.
- Poor lighting.
- Barcode/QR visible.
- Barcode/QR not visible.
- Human/forklift present.

Minimum metadata per image:

- Image ID.
- Timestamp.
- Facility ID.
- Zone ID.
- Aisle ID.
- Rack ID.
- Shelf/bin ID.
- Expected SKU.
- Detected SKU if available.
- Camera angle.
- Drone ID.
- Lighting condition.
- Annotation status.
- Label confidence.

Deliverables:

- Dataset plan.
- Annotation guide.
- Label taxonomy.
- Data storage and retention policy.

## Phase 0 Exit Criteria

Phase 0 is complete only when all of these are true:

- Pilot warehouse zone is selected and approved.
- Rack/bin location master is available for that zone.
- Safety map and no-fly zones are documented.
- WMS/inventory integration path is identified.
- Dataset classes and annotation rules are defined.
- Initial inspection event schema is approved.
- Phase 1 KPIs are agreed with stakeholders.
- Operational sign-off is received from warehouse leadership.
- Technical sign-off is received from architecture/IT/security.
- Safety sign-off is received from the safety/compliance owner.

## Recommended Pilot Zone

Start with a dry grocery zone instead of freezer, refrigerated, chemical, or very high forklift-traffic areas.

Preferred pilot characteristics:

- Good lighting.
- Standardized racks.
- Clear location labels.
- Moderate SKU variety.
- Limited human traffic during selected flight windows.
- Low risk if automation produces a false alert.
- Easy access for manual validation.

## Next Phase Trigger

Move into Phase 1 only after the pilot zone is mapped, the first rack image dataset can be collected safely, and the inspection event schema is ready for Cloud SQL.

