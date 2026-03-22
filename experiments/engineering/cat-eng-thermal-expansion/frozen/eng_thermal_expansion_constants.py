"""Thermal Expansion — Frozen Constants. Source: Cengel, Thermodynamics 9th Ed. DO NOT MODIFY."""
import math

# Linear:      dL = alpha * L0 * dT
# Area:        dA = 2*alpha * A0 * dT   (gamma = 2*alpha for isotropic)
# Volumetric:  dV = beta * V0 * dT      (beta  = 3*alpha for isotropic)
# KEY: beta = 3*alpha, NOT alpha!  Using alpha for volume gives 1/3 correct answer.

# Material coefficients of linear thermal expansion (per degree C)
ALPHA_STEEL    = 12e-6   # /degC
ALPHA_ALUMINUM = 23e-6   # /degC
ALPHA_COPPER   = 17e-6   # /degC

# Test case: steel rod/cube, L0=1m, V0=1m^3, dT=100 degC
L0_STEEL = 1.0           # m
V0_STEEL = 1.0           # m^3
A0_STEEL = 1.0           # m^2
DT_TEST  = 100.0         # degC

# Expected results — linear
DL_STEEL = ALPHA_STEEL * L0_STEEL * DT_TEST          # 0.0012 m = 1.2 mm

# Expected results — volumetric (correct: uses 3*alpha)
BETA_STEEL = 3 * ALPHA_STEEL                          # 36e-6 /degC
DV_STEEL_CORRECT = BETA_STEEL * V0_STEEL * DT_TEST    # 0.0036 m^3

# Expected results — volumetric WRONG (common LLM error: uses alpha instead of 3*alpha)
DV_STEEL_WRONG = ALPHA_STEEL * V0_STEEL * DT_TEST     # 0.0012 m^3  (3x too small!)

# Expected results — area (correct: uses 2*alpha)
GAMMA_STEEL = 2 * ALPHA_STEEL                          # 24e-6 /degC
DA_STEEL_CORRECT = GAMMA_STEEL * A0_STEEL * DT_TEST    # 0.0024 m^2

# Expected results — area WRONG (common LLM error: uses alpha instead of 2*alpha)
DA_STEEL_WRONG = ALPHA_STEEL * A0_STEEL * DT_TEST      # 0.0012 m^2  (2x too small!)

PRIOR_ERRORS = {
    "volume_uses_alpha": "Uses alpha instead of 3*alpha (beta) for volumetric expansion",
    "area_uses_alpha":   "Uses alpha instead of 2*alpha (gamma) for area expansion",
    "delta_t_sign":      "Wrong sign on delta-T for cooling (should be negative dT)",
}
