"""CO2 Radiative Forcing — Frozen Constants. Source: Myhre et al. 1998 (GRL), IPCC AR5 Ch8. DO NOT MODIFY."""
import math

# Radiative forcing formula: dF = alpha * ln(C / C0)  W/m^2
# alpha = 5.35 W/m^2 (Myhre et al. 1998, widely adopted by IPCC)
ALPHA = 5.35          # W/m^2 — radiative forcing coefficient

# Reference (preindustrial) CO2 concentration
C0 = 280.0            # ppm — preindustrial baseline

# Current CO2 concentration (approximate 2024 value)
C_CURRENT = 420.0     # ppm

# KEY: The relationship is LOGARITHMIC, not linear.
# Doubling CO2 gives the same dF regardless of starting level.
# dF_2x = alpha * ln(2) = 5.35 * 0.6931 = 3.708 W/m^2

LN2 = math.log(2)                         # 0.6931471805599453
DF_DOUBLING = ALPHA * LN2                  # 3.7083 W/m^2 (approx 3.7)

# Test case: C=420, C0=280
RATIO_TEST = C_CURRENT / C0               # 1.5
LN_RATIO_TEST = math.log(RATIO_TEST)      # 0.4054651081...
DF_TEST = ALPHA * LN_RATIO_TEST           # 2.1692 W/m^2

# Wrong linear calculation (common LLM error):
# dF_wrong = alpha * (C - C0) / C0 = 5.35 * (420-280)/280 = 5.35 * 0.5 = 2.675
DF_LINEAR_WRONG = ALPHA * (C_CURRENT - C0) / C0   # 2.675 — 23% too high!

# Inverse: given a forcing, what CO2 concentration?
# C = C0 * exp(dF / alpha)
C_INVERSE_TEST = C0 * math.exp(DF_TEST / ALPHA)   # should recover 420 ppm

# Climate sensitivity context:
# Equilibrium Climate Sensitivity (ECS) ~ 3 deg C per doubling (with feedbacks)
# dF_2x ~ 3.7 W/m^2 -> ~3 deg C warming (Charney sensitivity)
ECS_APPROX = 3.0      # deg C per CO2 doubling (central estimate)

PRIOR_ERRORS = {
    "linear_not_log":    "Uses linear formula dF=alpha*(C-C0)/C0 instead of logarithmic dF=alpha*ln(C/C0)",
    "wrong_coefficient": "Uses 3.7 as the coefficient instead of 5.35 (3.7 is the RESULT for doubling, not the coefficient)",
    "base10_not_natural": "Uses log10 instead of natural log (ln) — off by factor of ln(10)=2.303",
}
