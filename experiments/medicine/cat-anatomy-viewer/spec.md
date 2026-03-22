# Anatomy Viewer — Experiment Spec
# CHP Milestones for building a verified anatomical viewer

================================================================================
EXPERIMENT IDENTITY
================================================================================

Name:       anatomy-viewer
Domain:     Medical Anatomy / Scientific Visualization
Language:   JavaScript (HTML5 Canvas) + Python constants
Output:     anatomy_viewer.html — self-contained interactive viewer

Research question:
  Can CHP enforce anatomical accuracy in a programmatic body systems viewer
  by using published anthropometric data as a frozen spec, with the
  Prior-as-Detector layer catching the known positional errors LLMs make?

================================================================================
PRIOR-AS-DETECTOR TARGET
================================================================================

The expected false positive for this experiment:

  The Builder will generate a heart position at approximately y=0.310-0.320
  (T3/T4 level — the "upper chest" prior that dominates LLM training data).

  The frozen spec requires y=0.355 (T5 level per Gray's Anatomy 41st Ed).

  Gate 3 will catch this. The Critic will flag it. The Builder will correct
  it by reading frozen/anatomy_spec.md line by line.

  Secondary expected errors (may fire on any turn):
    - Liver placed left of midline (confusion with stomach)
    - Equal-sized lungs (missing cardiac notch asymmetry)
    - Aortic bifurcation at L3 instead of L4
    - Symmetric diaphragm (missing right-higher anatomy)

================================================================================
MILESTONES
================================================================================

Milestone 1 — Core viewer skeleton
  Build anatomy_viewer.html with:
  - HTML5 Canvas, 340x500px
  - Background #F0F4F8 with subtle grid
  - Body silhouette (proportions from SEGMENT_RATIOS in frozen spec)
  - Front/Back/Side view switcher (3 buttons)
  - 7 system toggle buttons with frozen colors
  - Info panel showing system description
  Sigma gates: canvas renders, 3 views present, 7 buttons present

Milestone 2 — Skeletal system
  Draw all skeletal structures for anterior view:
  - Skull, mandible at frozen HEAD_HEIGHT_RATIO
  - Vertebral column with correct curvatures (cervical lordosis, thoracic
    kyphosis, lumbar lordosis) — NOT a straight line
  - Rib cage: 12 pairs, 7 true / 3 false / 2 floating
  - Sternum at frozen STERNUM_TOP_Y to STERNUM_BOTTOM_Y
  - Clavicles, scapulae, pelvis, long bones of limbs
  Sigma gates: sternum within 2% of frozen Y positions, vertebral curvature present

Milestone 3 — Organ systems (all 6 soft-tissue systems)
  Draw circulatory, respiratory, digestive, nervous, muscular, lymphatic.
  ALL organ positions must use frozen constants from anatomy_constants.py.
  The false positive WILL fire on this milestone — document it.
  Sigma gates:
    - heart_center_y >= 0.330 (catches T3/T4 prior)
    - liver_center_x > 0 (catches left-side prior)
    - right_lung_height > left_lung_height (catches equal-size prior)
    - aorta_bifurcation_y >= 0.520 (catches L3 prior)

Milestone 4 — Posterior + lateral views
  Extend all 7 systems to posterior and lateral views.
  Posterior: trapezius, latissimus, erector spinae, posterior skull
  Lateral: spinal curvatures visible, organ depth relationships
  Sigma gates: all 3 views render, labels present in each view

================================================================================
SIGMA GATES (config.yaml equivalent)
================================================================================

anomaly_checks:
  - metric: heart_center_y_valid
    operator: "=="
    threshold: 1      # 1 = passes check, 0 = fails
    description: "heart_center_y >= 0.330 (not the T3 prior)"

  - metric: liver_on_right
    operator: "=="
    threshold: 1
    description: "liver center_x_offset > 0"

  - metric: right_lung_larger
    operator: "=="
    threshold: 1
    description: "right_lung_height > left_lung_height"

  - metric: aorta_bifurcation_l4
    operator: "=="
    threshold: 1
    description: "aorta_bifurcation_y >= 0.520"

  - metric: all_tests_passing
    operator: "=="
    threshold: 1
    description: "python -m pytest tests/ passes 0 failures"

================================================================================
FROZEN FILES
================================================================================

DO NOT MODIFY:
  frozen/anatomy_spec.md         — all proportions and organ positions
  frozen/anatomy_constants.py    — Python constants, same values as spec

All JavaScript code must use the exact numeric values from anatomy_constants.py.
The Builder must read the frozen spec before writing any coordinate.

================================================================================
CRITIC INSTRUCTIONS
================================================================================

Your specific mission for this experiment:

  1. After every build, open frozen/anatomy_spec.md
  2. For each organ, check: does the rendered position match the frozen Y?
     Tolerance: +/- 0.010 of frozen ratio value
  3. Specifically check the PRIOR_ERRORS section — these are your primary targets
  4. Heart at y < 0.330: BLOCKING issue, cite Gray's Anatomy T5 level
  5. Liver on left: BLOCKING issue
  6. Equal lung sizes: BLOCKING issue
  7. The frozen spec is the ground truth. Not what "looks right."

Gate 3 scoring rubric:
  1.00 = all organ positions within tolerance, all prior errors absent
  0.85 = minor position drift on secondary structures only
  0.70 = one primary organ misplaced (heart, liver, or lung)
  0.50 = multiple primary organs misplaced
  0.00 = figure does not render or missing major systems

================================================================================
EXIT CONDITIONS
================================================================================

EXIT when:
  - All 4 milestones complete
  - python -m pytest tests/test_anatomy.py passes all tests
  - anatomy_viewer.html renders all 7 systems in 3 views
  - No prior errors remain (all 5 PRIOR_ERROR checks pass)
  - REPORT.md written with false positive story

The false positive story is the most important output of this experiment.
Document exactly which prior fired, on which turn, and what the correction was.
