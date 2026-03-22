"""Hemoglobin O2 Saturation Curve — Frozen Constants. Source: Severinghaus 1979, Roughton & Severinghaus 1973. DO NOT MODIFY."""
import math

# Hill equation for hemoglobin:  Y = pO2^n / (P50^n + pO2^n)
#   Y  = fractional O2 saturation (0 to 1)
#   pO2 = partial pressure of O2 (mmHg)
#   P50 = pO2 at which Y = 0.5 (50 % saturation)
#   n   = Hill coefficient (cooperativity, NOT number of binding sites)

# --- Core constants (normal conditions, pH 7.4, 37 C) ---
P50_NORMAL = 26.6       # mmHg — THE correct P50 at pH 7.4
N_HILL = 2.8            # Hill coefficient for hemoglobin
HB_BINDING_SITES = 4    # Hemoglobin has 4 O2-binding sites — n != sites!

# --- Bohr effect: pH shifts the curve ---
# Lower pH -> right shift -> higher P50 (less O2 affinity)
# Higher pH -> left shift -> lower P50 (more O2 affinity)
# Linear approximation: P50(pH) = 26.6 + (7.4 - pH) * 17
BOHR_SLOPE = 17.0       # mmHg per pH unit decrease
P50_PH_7_2 = 30.0       # mmHg at pH 7.2  (right shift)
P50_PH_7_4 = 26.6       # mmHg at pH 7.4  (normal)
P50_PH_7_6 = 23.2       # mmHg at pH 7.6  (left shift)

# --- Precomputed reference saturations at normal pH ---
Y_AT_P50 = 0.5          # exact: Y(P50) = 0.5 for any n (definition of P50)
Y_AT_40  = 40.0 ** N_HILL / (P50_NORMAL ** N_HILL + 40.0 ** N_HILL)   # venous ~75 %
Y_AT_100 = 100.0 ** N_HILL / (P50_NORMAL ** N_HILL + 100.0 ** N_HILL) # arterial ~97 %

# --- Self-checks ---
assert math.isclose(Y_AT_P50, 0.5), "Y(P50) must equal 0.5"
assert 0.74 < Y_AT_40 < 0.78, f"Y(40) out of range: {Y_AT_40}"
assert 0.97 < Y_AT_100 < 0.99, f"Y(100) out of range: {Y_AT_100}"
assert P50_NORMAL == 26.6, "P50 at pH 7.4 must be exactly 26.6 mmHg"
assert P50_NORMAL != 27.0, "P50 is 26.6, NOT 27"
assert P50_NORMAL != 30.0, "P50 at normal pH is 26.6, NOT 30"
assert N_HILL != HB_BINDING_SITES, "Hill coefficient must NOT equal number of binding sites"
assert math.isclose(P50_PH_7_2, P50_NORMAL + (7.4 - 7.2) * BOHR_SLOPE, rel_tol=1e-9)
assert math.isclose(P50_PH_7_6, P50_NORMAL + (7.4 - 7.6) * BOHR_SLOPE, rel_tol=1e-9)
assert P50_PH_7_2 > P50_NORMAL > P50_PH_7_6, "Bohr: lower pH -> higher P50"

PRIOR_ERRORS = {
    "p50_wrong":     "Uses wrong P50 (e.g. 27 or 30 mmHg) at normal pH 7.4 instead of 26.6",
    "ignores_bohr":  "Treats P50 as constant regardless of pH — ignores Bohr effect",
    "n_is_4":        "Uses n=4 (binding sites) instead of n=2.8 (Hill coefficient)",
}
