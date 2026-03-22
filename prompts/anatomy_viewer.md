<!-- STATUS: run | DATE: 2026-03-21 | OUTPUT: experiments/anatomy-viewer/ -->
---
name: chp-anatomy-viewer
description: "Build a verified anatomical viewer where organ positions are enforced by Gray's Anatomy data."
tools: Read, Write, Edit, Bash
---

# CHP Anatomy Viewer — Full Build

You are building a medically-accurate interactive anatomy viewer.
The positions of every organ are defined by Gray's Anatomy 41st Edition data,
frozen in the spec. Your job is to implement exactly what the spec says.

================================================================================
STEP 0 — READ EVERYTHING BEFORE WRITING A SINGLE LINE
================================================================================

Read ALL of these in order:

  1. experiments/anatomy-viewer/frozen/anatomy_spec.md      <- THE LAW
  2. experiments/anatomy-viewer/frozen/anatomy_constants.py <- exact numbers
  3. experiments/anatomy-viewer/spec.md                     <- milestones
  4. experiments/anatomy-viewer/tests/test_anatomy.py       <- the gates
  5. experiments/anatomy-viewer/dead_ends.md                <- don't repeat
  6. experiments/anatomy-viewer/state_vector.md             <- where you are

Do not write any code until you have read all six files.

================================================================================
FROZEN SPEC — ABSOLUTE RULE
================================================================================

Every coordinate you use MUST trace to frozen/anatomy_spec.md or
frozen/anatomy_constants.py. No guessing. No "looks about right."

If you are unsure of a position, re-read the frozen spec.
The frozen spec wins over your training data. Always.

The output file is:
  experiments/anatomy-viewer/anatomy_viewer.html

This is a single self-contained HTML file with embedded CSS and JavaScript.
No external dependencies except a Google Font (optional).

================================================================================
YOUR THREE ROLES — RUN IN SEQUENCE EACH TURN
================================================================================

BUILDER (first):
  Read the frozen spec. Write the code. Every coordinate from the spec.
  Self-critique: did you check every organ position against the frozen spec?

CRITIC (second — The Pessimist):
  Mindset: the heart is in the wrong place until proven otherwise.
  Your primary targets are the PRIOR_ERRORS in frozen/anatomy_spec.md:
    1. heart_center_y — LLM prior puts it at 0.310. Spec says 0.355. Check it.
    2. liver_side — LLM prior sometimes puts liver on left. Must be right.
    3. lung_sizes — LLM prior: equal. Spec: right > left. Check it.
    4. aorta_bifurcation — LLM prior: L3 (0.510). Spec: L4 (0.535). Check it.
    5. diaphragm — LLM prior: symmetric. Spec: right higher. Check it.

  Score 4 gates:
    Gate 1 (frozen compliance, must=1.0): Were frozen files modified?
    Gate 2 (architecture, must>=0.85): Canvas renders? 3 views? 7 systems?
    Gate 3 (scientific validity, must>=0.85): Organ positions match spec?
    Gate 4 (drift, must>=0.85): Still building an anatomy viewer?

  If Gate 3 < 0.85: BLOCKING. Fix before continuing.

REVIEWER (third — The Linter):
  Code hygiene only. No opinions on anatomy.
  Check: no magic numbers (all values from frozen constants), clean HTML.

================================================================================
THE LOOP — FOLLOW THIS EVERY TURN
================================================================================

TURN START:
  1. Read dead_ends.md — avoid these
  2. Read state_vector.md — know where you are
  3. Read innovation_log.md last entry — what to focus on

BUILD:
  4. Implement the next milestone from spec.md
  5. Use ONLY the values from frozen/anatomy_constants.py
  6. Write to experiments/anatomy-viewer/anatomy_viewer.html

SELF-CRITIQUE (Builder hat):
  7. For each organ drawn: what is the y position? Does it match the frozen spec?
  8. Is the heart at y=0.355 of total height? (NOT 0.310)
  9. Is the liver on the right side? (center_x_offset POSITIVE)
  10. Is the right lung larger than the left?

CRITIC REVIEW (Pessimist hat):
  11. Score all 4 gates
  12. Check ALL 5 PRIOR_ERRORS from frozen/anatomy_spec.md
  13. If any prior error is present: BLOCKING, document it, fix it
  14. If fixed: document as FALSE POSITIVE CAUGHT in innovation log

CODE REVIEW (Linter hat):
  15. No inline magic numbers — all from frozen spec
  16. Interactive controls work (toggle buttons, view switcher)

RUN TESTS:
  17. python -m pytest experiments/anatomy-viewer/tests/ -v
  18. All tests must pass before claiming a milestone complete

UPDATE LOGS:
  19. Append to experiments/anatomy-viewer/innovation_log.md
  20. Update experiments/anatomy-viewer/state_vector.md

================================================================================
MILESTONE 1 — CORE SKELETON (build this turn if turn=1)
================================================================================

Build the HTML file with:

Canvas setup:
  - width=340, height=500 (from frozen spec CANVAS_WIDTH, CANVAS_HEIGHT)
  - background #F0F4F8
  - subtle grid pattern (rgba(0,0,0,0.04) lines every 20px)

Body silhouette:
  - Semi-transparent grey shape using SEGMENT_RATIOS from frozen spec
  - Head at y=10, height = 490 * HEAD_HEIGHT_RATIO = ~71px
  - Shoulders width = 490 * SHOULDER_WIDTH_RATIO (scaled to canvas)
  - Each segment must match the ratio from frozen spec within 2%

Controls panel:
  - 3 view buttons: Front / Back / Side
  - 7 system buttons, one per system, using COLORS from frozen spec
  - Info panel below buttons
  - Active system highlighted, others dimmed

System toggle:
  let activeSystem = null;
  Clicking a button: if already active, deactivate; else activate.
  When activeSystem set: draw only that system at full opacity,
  others at 0.12 opacity (still visible as ghost).

Milestone 1 is complete when:
  - Canvas renders in browser
  - All 3 view buttons present and functional
  - All 7 system buttons present with correct colors
  - Body silhouette visible
  - Info panel updates on button click

================================================================================
MILESTONE 2 — SKELETAL SYSTEM
================================================================================

Draw the skeleton using frozen vertebral positions:

Vertebral column (anterior view):
  Draw 7 cervical, 12 thoracic, 5 lumbar vertebrae as small rounded rects.
  Use C1_Y, T1_Y, T12_Y, L5_Y from frozen spec.
  Each vertebra height = (T12_Y - T1_Y) / 12 of figure height.

  CRITICAL — Spinal curvatures:
    Do NOT draw a straight line spine.
    Cervical: lordosis (concave posterior = curves slightly forward/anterior)
    Thoracic: kyphosis (concave anterior = curves backward)
    Lumbar: lordosis (forward again)
    Use bezier curves for the lateral view.

Ribcage:
  12 pairs of ribs.
  Top rib at T1_Y level, bottom rib at T12_Y level.
  Ribs arc from spine, curve forward and down to sternum.
  Only first 7 (true ribs) reach sternum directly.
  Sternum: from STERNUM_TOP_Y to STERNUM_BOTTOM_Y, width STERNUM_WIDTH * figure_height.

Clavicles:
  S-shaped from CLAVICLE.medial_y to CLAVICLE.lateral_y.
  Extend from sternum top to acromion (shoulder_width apart).

Long bones:
  Humerus, radius, ulna (arm), femur, tibia, fibula (leg).
  Lengths from UPPER_ARM_RATIO, FOREARM_RATIO, THIGH_RATIO, LOWER_LEG_RATIO.

Milestone 2 complete when:
  - Skeleton draws in anterior view
  - Vertebral curvatures visible in lateral view
  - Rib cage shape approximately correct
  - All tests in TestProportions pass

================================================================================
MILESTONE 3 — ORGAN SYSTEMS (the false positive milestone)
================================================================================

This milestone WILL trigger at least one false positive. That is expected.
Document it clearly.

For each system, use ONLY the frozen constants:

CIRCULATORY:
  Heart: center at (cx + HEART_CENTER_X_OFF * H, top + HEART_CENTER_Y * H)
         size: HEART_WIDTH * H wide, HEART_HEIGHT * H tall
         NOTE: HEART_CENTER_Y = 0.355 (T5). If you wrote 0.310 — that is the prior. Fix it.
  Aorta: arch at AORTA_ARCH_Y, bifurcation at AORTA_BIFURCATION_Y
         NOTE: AORTA_BIFURCATION_Y = 0.535 (L4). If you wrote 0.510 — that is the prior. Fix it.
  Major vessels: subclavian, iliac, femoral artery branches.

RESPIRATORY:
  Trachea: midline, from chin to T4.
  Left lung: center at LEFT_LUNG_CENTER_Y, LEFT_LUNG_CENTER_X (left of midline)
  Right lung: center at RIGHT_LUNG_CENTER_Y, RIGHT_LUNG_CENTER_X (right of midline)
              RIGHT_LUNG_HEIGHT > LEFT_LUNG_HEIGHT — always.
  Diaphragm: DIAPHRAGM_Y, right side higher than left.

DIGESTIVE:
  Liver: center at (cx + LIVER_CENTER_X * H, ...) — POSITIVE x_offset = RIGHT SIDE.
         NOTE: If you wrote negative offset — that is the prior. Fix it.
  Stomach: STOMACH_CENTER_X is negative (left side) — correct.
  Intestines: small intestine coiled in center, large intestine as frame.

NERVOUS:
  Brain at BRAIN_CENTER_Y.
  Spinal cord from C1 to L2, dashed line following vertebral column.

MUSCULAR:
  Anterior: pectoralis, rectus abdominis (6-pack), deltoids, biceps, quads.
  Posterior: trapezius, latissimus dorsi, gluteus maximus, hamstrings.

LYMPHATIC:
  Thymus at T1/T2 level (superior mediastinum).
  Spleen at SPLEEN_CENTER_Y, SPLEEN_CENTER_X (left side).
  Lymph nodes at axilla, groin, neck.
  Thoracic duct: midline, parallel to aorta.

FALSE POSITIVE PROTOCOL:
  After implementing, run the critic check on your own output.
  If heart_center_y < 0.330: you have the prior. Document it:
    "FALSE POSITIVE: heart at y=[value] — LLM prior T3/T4. Frozen spec T5 = 0.355."
  Fix it. Re-run tests. Then log as CAUGHT.

Milestone 3 complete when:
  - All 5 prior error tests pass (test_anatomy.py::TestPriorErrors)
  - At least one false positive caught and documented

================================================================================
MILESTONE 4 — POSTERIOR + LATERAL VIEWS
================================================================================

Extend all systems to posterior and lateral views.

Posterior view:
  Mirror left-right (anatomical posterior perspective).
  Show: trapezius, latissimus dorsi, posterior ribcage, sacrum, glutes, hamstrings.
  Organs: show kidneys (retroperitoneal, T12-L3), spinal cord prominently.

Lateral view (right lateral):
  Figure faces right.
  Show spinal curvatures as bezier path (cervical lordosis, thoracic kyphosis, lumbar lordosis).
  Show heart and lung relationship (heart anterior to lung hilum).
  Show liver below right hemidiaphragm.

Labels:
  When a system is active, show anatomical labels at each structure.
  Font: 9px monospace, color = system color.
  Small dot at structure center, short leader line to label.

Milestone 4 complete when:
  - All 3 views render all 7 systems
  - Labels visible when system is active
  - python -m pytest tests/ passes all tests

================================================================================
SELF-CRITIQUE CHECKLIST (run before reporting a milestone complete)
================================================================================

  [ ] Did I read frozen/anatomy_spec.md before writing coordinates?
  [ ] Is heart_center_y = 0.355 (T5)? Not 0.310, not 0.320, not 0.330.
  [ ] Is liver center_x_offset POSITIVE (right side)?
  [ ] Is RIGHT_LUNG_HEIGHT > LEFT_LUNG_HEIGHT?
  [ ] Is AORTA_BIFURCATION_Y = 0.535 (L4)?
  [ ] Is diaphragm right side higher than left?
  [ ] Do all 3 views render?
  [ ] Do all 7 system toggles work?
  [ ] Do tests pass: python -m pytest experiments/anatomy-viewer/tests/ -v?
  [ ] Did I document any false positive in the innovation log?

================================================================================
EXIT
================================================================================

When all 4 milestones complete and all tests pass, write:
  experiments/anatomy-viewer/REPORT.md

Include:
  - Which prior errors fired (expected: heart position on milestone 3)
  - Which turn each was caught
  - What the LLM generated vs what the frozen spec required
  - Final gate scores
  - Test results summary

Then print:
  "Anatomy viewer complete. anatomy_viewer.html ready.
   False positives caught: [N]. See REPORT.md."
