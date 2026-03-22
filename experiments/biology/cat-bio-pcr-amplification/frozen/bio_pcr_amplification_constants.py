"""PCR Amplification — Frozen Constants. Source: Saiki et al. 1988, Pfaffl 2001. DO NOT MODIFY."""
import math

# PCR amplification: N(c) = N₀ * (1 + E)^c
#   N₀ = initial template copies
#   E  = amplification efficiency (0 < E ≤ 1)
#   c  = number of cycles
#
# IDEAL model (100% efficiency, E=1): N(c) = N₀ * 2^c
# REAL  model (typical E≈0.95):       N(c) = N₀ * 1.95^c
#
# The ideal model overestimates yield because real PCR never reaches
# 100% efficiency — primer annealing, polymerase processivity, and
# reagent depletion all reduce E below 1.0. Typical E is 0.90–0.98.
#
# After 30 cycles with N₀=1:
#   Ideal: 2^30     = 1,073,741,824
#   Real:  1.95^30  ≈   502,386,940  (roughly half the ideal!)

N0 = 1                # initial template copy number
E_IDEAL = 1.0         # perfect efficiency (LLM default assumption)
E_TYPICAL = 0.95      # real-world typical efficiency
CYCLES = 30           # standard PCR cycle count

# Precomputed reference values
N_IDEAL_30 = N0 * 2 ** CYCLES                       # 1073741824
N_REAL_30 = N0 * (1 + E_TYPICAL) ** CYCLES           # 502386939.8554185
RATIO = N_REAL_30 / N_IDEAL_30                        # ~0.4679

# Sanity checks
assert N_IDEAL_30 == 1073741824, f"Ideal yield wrong: {N_IDEAL_30}"
assert math.isclose(N_REAL_30, 502386939.8554185, rel_tol=1e-9), \
    f"Real yield wrong: {N_REAL_30}"
assert 0.46 < RATIO < 0.48, f"Ratio out of range: {RATIO}"
assert N_REAL_30 < N_IDEAL_30, "Real yield must be less than ideal yield"
assert 0 < E_TYPICAL <= 1.0, "Efficiency must be in (0, 1]"

# Cycles needed for 1e6-fold amplification at E=0.95
CYCLES_FOR_1M_FOLD = math.ceil(math.log(1e6) / math.log(1 + E_TYPICAL))  # 21
assert CYCLES_FOR_1M_FOLD == 21, f"Cycles for 1M-fold wrong: {CYCLES_FOR_1M_FOLD}"

PRIOR_ERRORS = {
    "assumes_100_efficiency": "Uses 2^c instead of (1+E)^c — assumes perfect doubling every cycle",
    "efficiency_gt_1":        "Uses efficiency E > 1 which is physically impossible",
    "linear_not_exponential": "Models PCR as linear growth instead of exponential amplification",
}
