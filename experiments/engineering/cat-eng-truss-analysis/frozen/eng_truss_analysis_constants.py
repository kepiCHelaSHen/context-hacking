"""Truss Analysis (Method of Joints) — Frozen Constants. Source: Hibbeler, Structural Analysis. DO NOT MODIFY."""
import math

# Method of joints: at each joint, ΣFx = 0 and ΣFy = 0
# Sign convention: POSITIVE = TENSION (pulling away from joint)
#                  NEGATIVE = COMPRESSION (pushing into joint)
#
# Simple truss: equilateral triangle, 3 members (2 diagonal, 1 horizontal)
# Load P applied downward at apex, pinned supports at both base joints.
#
# By symmetry: R_left = R_right = P/2
#
# At left support joint (joint equilibrium):
#   ΣFy = 0: R_left + F_diag * sin(60°) = 0
#            F_diag = -R_left / sin(60°) = -P / (2 sin 60°) = -P/√3
#   ΣFx = 0: F_horiz + F_diag * cos(60°) = 0
#            F_horiz = -F_diag * cos(60°) = P cos(60°) / (2 sin(60°)) = P/(2 tan 60°) = P/(2√3)
#
# LLM priors (common errors):
#   1. tension_compression_swap — applies wrong sign convention (positive=compression)
#   2. force_direction_wrong — applies forces in wrong direction at joint
#   3. reaction_wrong — computes wrong support reactions

# Reference geometry
ANGLE_DEG = 60.0                                # equilateral triangle angle
ANGLE_RAD = math.radians(ANGLE_DEG)             # pi/3
L_REF = 2.0                                     # member length in metres

# Reference load
P_REF = 10.0                                    # 10 kN applied at apex (downward)

# Support reactions (by symmetry)
R_LEFT_REF = P_REF / 2.0                        # 5.0 kN  (upward)
R_RIGHT_REF = P_REF / 2.0                       # 5.0 kN  (upward)

# Trig values at 60°
SIN60 = math.sin(ANGLE_RAD)                     # √3/2 ≈ 0.8660254038
COS60 = math.cos(ANGLE_RAD)                     # 1/2 = 0.5
TAN60 = math.tan(ANGLE_RAD)                     # √3 ≈ 1.7320508076

# Correct member forces
# Diagonal members: F_diag = -P / (2 sin 60°) = -P/√3  (COMPRESSION — negative!)
F_DIAG_REF = -P_REF / (2.0 * SIN60)            # -5.7735026919 kN

# Horizontal member: F_horiz = P / (2 tan 60°) = P/(2√3)  (TENSION — positive!)
F_HORIZ_REF = P_REF / (2.0 * TAN60)            # +2.8867513459 kN

# WRONG values — common LLM errors
# Error 1: swapped signs (tension ↔ compression)
F_DIAG_WRONG_SIGN = -F_DIAG_REF                 # +5.7735 (wrong: positive = tension)
F_HORIZ_WRONG_SIGN = -F_HORIZ_REF               # -2.8868 (wrong: negative = compression)

# Error 2: wrong reaction (e.g. R = P instead of P/2)
R_WRONG_FULL_LOAD = P_REF                       # 10.0 kN (wrong: forgot to split)
F_DIAG_WRONG_REACTION = -R_WRONG_FULL_LOAD / SIN60   # -11.5470 kN (wrong)

# Error 3: using degrees instead of radians in sin/cos (nonsensical result)
F_DIAG_WRONG_DEG = -P_REF / (2.0 * math.sin(ANGLE_DEG))  # using sin(60) not sin(pi/3)

PRIOR_ERRORS = {
    "tension_compression_swap":  "Swaps sign convention — reports diagonal as tension (+) and horizontal as compression (-)",
    "force_direction_wrong":     "Applies forces in wrong direction at joint, producing incorrect equilibrium equations",
    "reaction_wrong":            "Computes support reactions as P instead of P/2 (forgets symmetric split)",
}
