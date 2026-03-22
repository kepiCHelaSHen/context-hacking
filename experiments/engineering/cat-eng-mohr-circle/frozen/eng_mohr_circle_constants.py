"""Mohr's Circle — Frozen Constants. Source: Timoshenko & Gere, Mechanics of Materials. DO NOT MODIFY."""
import math

# Mohr's Circle for 2-D stress state (σ_x, σ_y, τ_xy)
# Center:           C     = (σ_x + σ_y) / 2
# Radius:           R     = √( ((σ_x - σ_y)/2)² + τ_xy² )
# Principal stress:  σ₁    = C + R  (max),  σ₂ = C - R  (min)
# Max shear stress: τ_max = R
# Principal angle:  θ_p   = (1/2) * arctan(2*τ_xy / (σ_x - σ_y))
#
# LLM priors:
#   - Uses (σ_x - σ_y)/2 for center instead of (σ_x + σ_y)/2
#   - Forgets τ_xy² in radius (uses only ((σ_x - σ_y)/2)²)
#   - Forgets 1/2 factor in principal angle formula

# Reference stress state (MPa)
SX_REF  = 80.0   # σ_x
SY_REF  = 40.0   # σ_y
TXY_REF = 30.0   # τ_xy

# Derived constants (frozen from reference values)
CENTER_REF = (SX_REF + SY_REF) / 2.0                                          # 60.0 MPa
RADIUS_REF = math.sqrt(((SX_REF - SY_REF) / 2.0) ** 2 + TXY_REF ** 2)       # √1300 = 36.05551... MPa
SIGMA1_REF = CENTER_REF + RADIUS_REF                                           # 96.05551... MPa
SIGMA2_REF = CENTER_REF - RADIUS_REF                                           # 23.94448... MPa
TAU_MAX_REF = RADIUS_REF                                                       # 36.05551... MPa
THETA_P_RAD_REF = 0.5 * math.atan2(2.0 * TXY_REF, SX_REF - SY_REF)          # 0.49145... rad
THETA_P_DEG_REF = math.degrees(THETA_P_RAD_REF)                               # 28.1553... deg

# Known-wrong values for trap detection
CENTER_WRONG  = (SX_REF - SY_REF) / 2.0                                       # 20.0 MPa — WRONG (difference instead of sum)
RADIUS_NO_SHEAR = abs(SX_REF - SY_REF) / 2.0                                  # 20.0 MPa — WRONG (missing τ_xy)
THETA_P_NO_HALF = math.degrees(math.atan2(2.0 * TXY_REF, SX_REF - SY_REF))   # 56.3099... deg — WRONG (missing 1/2)

PRIOR_ERRORS = {
    "center_difference":  "Uses (σ_x - σ_y)/2 for center instead of (σ_x + σ_y)/2",
    "radius_no_shear":    "Forgets τ_xy² in radius — uses only ((σ_x - σ_y)/2)²",
    "angle_no_half":      "Forgets 1/2 factor in principal angle — returns full arctan instead of half",
}
