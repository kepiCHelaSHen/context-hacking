"""Hill Equation — Frozen Constants. Source: Hill 1910, Weiss 1997. DO NOT MODIFY."""
import math
# θ = [L]^n / (K_d^n + [L]^n)  where n = Hill coefficient
# n=1: no cooperativity (reduces to Michaelis-Menten / hyperbolic)
# n>1: positive cooperativity (sigmoidal curve)
# n<1: negative cooperativity
# KEY: n is NOT the number of binding sites.
#   Hemoglobin has 4 O₂-binding sites but n≈2.8
# At [L]=K_d: θ=0.5 regardless of n (always true)
# Test: K_d=10.0, n=2.8 (hemoglobin-like)
#   θ(5)  = 5^2.8  / (10^2.8 + 5^2.8)  = 90.5975 / 721.5548 ≈ 0.12556
#   θ(10) = 10^2.8 / (10^2.8 + 10^2.8) = 0.5 (exact, always)
#   θ(20) = 20^2.8 / (10^2.8 + 20^2.8) ≈ 0.87444
KD = 10.0
N_HILL = 2.8        # Hill coefficient (hemoglobin-like)
HEMO_SITES = 4      # Hemoglobin has 4 binding sites — n ≠ sites!

# Precomputed reference values
THETA_AT_5  = 5.0  ** N_HILL / (KD ** N_HILL + 5.0  ** N_HILL)
THETA_AT_10 = 0.5  # exact: θ(Kd) = 0.5 for any n
THETA_AT_20 = 20.0 ** N_HILL / (KD ** N_HILL + 20.0 ** N_HILL)

assert math.isclose(THETA_AT_10, 0.5), "θ(Kd) must equal 0.5"
assert THETA_AT_5 < 0.5, "θ(L<Kd) must be < 0.5"
assert THETA_AT_20 > 0.5, "θ(L>Kd) must be > 0.5"
assert math.isclose(THETA_AT_5 + THETA_AT_20, 1.0, rel_tol=1e-9), "Symmetry: θ(Kd/k)+θ(Kd*k)=1"
assert N_HILL != HEMO_SITES, "Hill coefficient must NOT equal number of binding sites"

PRIOR_ERRORS = {
    "n_equals_sites":         "Claims Hill coefficient n = number of binding sites",
    "no_cooperativity_sigmoid": "Produces sigmoid curve with n=1 (should be hyperbolic)",
    "kd_not_half_max":        "Gets wrong [L] at θ=0.5 (should be Kd for all n)",
}
