"""Euler-Bernoulli Beam Bending — Frozen Constants. Source: Timoshenko & Gere, Mechanics of Materials. DO NOT MODIFY."""
import math

# Bending stress: sigma = M * y / I
# M = bending moment, y = distance from neutral axis, I = second moment of area
#
# Rectangular cross-section: I = b*h^3 / 12  (NOT b*h^2/12!)
# Circular cross-section:    I = pi*d^4 / 64  (NOT pi*d^4/32 — that's the POLAR moment J)
#
# Max deflection, simply-supported beam, center point load:
#   delta = P*L^3 / (48*E*I)
#
# LLM priors:
#   1. Uses b*h^2/12 for rectangular I (drops one power of h)
#   2. Confuses area moment I with polar moment J (pi*d^4/32 vs /64)
#   3. Wrong coefficient in deflection formula (e.g. 1/384 or 1/24 instead of 1/48)

# Reference rectangular beam
B_REF = 0.05    # width 50 mm = 0.05 m
H_REF = 0.1     # height 100 mm = 0.1 m

# Correct I for rectangular: b*h^3/12
I_RECT_REF = B_REF * H_REF**3 / 12.0               # 4.16666...e-6 m^4

# WRONG I — common LLM error: b*h^2/12 (missing one power of h)
I_RECT_WRONG_BH2 = B_REF * H_REF**2 / 12.0         # 4.16666...e-5 m^4 (10x too large!)

# Reference circular cross-section
D_REF = 0.1     # diameter 100 mm = 0.1 m

# Correct area moment of inertia for circle: pi*d^4/64
I_CIRC_REF = math.pi * D_REF**4 / 64.0              # 4.90874...e-6 m^4

# WRONG — polar moment J = pi*d^4/32 (2x area moment)
J_POLAR_WRONG = math.pi * D_REF**4 / 32.0           # 9.81748...e-6 m^4 (2x too large!)

# Reference beam loading
P_REF = 1000.0      # 1 kN center point load
L_REF = 2.0         # 2 m span
E_REF = 200e9       # 200 GPa (steel)

# Bending stress test: M_max = P*L/4 for center-loaded simply-supported beam
M_MAX_REF = P_REF * L_REF / 4.0                     # 500 N*m
Y_MAX_REF = H_REF / 2.0                             # 0.05 m (outermost fiber)
SIGMA_MAX_REF = M_MAX_REF * Y_MAX_REF / I_RECT_REF  # 6.0e6 Pa = 6 MPa

# Max deflection at midspan: delta = P*L^3 / (48*E*I)
DELTA_REF = P_REF * L_REF**3 / (48.0 * E_REF * I_RECT_REF)  # 0.0002 m = 0.2 mm

# Wrong deflection using wrong I (bh^2/12): 10x smaller deflection (wrong!)
DELTA_WRONG_I = P_REF * L_REF**3 / (48.0 * E_REF * I_RECT_WRONG_BH2)  # 0.00002 m

PRIOR_ERRORS = {
    "i_bh_squared":           "Uses b*h^2/12 instead of b*h^3/12 for rectangular I — off by factor h",
    "polar_vs_area":          "Uses polar moment J = pi*d^4/32 instead of area moment I = pi*d^4/64 — 2x too large",
    "deflection_formula_wrong": "Wrong coefficient in simply-supported deflection (e.g. 1/384 or 1/24 instead of 1/48)",
}
