"""Transfer Function — Frozen Constants. Source: Ogata, Modern Control Engineering 5th Ed. DO NOT MODIFY."""
import math

# H(s) = N(s) / D(s)
# Zeros = roots of N(s)  (where output is ZERO)
# Poles = roots of D(s)  (where output is INFINITE)
# KEY: Poles determine stability — ALL poles must have Re(s) < 0 for BIBO stability
# Zeros do NOT affect stability directly
# LLM prior: swaps poles/zeros, claims RHP zeros cause instability

# Test system: H(s) = (s+2) / ((s+1)(s+3)) = (s+2) / (s² + 4s + 3)
NUM_COEFFS = [1.0, 2.0]          # s + 2  (descending powers: 1·s¹ + 2·s⁰)
DEN_COEFFS = [1.0, 4.0, 3.0]    # s² + 4s + 3  (descending: 1·s² + 4·s¹ + 3·s⁰)

ZEROS = [-2.0]                    # roots of N(s): s + 2 = 0 → s = -2
POLES = [-1.0, -3.0]             # roots of D(s): (s+1)(s+3) = 0 → s = -1, -3

# Stability: all poles in LHP (Re < 0) → STABLE
IS_STABLE = True

# DC gain: H(0) = N(0)/D(0) = 2 / (1*3) = 2/3
DC_GAIN = 2.0 / 3.0              # ≈ 0.6667

# Unstable system: H(s) = 1 / (s - 1) → pole at s = +1 (RHP) → UNSTABLE
UNSTABLE_POLE = 1.0
UNSTABLE_IS_STABLE = False

# Quadratic formula: roots of as² + bs + c
# For s² + 4s + 3: a=1, b=4, c=3
# discriminant = 16 - 12 = 4, sqrt(disc)=2
# roots = (-4 ± 2) / 2 = -1, -3
QUAD_A, QUAD_B, QUAD_C = 1.0, 4.0, 3.0
QUAD_DISC = QUAD_B**2 - 4*QUAD_A*QUAD_C   # = 4.0
QUAD_ROOTS = [(-QUAD_B + math.sqrt(QUAD_DISC)) / (2*QUAD_A),
              (-QUAD_B - math.sqrt(QUAD_DISC)) / (2*QUAD_A)]  # [-1.0, -3.0]

# H(s) evaluated from factored form at s = 0:
# H(0) = (0 - (-2)) / ((0 - (-1))*(0 - (-3))) = 2 / 3
FACTORED_AT_ZERO = 2.0 / 3.0

# H(s) at s = -0.5: (−0.5+2) / ((−0.5+1)(−0.5+3)) = 1.5 / (0.5*2.5) = 1.5 / 1.25 = 1.2
H_AT_NEG05 = 1.2

PRIOR_ERRORS = {
    "poles_zeros_swapped":  "Calls roots of numerator 'poles' (they are ZEROS)",
    "rhp_zero_unstable":    "Claims RHP zeros cause instability (only POLES do)",
    "dc_gain_wrong":        "Evaluates H at s=1 instead of s=0 for DC gain",
}
