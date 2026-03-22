"""Michaelis-Menten Enzyme Kinetics — Frozen Constants. Source: Michaelis & Menten 1913. DO NOT MODIFY."""
import math

# v = Vmax * [S] / (Km + [S])
# Km = substrate concentration at which v = Vmax / 2  (NOT Vmax!)
# At [S] = Km:     v = Vmax * Km / (Km + Km) = Vmax / 2   (50% of max velocity)
# At [S] = 10*Km:  v = Vmax * 10Km / (Km + 10Km) = 10/11 * Vmax ≈ 0.909 * Vmax (NOT Vmax)
# v approaches Vmax asymptotically — never actually reaches it at finite [S]

# Lineweaver-Burk (double-reciprocal): 1/v = (Km/Vmax)(1/[S]) + 1/Vmax
#   slope     = Km / Vmax
#   y-intercept = 1 / Vmax
#   x-intercept = -1 / Km   (NEGATIVE, not positive)
# Back-calculate: Km = slope / y_intercept  (since slope = Km/Vmax and y_int = 1/Vmax)

# Test parameters
VMAX = 100.0   # μmol/min
KM   = 5.0     # mM

# Pre-computed correct values at key substrate concentrations
V_AT_KM   = VMAX * KM / (KM + KM)          # 50.0 (= Vmax/2 when [S]=Km ✓)
V_AT_10   = VMAX * 10 / (KM + 10)          # 66.667
V_AT_50   = VMAX * 50 / (KM + 50)          # 90.909
V_AT_100  = VMAX * 100 / (KM + 100)        # 95.238

assert math.isclose(V_AT_KM, VMAX / 2, rel_tol=1e-9), "v at [S]=Km must equal Vmax/2"
assert math.isclose(V_AT_KM, 50.0, rel_tol=1e-9)
assert math.isclose(V_AT_10, 100 * 10 / 15, rel_tol=1e-9)
assert math.isclose(V_AT_50, 100 * 50 / 55, rel_tol=1e-9)
assert math.isclose(V_AT_100, 100 * 100 / 105, rel_tol=1e-9)

# v at [S]=Km is Vmax/2, NOT Vmax — this is the most common LLM error
WRONG_V_AT_KM = VMAX  # The wrong answer LLMs give (thinks Km means v=Vmax)
assert not math.isclose(V_AT_KM, WRONG_V_AT_KM), "v at Km must NOT equal Vmax"

# Lineweaver-Burk derived values
LB_SLOPE       = KM / VMAX                 # 0.05
LB_Y_INTERCEPT = 1.0 / VMAX                # 0.01
LB_X_INTERCEPT = -1.0 / KM                 # -0.2 (negative!)

assert math.isclose(LB_SLOPE, 0.05, rel_tol=1e-9)
assert math.isclose(LB_Y_INTERCEPT, 0.01, rel_tol=1e-9)
assert math.isclose(LB_X_INTERCEPT, -0.2, rel_tol=1e-9)
assert LB_X_INTERCEPT < 0, "Lineweaver-Burk x-intercept must be negative"

PRIOR_ERRORS = {
    "km_is_max":              "Thinks [S]=Km gives v=Vmax (should be Vmax/2)",
    "lineweaver_x_intercept": "Wrong sign on Lineweaver-Burk x-intercept (should be -1/Km)",
    "v_at_high_S":            "Claims v=Vmax at some finite [S] (v only approaches Vmax asymptotically)",
}
