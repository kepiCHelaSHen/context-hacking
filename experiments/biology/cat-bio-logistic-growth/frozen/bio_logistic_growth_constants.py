"""Logistic Growth — Frozen Constants. Source: Verhulst 1838. DO NOT MODIFY."""
import math

# Logistic growth model:
#   N(t) = K / (1 + ((K - N0) / N0) * exp(-r * t))
#   dN/dt = r * N * (1 - N / K)
#
# Inflection point: N = K/2 (maximum growth rate occurs at HALF carrying capacity)
# Max growth rate at inflection: dN/dt_max = r * K / 4
#
# KEY: Inflection is at K/2, NOT at K.  Max growth rate is at N=K/2, NOT at N~0.
#
# Test parameters: r=0.5, K=1000, N0=10
#   N(10) = 1000 / (1 + 99*exp(-5))
#        = 1000 / (1 + 99*0.006738...)
#        = 1000 / (1 + 0.667060...)
#        = 1000 / 1.667060...
#        = 599.84...
#   N(20) = 1000 / (1 + 99*exp(-10))
#        = 1000 / (1 + 99*0.00004540...)
#        = 1000 / 1.004494...
#        = 995.53...
#   Inflection at N = K/2 = 500
#   Max growth rate = r*K/4 = 0.5*1000/4 = 125.0

R = 0.5
K = 1000
N0 = 10

# Precomputed reference values
N_AT_10 = K / (1 + ((K - N0) / N0) * math.exp(-R * 10))   # 599.84...
N_AT_20 = K / (1 + ((K - N0) / N0) * math.exp(-R * 20))   # 995.53...
INFLECTION_N = K / 2                                        # 500.0
MAX_GROWTH_RATE = R * K / 4                                 # 125.0

# Verify frozen values
assert math.isclose(N_AT_10, 599.8489, rel_tol=1e-4), f"N(10) wrong: {N_AT_10}"
assert math.isclose(N_AT_20, 995.5308, rel_tol=1e-4), f"N(20) wrong: {N_AT_20}"
assert INFLECTION_N == 500.0, f"Inflection wrong: {INFLECTION_N}"
assert MAX_GROWTH_RATE == 125.0, f"Max growth rate wrong: {MAX_GROWTH_RATE}"

# dN/dt at several N values for verification
# dN/dt = r * N * (1 - N/K)
DNDT_AT_100 = R * 100 * (1 - 100 / K)    # 0.5 * 100 * 0.9 = 45.0
DNDT_AT_500 = R * 500 * (1 - 500 / K)    # 0.5 * 500 * 0.5 = 125.0 (max!)
DNDT_AT_900 = R * 900 * (1 - 900 / K)    # 0.5 * 900 * 0.1 = 45.0

assert math.isclose(DNDT_AT_100, 45.0)
assert math.isclose(DNDT_AT_500, 125.0)
assert math.isclose(DNDT_AT_900, 45.0)
# Symmetry: dN/dt at N=100 equals dN/dt at N=900 (equidistant from K/2)
assert math.isclose(DNDT_AT_100, DNDT_AT_900)
# Max occurs at K/2
assert DNDT_AT_500 > DNDT_AT_100
assert DNDT_AT_500 > DNDT_AT_900

PRIOR_ERRORS = {
    "inflection_at_K":  "Claims inflection at N=K instead of N=K/2",
    "max_rate_at_0":    "Claims maximum growth rate when N is small (near 0)",
    "r_changes_K":      "Confuses growth rate r with carrying capacity K",
}
