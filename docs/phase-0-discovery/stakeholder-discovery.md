# Stakeholder Discovery

## Required Stakeholders

| Group | Role In Phase 0 | Required Sign-Off |
| --- | --- | --- |
| Warehouse operations leader | Confirms business goals, pilot zone, workflows, and success criteria | Yes |
| Inventory control manager | Confirms inventory audit process, exception handling, and data accuracy requirements | Yes |
| Safety/compliance owner | Approves drone operating constraints, no-fly zones, and incident procedures | Yes |
| IT/cloud architect | Confirms cloud, network, identity, and deployment constraints | Yes |
| WMS/ERP owner | Confirms integration method and data ownership | Yes |
| Security owner | Confirms access control, data retention, audit, and device security | Yes |
| Maintenance/facility team | Provides physical layout, rack constraints, charging areas, and facility limitations | Recommended |
| Shift supervisors | Validate real-world aisle traffic, timing, and manual processes | Recommended |
| Finance/business sponsor | Confirms ROI assumptions and pilot funding | Recommended |

## Interview Questions

### Operations

- Which zones have the highest pain from empty racks or missed replenishment?
- How many manual inspections happen per day or week?
- What is the average time between an empty rack being noticed and resolved?
- Which products are most critical for the pilot?
- Which times are safest for drone inspection?
- Which areas should be excluded from initial drone flights?

### Inventory Control

- What is the current location accuracy?
- How are SKU-location mismatches corrected?
- How often does cycle counting happen?
- What confidence level is required before creating a replenishment task?
- What evidence is required for audit or dispute resolution?

### WMS/ERP

- Which system is the source of truth for SKU-location data?
- Can the system expose inventory and location data through APIs?
- Are updates event-based, batch-based, or manual?
- Can external systems create replenishment tasks?
- What identifiers are stable across systems?

### Safety

- What certifications or approvals are required for indoor drones?
- What are the emergency stop procedures?
- What areas are forbidden for flight?
- What is the required distance from workers, forklifts, sprinklers, and rack structures?
- What incident logging is required?

### IT And Security

- Which cloud provider is preferred?
- Is Kubernetes allowed?
- Are edge devices allowed on the corporate network?
- How are device identities managed?
- What encryption and retention policies apply to images?
- Are warehouse images considered sensitive data?

## Sign-Off Checklist

- Business sponsor approves pilot objective.
- Operations approves pilot zone.
- Safety approves feasibility constraints.
- IT approves target architecture direction.
- Security approves image and device data handling.
- WMS/ERP owner approves integration path.
- Inventory owner approves inspection event fields.

