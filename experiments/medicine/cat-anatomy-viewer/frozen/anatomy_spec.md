# Anatomy Viewer — Frozen Specification
# Source: Gray's Anatomy 41st Edition + WHO Anthropometric Reference Data
# DO NOT MODIFY. All coordinates and ratios are authoritative.
# New code must compose WITH this spec, not redefine it.

================================================================================
CANONICAL BODY PROPORTIONS
Source: Anthropometric reference data (WHO 2012, Table B.2)
Reference height: H = total figure height in pixels
================================================================================

SEGMENT_RATIOS:
  head_height:          0.145   # skull = 14.5% of total height
  neck_height:          0.040
  torso_height:         0.305   # sternum top to iliac crest
  upper_arm_length:     0.145
  forearm_length:       0.120
  hand_length:          0.075
  pelvis_height:        0.095
  thigh_length:         0.245
  lower_leg_length:     0.235
  foot_height:          0.040

TRANSVERSE_RATIOS:
  # Expressed as fraction of total height
  shoulder_width:       0.259   # acromion to acromion
  hip_width:            0.191   # greater trochanter to trochanter
  head_width:           0.130
  waist_width:          0.155

BILATERAL_SYMMETRY_TOLERANCE: 0.005  # max ratio difference left vs right

================================================================================
ORGAN POSITIONS
Source: Gray's Anatomy 41st Ed, Chapter 4 (Thorax) and Chapter 5 (Abdomen)
All positions expressed as fraction of total figure height from top
================================================================================

ORGANS:
  heart:
    center_y:           0.355   # T5 vertebral level
    center_x_offset:   -0.015   # 1.5% left of midline
    height:             0.080
    width:              0.060
    note: "Apex points inferolaterally to left, T5 level"

  left_lung:
    center_y:           0.340
    center_x_offset:   -0.090
    height:             0.175
    width:              0.065
    note: "T2 to T10, cardiac notch on medial surface"

  right_lung:
    center_y:           0.330
    center_x_offset:    0.080
    height:             0.185
    width:              0.068
    note: "T2 to T9, slightly larger than left"

  liver:
    center_y:           0.405
    center_x_offset:    0.060
    height:             0.090
    width:              0.110
    note: "Right hypochondriac, T7-T11 vertebral levels"

  stomach:
    center_y:           0.415
    center_x_offset:   -0.055
    height:             0.070
    width:              0.065
    note: "Left hypochondriac, T10-L1 levels"

  spleen:
    center_y:           0.400
    center_x_offset:   -0.110
    height:             0.050
    width:              0.035
    note: "Left hypochondriac, 9th-11th rib level"

  kidneys:
    left_center_y:      0.440
    right_center_y:     0.430   # right kidney slightly lower (liver displacement)
    center_x_offset:    0.060   # distance from midline
    height:             0.055
    width:              0.030
    note: "Retroperitoneal, T12-L3"

  brain:
    center_y:           0.095
    height:             0.110
    width:              0.095

  diaphragm:
    center_y:           0.450   # T8 on right, T9 on left
    note: "Dome shape, right higher than left by one rib"

================================================================================
SKELETAL LANDMARKS
Source: Gray's Anatomy 41st Ed, Chapter 2
================================================================================

VERTEBRAL_COLUMN:
  cervical_vertebrae:   7       # C1-C7
  thoracic_vertebrae:   12      # T1-T12
  lumbar_vertebrae:     5       # L1-L5
  sacral_fused:         5
  coccygeal_fused:      4

  cervical_curvature:   lordosis    # concave posterior
  thoracic_curvature:   kyphosis    # concave anterior
  lumbar_curvature:     lordosis    # concave posterior

  # Y positions as fraction of total height
  C1_y:    0.185
  T1_y:    0.225
  T12_y:   0.445
  L5_y:    0.530
  S1_y:    0.545

STERNUM:
  top_y:      0.235   # manubrium top = T2/T3 level
  bottom_y:   0.410   # xiphoid = T10 level
  width:      0.020

RIBS:
  count: 12 pairs
  true_ribs: 7       # attach directly to sternum
  false_ribs: 3      # attach via costal cartilage
  floating: 2        # no anterior attachment
  angle: 15_degrees  # rib angle below horizontal (lateral view)

CLAVICLE:
  medial_y:   0.232  # sternal end, T2 level
  lateral_y:  0.238  # acromial end, slightly lower
  note: "S-shaped, medial 2/3 convex anteriorly"

SCAPULA:
  superior_y:  0.235
  inferior_y:  0.360
  note: "T2 to T7 posterior, overlaps ribs 2-7"

================================================================================
VASCULAR SYSTEM
Source: Gray's Anatomy 41st Ed, Chapter 6
================================================================================

AORTA:
  arch_apex_y:    0.255   # superior to aortic valve
  descending_y:   0.280
  bifurcation_y:  0.535   # L4 vertebral level — NOT L3, NOT L5
  note: "Bifurcation at L4 is the frozen value. LLM prior often says L3."

HEART_VALVES:
  aortic_y:       0.355
  pulmonary_y:    0.345
  mitral_y:       0.365
  tricuspid_y:    0.370

================================================================================
KNOWN LLM PRIOR ERRORS (Prior-as-Detector targets)
These are the values LLMs generate from training priors.
The Critic MUST check for these specific drifts.
================================================================================

PRIOR_ERRORS:
  - field: heart_center_y
    prior_value: 0.310   # LLM places heart too high ("upper chest")
    correct_value: 0.355  # T5 level per Gray's
    detection: "heart center_y < 0.330 triggers Gate 3 FAIL"

  - field: aorta_bifurcation_y
    prior_value: 0.510   # LLM says L3
    correct_value: 0.535  # L4 per Gray's
    detection: "bifurcation_y < 0.520 triggers Gate 3 FAIL"

  - field: liver_side
    prior_value: "left"  # LLM occasionally places liver on left
    correct_value: "right"
    detection: "liver center_x_offset < 0 triggers Gate 3 FAIL"

  - field: right_lung_size
    prior_value: "equal_to_left"
    correct_value: "larger_than_left"  # right_lung height > left_lung height
    detection: "right_lung.height <= left_lung.height triggers Gate 3 FAIL"

  - field: diaphragm_laterality
    prior_value: "symmetric"
    correct_value: "right_higher"
    detection: "symmetric diaphragm triggers Gate 3 FAIL"

================================================================================
COLOR PALETTE (frozen — do not change)
================================================================================

SYSTEM_COLORS:
  skeletal:     "#B45309"   # amber-700
  muscular:     "#991B1B"   # red-800
  nervous:      "#1D4ED8"   # blue-700
  circulatory:  "#DC2626"   # red-600
  respiratory:  "#0369A1"   # sky-700
  digestive:    "#065F46"   # emerald-900
  lymphatic:    "#6D28D9"   # violet-700

BACKGROUND:   "#F0F4F8"
GRID_COLOR:   "rgba(0,0,0,0.04)"
SILHOUETTE:   "rgba(55,65,81,0.07)"

================================================================================
RENDERING CONSTRAINTS
================================================================================

CANVAS:
  width:  340
  height: 500
  figure_height: 490   # total figure occupies 490px of canvas
  figure_top:    10    # figure starts at y=10

VIEWS: [anterior, posterior, lateral]

LABEL_FONT:    "9px monospace"
LABEL_COLOR:   system_color  # label uses same color as system

BILATERAL_RENDERING:
  anterior: both sides drawn, left = anatomical left = viewer's right
  posterior: flipped, traps and posterior muscles shown
  lateral: right lateral view, figure faces right
