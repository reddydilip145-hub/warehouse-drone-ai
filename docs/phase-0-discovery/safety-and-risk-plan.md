# Safety And Risk Plan

## Safety Principles

The drone system should first be treated as an inspection aid, not a warehouse control authority. Phase 0 must prove that image collection can happen without increasing risk to people, equipment, inventory, or facility operations.

## Required Safety Controls

- No-fly zones.
- Controlled flight windows.
- Emergency stop process.
- Manual override.
- Drone speed and altitude limits.
- Distance rules from people, forklifts, sprinklers, and rack structures.
- Battery health monitoring.
- Incident logging.
- Pre-flight checklist.
- Post-flight inspection checklist.
- Fallback manual inspection process.

## No-Fly Zones

No-fly zones should include:

- Emergency exits.
- Fire suppression equipment.
- High forklift traffic areas.
- Dock doors during active loading.
- Human break areas.
- Maintenance zones.
- Hazardous material storage.
- Areas with poor signal or visibility.
- Any aisle marked restricted by safety leadership.

## Risk Register

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Drone collision with worker or forklift | High | Controlled routes, flight windows, sensors, emergency stop |
| Poor indoor localization | High | QR markers, visual SLAM, UWB, LiDAR validation |
| Low image quality | Medium | Lighting assessment, camera standards, repeat capture rules |
| False empty-rack detection | Medium | Confidence threshold, human review, recheck flight |
| WMS data mismatch | High | Read-only pilot first, data reconciliation process |
| Network outage | Medium | Edge buffering and retry upload |
| Battery failure | Medium | Battery telemetry, emergency landing zones |
| Cold-zone performance issues | Medium | Exclude freezer/chilled zones from pilot |
| Privacy concerns from worker images | Medium | Policy review, masking, access controls |
| Operational disruption | High | Start with limited dry zone and scheduled flights |

## Incident Procedure

Every incident or near miss should record:

- Date and time.
- Zone and aisle.
- Drone ID.
- Operator or supervising system.
- Event description.
- Images/video if available.
- Impact level.
- Immediate response.
- Root cause.
- Corrective action.
- Approval before resuming flights.

## Phase 0 Safety Exit Criteria

- Safety owner approves pilot zone.
- No-fly zones are documented.
- Emergency stop process is tested or demonstrated.
- Flight route assumptions are reviewed.
- Manual fallback process is documented.
- Incident logging workflow is defined.

