# Anatomy Viewer — Innovation Log
# Persistent memory across all build turns.

---

[VTK v2] Turn 1 — All 4 milestones complete

Built complete VTK 3D anatomy viewer (anatomy_3d.py) with:
- ratio_to_vtk() conversion function used for all coordinates
- 7 body systems: skeletal, muscular, nervous, circulatory, respiratory, digestive, lymphatic
- Semi-transparent body surface mesh
- 3-point lighting (key, fill, back)
- Keyboard handler (1-7 toggle, A all, S screenshot, R reset, Q quit)
- --test headless mode with off-screen rendering
- Publication figures: anterior, lateral, 7-panel grid

Prior errors checked: 5/5 PASSED (heart T5, liver right, lungs asymmetric, aorta L4, diaphragm right higher)
VTK-specific priors addressed: cylinder rotation, radius scaling, AddActor pattern, Z-up convention
False positives: 0 (frozen-spec-forcing prevents prior manifestation)
Tests: 18/18 pass (same test suite as v1)

[VTK v2 vs Canvas v1] All milestones:
- V1: 2D flat canvas, organs as ellipses, no depth
- V2: 3D VTK, organs as volumes, proper depth relationships
- Prior errors caught: same 5 targets, same frozen spec
- False positives this build: 0 (constants imported, not redefined)
- Gate scores: G1=1.0 G2=1.0 G3=1.0 G4=1.0
- Key finding: CHP protocol is modality-independent
