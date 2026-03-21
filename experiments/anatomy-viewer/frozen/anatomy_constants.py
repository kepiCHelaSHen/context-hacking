"""
Anatomy Viewer — Frozen Proportion Constants
Source: frozen/anatomy_spec.md

DO NOT MODIFY THIS FILE.
All values trace to Gray's Anatomy 41st Edition or WHO anthropometric data.
Import these constants. Do not redefine them.
"""

# ── Segment ratios (fraction of total figure height H) ───────────────────────

HEAD_HEIGHT_RATIO    = 0.145
NECK_HEIGHT_RATIO    = 0.040
TORSO_HEIGHT_RATIO   = 0.305
UPPER_ARM_RATIO      = 0.145
FOREARM_RATIO        = 0.120
HAND_RATIO           = 0.075
PELVIS_HEIGHT_RATIO  = 0.095
THIGH_RATIO          = 0.245
LOWER_LEG_RATIO      = 0.235
FOOT_HEIGHT_RATIO    = 0.040

SHOULDER_WIDTH_RATIO = 0.259
HIP_WIDTH_RATIO      = 0.191
HEAD_WIDTH_RATIO     = 0.130
WAIST_WIDTH_RATIO    = 0.155

BILATERAL_SYMMETRY_TOL = 0.005

# ── Organ positions (fraction of total height from top) ──────────────────────

HEART_CENTER_Y       = 0.355   # T5 — NOT 0.310 (LLM prior)
HEART_CENTER_X_OFF   = -0.015  # 1.5% left of midline
HEART_HEIGHT         = 0.080
HEART_WIDTH          = 0.060

LEFT_LUNG_CENTER_Y   = 0.340
LEFT_LUNG_CENTER_X   = -0.090
LEFT_LUNG_HEIGHT     = 0.175
LEFT_LUNG_WIDTH      = 0.065

RIGHT_LUNG_CENTER_Y  = 0.330
RIGHT_LUNG_CENTER_X  = 0.080
RIGHT_LUNG_HEIGHT    = 0.185  # MUST be > LEFT_LUNG_HEIGHT
RIGHT_LUNG_WIDTH     = 0.068

LIVER_CENTER_Y       = 0.405
LIVER_CENTER_X       = 0.060   # positive = right side — NOT negative (LLM prior)
LIVER_HEIGHT         = 0.090
LIVER_WIDTH          = 0.110

STOMACH_CENTER_Y     = 0.415
STOMACH_CENTER_X     = -0.055  # left side
STOMACH_HEIGHT       = 0.070
STOMACH_WIDTH        = 0.065

SPLEEN_CENTER_Y      = 0.400
SPLEEN_CENTER_X      = -0.110  # left side
SPLEEN_HEIGHT        = 0.050
SPLEEN_WIDTH         = 0.035

BRAIN_CENTER_Y       = 0.095
BRAIN_HEIGHT         = 0.110
BRAIN_WIDTH          = 0.095

DIAPHRAGM_Y          = 0.450
DIAPHRAGM_RIGHT_HIGHER = True  # NOT symmetric (LLM prior is symmetric)

# ── Aorta ─────────────────────────────────────────────────────────────────────

AORTA_ARCH_Y         = 0.255
AORTA_DESCENDING_Y   = 0.280
AORTA_BIFURCATION_Y  = 0.535  # L4 — NOT 0.510/L3 (LLM prior)

# ── Vertebral column Y positions ─────────────────────────────────────────────

C1_Y   = 0.185
T1_Y   = 0.225
T12_Y  = 0.445
L5_Y   = 0.530
S1_Y   = 0.545

STERNUM_TOP_Y    = 0.235
STERNUM_BOTTOM_Y = 0.410
STERNUM_WIDTH    = 0.020

# ── System colors (frozen — do not change) ───────────────────────────────────

COLORS = {
    "skeletal":    "#B45309",
    "muscular":    "#991B1B",
    "nervous":     "#1D4ED8",
    "circulatory": "#DC2626",
    "respiratory": "#0369A1",
    "digestive":   "#065F46",
    "lymphatic":   "#6D28D9",
}

BACKGROUND  = "#F0F4F8"
GRID_COLOR  = "rgba(0,0,0,0.04)"

# ── Canvas ────────────────────────────────────────────────────────────────────

CANVAS_WIDTH   = 340
CANVAS_HEIGHT  = 500
FIGURE_HEIGHT  = 490
FIGURE_TOP     = 10
