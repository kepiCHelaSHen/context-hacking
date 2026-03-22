<!-- STATUS: run | DATE: 2026-03-21 | OUTPUT: experiments/anatomy-viewer-vtk/ -->
---
name: chp-anatomy-viewer-vtk
description: "Build a verified 3D anatomical viewer using VTK — organ positions enforced by Gray's Anatomy data."
tools: Read, Write, Edit, Bash
---

# CHP Anatomy Viewer v2 — VTK 3D Renderer

You are building a medically-accurate 3D anatomy viewer using VTK (Visualization
Toolkit) — the same library used in hospital PACS systems and surgical planning
software.

The frozen spec is IDENTICAL to v1. The organ positions, proportions, prior-error
targets, and sigma gates are unchanged. The only difference is the renderer:
  v1 = HTML5 Canvas (2D, flat)
  v2 = VTK + matplotlib (3D, interactive, publication-quality)

This is a controlled comparison. Same biology, different technology.

================================================================================
STEP 0 — READ EVERYTHING BEFORE WRITING A SINGLE LINE
================================================================================

Read ALL of these in order:

  1. experiments/anatomy-viewer/frozen/anatomy_spec.md      <- THE LAW (same as v1)
  2. experiments/anatomy-viewer/frozen/anatomy_constants.py <- exact numbers (same as v1)
  3. experiments/anatomy-viewer/spec.md                     <- milestones (adapted below)
  4. experiments/anatomy-viewer/tests/test_anatomy.py       <- gates (same as v1)
  5. experiments/anatomy-viewer/dead_ends.md                <- don't repeat
  6. experiments/anatomy-viewer/state_vector.md             <- where you are

Do not write any code until you have read all six files.

================================================================================
FROZEN SPEC — ABSOLUTE RULE (same as v1)
================================================================================

Every 3D coordinate MUST trace to frozen/anatomy_spec.md or
frozen/anatomy_constants.py.

The frozen spec defines Y positions as fractions of total figure height H.
For VTK: use a canonical figure height of H = 1.80 metres (adult reference).
Convert: vtk_z = (1.0 - ratio) * 1.80  (z=0 at feet, z=1.80 at top of head)
         vtk_x = offset_ratio * 1.80
         vtk_y = depth offset (anterior-posterior axis)

This conversion must be done in a single function. Never inline the math.

================================================================================
TECHNOLOGY STACK
================================================================================

Primary: VTK (Visualization Toolkit)
  pip install vtk

Secondary: matplotlib (for 2D cross-section views)
  pip install matplotlib numpy

Output files:
  experiments/anatomy-viewer-vtk/anatomy_3d.py   <- main viewer script
  experiments/anatomy-viewer-vtk/figures/        <- rendered PNG exports

The viewer runs as:
  python experiments/anatomy-viewer-vtk/anatomy_3d.py

It opens a VTK render window with:
  - 3D rotating figure
  - System toggle via keyboard (1-7 keys, one per system)
  - Mouse rotation, zoom, pan
  - Press 'S' to save current view as PNG to figures/

ALSO generate static publication figures:
  figures/vtk_anterior.png    <- anterior view, all systems
  figures/vtk_systems_grid.png <- 7-panel grid, one system each
  figures/vtk_lateral.png     <- right lateral view

================================================================================
VTK ARCHITECTURE
================================================================================

The script must follow this structure:

  anatomy_3d.py
  ├── imports and frozen constants (from anatomy_constants.py)
  ├── ratio_to_vtk(ratio_y, offset_x=0, depth_y=0) -> (x, y, z)
  ├── build_skeleton(renderer, active_systems)
  ├── build_circulatory(renderer, active_systems)
  ├── build_respiratory(renderer, active_systems)
  ├── build_digestive(renderer, active_systems)
  ├── build_nervous(renderer, active_systems)
  ├── build_muscular(renderer, active_systems)
  ├── build_lymphatic(renderer, active_systems)
  ├── build_body_surface(renderer)     <- semi-transparent skin mesh
  ├── AnatomyInteractor(vtk.vtkInteractorStyle)  <- keyboard handler
  └── main()

No circular imports. Each build_* function is independent.
All build_* functions take renderer and active_systems set as arguments.

================================================================================
VTK PRIMITIVES — USE THESE, NOT OTHERS
================================================================================

Organs (solid volumes):
  vtkSphereSource     — brain, lymph nodes, heart ventricles
  vtkCylinderSource   — trachea, long bones (femur, humerus)
  vtkEllipsoidSource  — OR vtkSphereSource with SetRadius(rx, ry, rz) for:
                        lungs, liver, kidneys, stomach, spleen
  vtkTubeFilter       — blood vessels, nerves, thoracic duct
  vtkLineSource       — to create centerlines for TubeFilter

Body surface:
  vtkCapsuleSource    — torso, head, thigh segments
  vtkCylinderSource   — arm and leg segments
  Opacity: 0.08 (barely visible, like seeing through skin)
  Color: (0.94, 0.82, 0.72) — skin tone

Vertebral column:
  vtkCubeSource       — individual vertebrae
  Place along bezier curve path (cervical lordosis, thoracic kyphosis, lumbar lordosis)

Ribs:
  vtkArcSource + vtkTubeFilter — arc the ribs properly
  12 pairs, arc from spine, curve anterior

Muscle sheets:
  vtkPlaneSource + warp — for flat muscles (pectoralis, latissimus)
  Low-opacity: 0.4

For each actor:
  actor.GetProperty().SetColor(r, g, b)    <- from COLORS frozen spec
  actor.GetProperty().SetOpacity(opacity)
  actor.GetProperty().SetSpecular(0.3)
  actor.GetProperty().SetSpecularPower(20)

================================================================================
COORDINATE SYSTEM
================================================================================

  x = left-right (negative = anatomical left = viewer's right in anterior view)
  y = anterior-posterior (positive = anterior / front)
  z = inferior-superior (0 = feet, 1.80 = top of head)

Conversion from frozen spec ratios:
  z = (1.0 - ratio_y) * 1.80
  x = offset_x_ratio * 1.80
  y = depth (fixed per structure, see below)

Depth values (y axis — anterior to posterior):
  Skin surface anterior:  y = +0.12
  Heart:                  y = +0.05
  Lungs (center):         y = +0.00
  Spine:                  y = -0.08
  Kidneys (retroperitoneal): y = -0.06
  Skin surface posterior: y = -0.12

================================================================================
YOUR THREE ROLES — RUN IN SEQUENCE EACH TURN
================================================================================

BUILDER (first):
  Read frozen spec. Write VTK code. Every coordinate from the spec.
  Use ratio_to_vtk() for every position. Never hardcode (x, y, z) directly.
  Self-critique: run the prior-error checks manually before submitting.

CRITIC (second — The Pessimist):
  Same five prior-error targets as v1:
    1. Heart Z position: ratio_to_vtk(HEART_CENTER_Y) must give z >= 1.08m
       (0.355 * 1.80 = 0.639m from feet = 1.161m from top... wait:
        z = (1.0 - 0.355) * 1.80 = 1.161m)
       LLM prior: z = (1.0 - 0.310) * 1.80 = 1.242m (too high = T3 level)
       If heart z > 1.20m: BLOCKING — heart placed at T3, not T5.

    2. Liver X position: liver_x = LIVER_CENTER_X * 1.80 = +0.108m (positive = right)
       If liver_x < 0: BLOCKING — liver on wrong side.

    3. Right lung larger: right lung radii must exceed left lung radii.
       RIGHT_LUNG_HEIGHT * 1.80 > LEFT_LUNG_HEIGHT * 1.80.
       If equal: BLOCKING.

    4. Aorta bifurcation Z: (1.0 - 0.535) * 1.80 = 0.837m from feet
       LLM prior: (1.0 - 0.510) * 1.80 = 0.882m (too high = L3)
       If bifurcation z > 0.86m: BLOCKING.

    5. Diaphragm: right dome must be at higher Z than left dome.
       If symmetric: BLOCKING.

  Score 4 gates:
    Gate 1 (frozen compliance, must=1.0): Frozen files unmodified?
    Gate 2 (architecture, must>=0.85): VTK window opens? Keyboard works?
                                        ratio_to_vtk() used consistently?
    Gate 3 (scientific validity, must>=0.85): All 5 prior checks pass?
    Gate 4 (drift, must>=0.85): Still a VTK anatomy viewer?

REVIEWER (third — The Linter):
  Check: no hardcoded (x,y,z) tuples — all via ratio_to_vtk().
  Check: each build_* function is self-contained (no shared state).
  Check: figures/ directory created before save attempts.
  Check: VTK actors properly added to renderer (actor not just created).

================================================================================
THE LOOP
================================================================================

TURN START:
  1. Read dead_ends.md
  2. Read state_vector.md
  3. Read innovation_log.md last entry

BUILD:
  4. Implement next milestone
  5. All coordinates via ratio_to_vtk() using frozen constants
  6. Write to experiments/anatomy-viewer-vtk/anatomy_3d.py

SELF-CRITIQUE:
  7. Print the heart Z coordinate. Is it ~1.161? (Should be, T5 level)
  8. Print the liver X coordinate. Is it positive?
  9. Check right_lung vs left_lung radius
  10. Check aorta bifurcation Z

CRITIC REVIEW:
  11. Score 4 gates
  12. Check all 5 prior errors — same targets as v1
  13. BLOCKING if any prior error present

TESTS:
  14. python -m pytest experiments/anatomy-viewer/tests/ -v
      (tests work against both v1 and v2 — same frozen constants)
  15. python experiments/anatomy-viewer-vtk/anatomy_3d.py --test
      (headless mode: render one frame, save to figures/vtk_test.png, exit)

UPDATE LOGS:
  16. Append to experiments/anatomy-viewer/innovation_log.md
      Tag each entry "[VTK v2]" to distinguish from v1 entries
  17. Update state_vector.md

================================================================================
MILESTONE 1 — VTK ENVIRONMENT + BODY SURFACE
================================================================================

Install and verify:
  pip install vtk matplotlib numpy
  python -c "import vtk; print(vtk.vtkVersion.GetVTKVersion())"
  If version < 9.0: log dead end "vtk < 9.0 — capsule source unavailable"
  Use vtkCylinder + vtkSphere combination instead for body segments.

Build the basic VTK window:
  - Renderer: black background (0.05, 0.05, 0.08)
  - RenderWindow: 800x900
  - Interactor with AnatomyInteractor style
  - Lighting: 3-point (key, fill, back) — see lighting spec below

Lighting spec:
  Key light:  position (2, 3, 4),  intensity 1.0, warm white (1.0, 0.98, 0.90)
  Fill light: position (-2, 1, 2), intensity 0.4, cool blue  (0.85, 0.90, 1.0)
  Back light: position (0, -3, 1), intensity 0.3, neutral    (1.0, 1.0, 1.0)

Body surface (semi-transparent skin):
  Head:    vtkSphereSource at ratio_to_vtk(0.072, 0, 0.02),  radius=0.13
  Torso:   vtkCylinderSource at ratio_to_vtk(0.42, 0, 0),    height=0.55, radius=0.14
  Pelvis:  vtkSphereSource at ratio_to_vtk(0.54, 0, 0),      radius=0.09
  Thighs:  vtkCylinderSource x2 at ratio_to_vtk(0.67, ±0.09, 0), height=0.44
  Legs:    vtkCylinderSource x2 at ratio_to_vtk(0.88, ±0.09, 0), height=0.42
  Arms:    vtkCylinderSource x2 at ratio_to_vtk(0.40, ±0.22, 0), height=0.26
  Forearms:vtkCylinderSource x2 at ratio_to_vtk(0.55, ±0.22, 0), height=0.22

  All skin actors: opacity=0.08, color=(0.94, 0.82, 0.72)

Keyboard handler (AnatomyInteractor):
  Key '1' -> toggle skeletal
  Key '2' -> toggle muscular
  Key '3' -> toggle nervous
  Key '4' -> toggle circulatory
  Key '5' -> toggle respiratory
  Key '6' -> toggle digestive
  Key '7' -> toggle lymphatic
  Key 'a' -> toggle all systems
  Key 's' -> save current view PNG to figures/
  Key 'r' -> reset camera to anterior view
  Key 'q' or Escape -> quit

  When a system is toggled OFF: set all its actors' visibility to False
  When toggled ON: set visibility to True

CLI flag --test:
  import sys
  if '--test' in sys.argv:
      # render one frame, save figure, exit without showing window
      render_window.OffScreenRenderingOn()
      render_window.Render()
      save_screenshot('figures/vtk_test.png')
      sys.exit(0)

Milestone 1 complete when:
  - python anatomy_3d.py --test exits without error
  - figures/vtk_test.png created and non-empty
  - Body surface visible as faint skin mesh

================================================================================
MILESTONE 2 — SKELETAL SYSTEM IN 3D
================================================================================

Skull:
  vtkSphereSource at ratio_to_vtk(BRAIN_CENTER_Y, 0, 0.01)
  radius=0.12
  Color: COLORS['skeletal'] parsed as RGB

Vertebral column:
  Generate bezier path for spinal curvatures:
    cervical (C1_Y to T1_Y): lordosis — peak at x=+0.015 (anterior)
    thoracic (T1_Y to T12_Y): kyphosis — peak at x=-0.020 (posterior)
    lumbar (T12_Y to L5_Y): lordosis — peak at x=+0.015 (anterior)

  Place vtkCubeSource for each vertebra along this path.
  Cervical: 7 cubes, size (0.025, 0.025, 0.015)
  Thoracic: 12 cubes, size (0.028, 0.028, 0.014)
  Lumbar:   5 cubes,  size (0.035, 0.035, 0.016)

Ribcage:
  For each of 12 ribs (bilateral, so 24 arcs):
    z = T1_Y_vtk to T12_Y_vtk, evenly spaced
    Use vtkArcSource: center=(0, -0.08, rib_z), angle=180 degrees
    Radius decreases from rib 1 (0.14m) to rib 12 (0.09m)
    Wrap in vtkTubeFilter, radius=0.008
  True ribs (1-7): extend arc to sternum x position
  False/floating (8-12): shorter arc, no sternum connection

Sternum:
  vtkCylinderSource at x=0, y=+0.10
  z center = midpoint of STERNUM_TOP_Y and STERNUM_BOTTOM_Y in VTK coords
  height = (STERNUM_BOTTOM_Y - STERNUM_TOP_Y) * 1.80
  radius = STERNUM_WIDTH * 1.80 / 2

Long bones:
  Femur (x2): vtkCylinderSource, length = THIGH_RATIO * 1.80
  Tibia (x2): length = LOWER_LEG_RATIO * 1.80 * 0.8
  Fibula (x2): same z, offset x by 0.015, radius 0.006
  Humerus (x2): length = UPPER_ARM_RATIO * 1.80
  Radius/Ulna (x2): length = FOREARM_RATIO * 1.80

Pelvis:
  vtkSphereSource, radiusX=0.12, radiusY=0.08, radiusZ=0.07

Milestone 2 complete when:
  - Full skeleton visible in 3D
  - Spinal curvatures visible (not straight line)
  - Rib cage has arched ribs
  - All tests in TestProportions pass

================================================================================
MILESTONE 3 — ORGAN SYSTEMS (the false positive milestone)
================================================================================

This milestone WILL trigger the heart-position prior. Expected and documented.

CIRCULATORY:
  Heart:
    pos = ratio_to_vtk(HEART_CENTER_Y, HEART_CENTER_X_OFF, 0.04)
    NOTE: HEART_CENTER_Y = 0.355. VTK z = (1-0.355)*1.80 = 1.161m
    If you compute z > 1.20: you have the prior (T3 level). Fix it.
    Use vtkSphereSource scaled to (HEART_WIDTH*1.80, HEART_HEIGHT*1.80, HEART_WIDTH*1.80)
    Color: (0.85, 0.10, 0.10)  <- bright red for heart

  Aorta:
    vtkLineSource from heart to arch apex (AORTA_ARCH_Y)
    then down to bifurcation (AORTA_BIFURCATION_Y)
    NOTE: bifurcation z = (1-0.535)*1.80 = 0.837m. If z > 0.86: L3 prior. Fix it.
    Wrap in vtkTubeFilter, radius=0.015 (aorta ~3cm diameter)

  Iliac arteries from bifurcation to each leg, radius=0.010
  Femoral arteries down thighs, radius=0.007

RESPIRATORY:
  Left lung:
    pos = ratio_to_vtk(LEFT_LUNG_CENTER_Y, LEFT_LUNG_CENTER_X, 0.00)
    vtkSphereSource radiusX=LEFT_LUNG_WIDTH*1.80/2
                    radiusY=0.07
                    radiusZ=LEFT_LUNG_HEIGHT*1.80/2
    opacity=0.55, color=(0.60, 0.75, 0.90)

  Right lung:
    pos = ratio_to_vtk(RIGHT_LUNG_CENTER_Y, RIGHT_LUNG_CENTER_X, 0.00)
    radiusZ = RIGHT_LUNG_HEIGHT*1.80/2  <- MUST be > left lung radiusZ
    Same color, same opacity

  NOTE: If right radiusZ <= left radiusZ: equal-lung prior. Fix it.
  Diaphragm right dome: z slightly higher than left dome. Use two separate actors.
  Trachea: vtkCylinderSource from z=1.50 down to z=1.26 (T4 level), radius=0.009

DIGESTIVE:
  Liver:
    x = LIVER_CENTER_X * 1.80   <- MUST be positive (right side)
    NOTE: If x < 0: left-liver prior. Fix it.
    vtkSphereSource radiusX=LIVER_WIDTH*1.80/2
                    radiusY=0.06
                    radiusZ=LIVER_HEIGHT*1.80/2
    opacity=0.7, color=(0.60, 0.25, 0.15)

  Stomach: left side, ellipsoid
  Small intestine: coiled tube (multiple vtkTubeFilter segments)
  Large intestine: rectangular frame of tubes

NERVOUS:
  Brain: vtkSphereSource at ratio_to_vtk(BRAIN_CENTER_Y, 0, 0.01)
         radiusX=BRAIN_WIDTH*1.80/2, radiusZ=BRAIN_HEIGHT*1.80/2
         opacity=0.8, color=(0.85, 0.80, 0.92)
  Spinal cord: thin vtkTubeFilter (radius=0.007) following vertebral bezier path

MUSCULAR:
  Pectoralis major (x2): vtkPlaneSource warped to chest curvature, opacity=0.45
  Deltoids: rounded ellipsoids at shoulder
  Rectus abdominis: series of ellipsoids down midline (6-pack)
  Trapezius: large flat triangle posterior
  Latissimus dorsi: wing-shaped, posterior torso
  Gluteus maximus: large ellipsoids posterior pelvis
  Quadriceps / Hamstrings: cylinders around femur

LYMPHATIC:
  Thymus: ellipsoid at ratio_to_vtk(0.250, 0, 0.05)
  Spleen: ellipsoid at ratio_to_vtk(SPLEEN_CENTER_Y, SPLEEN_CENTER_X, -0.02)
  Thoracic duct: thin tube from abdomen to left subclavian
  Lymph nodes: small spheres (radius=0.012) at axilla, groin, neck

FALSE POSITIVE PROTOCOL:
  Before moving on, explicitly print to stdout:
    "SELF-CHECK: heart z = {z:.3f}m (should be 1.161m for T5)"
    "SELF-CHECK: liver x = {x:.3f}m (should be +0.108m, right side)"
    "SELF-CHECK: right_lung_rz = {rz:.3f}m > left_lung_rz = {lz:.3f}m: {rz > lz}"
    "SELF-CHECK: bifurcation z = {z:.3f}m (should be 0.837m for L4)"
  If any check fails: BLOCKING. Document it. Fix it. Re-run checks.

Milestone 3 complete when:
  - All 5 SELF-CHECK lines print correct values
  - All TestPriorErrors tests pass
  - At least one false positive caught and logged

================================================================================
MILESTONE 4 — PUBLICATION FIGURES
================================================================================

Generate 3 static publication-quality PNG renders:

  figures/vtk_anterior.png (800x900)
    Camera: position (0, 4, 0.9), focal_point (0, 0, 0.9), up=(0,0,1)
    All systems visible, skin very transparent
    White background for publication

  figures/vtk_systems_grid.png (1600x900)
    7-panel grid using matplotlib imshow
    Each panel: one system active, others hidden
    Label each panel with system name and frozen color
    Use subprocess to render each system separately headless

  figures/vtk_lateral.png (800x900)
    Camera: position (4, 0, 0.9), focal_point (0, 0, 0.9), up=(0,0,1)
    Right lateral view
    White background

For white background renders:
  renderer.SetBackground(1.0, 1.0, 1.0)
  renderer.SetBackground2(0.95, 0.95, 0.97)
  renderer.GradientBackgroundOn()

Save PNG using vtkWindowToImageFilter + vtkPNGWriter.

Milestone 4 complete when:
  - All 3 PNG files exist and are > 50KB
  - Interactive viewer opens with keyboard controls working
  - All tests pass

================================================================================
VTK-SPECIFIC PRIOR ERRORS (additional to v1 prior errors)
================================================================================

These are errors specific to the 3D/VTK implementation.
The Critic checks these IN ADDITION to the 5 from the frozen spec.

  VTK-PRIOR-1: Cylinder default orientation
    vtkCylinderSource default axis is Y.
    Bones must be Z-axis aligned (superior-inferior).
    If femur renders horizontal: cylinder not rotated. Fix: SetOrientationWXYZ(90, 1, 0, 0)

  VTK-PRIOR-2: Sphere radius not scaled
    vtkSphereSource radius is in VTK world units (metres here).
    LLM prior: uses ratio directly as radius (e.g., heart radius=0.080 instead of 0.080*1.80/2=0.072m)
    Fix: always multiply by 1.80 and divide by 2.

  VTK-PRIOR-3: Actor not added to renderer
    LLM sometimes creates actor but forgets renderer.AddActor(actor).
    Reviewer check: every build_* function must end with renderer.AddActor() calls.

  VTK-PRIOR-4: Wrong coordinate system (Z up vs Y up)
    VTK default: Y is up. This viewer uses Z-up convention.
    If figure is lying down: camera not set correctly or cylinder orientations wrong.
    Camera must use up_vector=(0, 0, 1).

================================================================================
COMPARISON WITH V1 (document in innovation log)
================================================================================

After each milestone, log a comparison entry in innovation_log.md:

  "[VTK v2 vs Canvas v1] Milestone N:
   - V1: 2D flat canvas, organs as ellipses, no depth
   - V2: 3D VTK, organs as volumes, proper depth relationships
   - Prior errors caught: same 5 targets, same frozen spec
   - False positives this milestone: [list]
   - Gate scores: G1=[x] G2=[x] G3=[x] G4=[x]"

This comparison IS the science. Two different implementations,
same frozen spec, same prior errors caught. That is the CHP protocol
demonstrating modality-independence of the Prior-as-Detector layer.

================================================================================
SELF-CRITIQUE CHECKLIST (run before reporting milestone complete)
================================================================================

  [ ] Did ratio_to_vtk() conversion function exist and is it used everywhere?
  [ ] Did I print all 4 SELF-CHECK lines? Do they show correct values?
  [ ] Heart z = ~1.161m (T5)?
  [ ] Liver x = positive (right side)?
  [ ] Right lung radiusZ > left lung radiusZ?
  [ ] Aorta bifurcation z = ~0.837m (L4)?
  [ ] Diaphragm right dome z > left dome z?
  [ ] Cylinders (bones) rotated to Z-axis?
  [ ] All actors added to renderer?
  [ ] figures/ directory exists?
  [ ] --test flag works headlessly?
  [ ] python -m pytest experiments/anatomy-viewer/tests/ -v — all pass?

================================================================================
EXIT
================================================================================

When all 4 milestones complete and all tests pass, write:
  experiments/anatomy-viewer-vtk/REPORT.md

Include:
  - VTK version used
  - Which prior errors fired (expected: heart position, cylinder orientation)
  - Which turn each was caught
  - What VTK-specific priors fired beyond the 5 anatomical ones
  - Comparison with v1 (Canvas): same prior errors, different renderer, same frozen spec
  - Final gate scores
  - File sizes of generated PNGs

Then print:
  "VTK anatomy viewer complete. anatomy_3d.py ready.
   Run: python experiments/anatomy-viewer-vtk/anatomy_3d.py
   False positives caught: [N] anatomical + [M] VTK-specific. See REPORT.md."
