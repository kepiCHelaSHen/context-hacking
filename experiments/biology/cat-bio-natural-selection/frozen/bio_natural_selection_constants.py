"""Natural Selection — Frozen Constants. Source: Gillespie, Population Genetics. DO NOT MODIFY."""
import math

# Standard parameterization: w_AA = 1, w_Aa = 1 - hs, w_aa = 1 - s
# h = dominance coefficient:
#   h = 0   : A fully dominant (heterozygote same fitness as AA)
#   h = 0.5 : additive / codominant (heterozygote midpoint)
#   h = 1   : a fully dominant (heterozygote same fitness as aa)

# KEY DISTINCTION — additive vs multiplicative fitness:
#   Additive:        w_Aa = (w_AA + w_aa) / 2           (arithmetic mean)
#   Multiplicative:  w_Aa = sqrt(w_AA * w_aa)            (geometric mean)
#   These coincide only when s -> 0; they DIFFER for large s.

# Test case: s = 0.4, h = 0.5 (additive/codominant case)
S = 0.4
H = 0.5
W_AA = 1.0
W_Aa = 1.0 - H * S                       # = 0.8
W_aa = 1.0 - S                           # = 0.6

# Additive check: (1.0 + 0.6) / 2 = 0.8  (matches W_Aa when h = 0.5)
# Multiplicative heterozygote: sqrt(1.0 * 0.6) = 0.7746 != 0.8
W_Aa_MULT = math.sqrt(W_AA * W_aa)       # = 0.7745966...

# Allele frequency dynamics
# Mean fitness: w_bar = p^2 * w_AA + 2pq * w_Aa + q^2 * w_aa
# Delta p:      dp = pq [p(w_AA - w_Aa) + q(w_Aa - w_aa)] / w_bar

# Test case: p = 0.3 (q = 0.7)
P_TEST = 0.3
Q_TEST = 1.0 - P_TEST                    # = 0.7

# w_bar = 0.09*1.0 + 2*0.21*0.8 + 0.49*0.6 = 0.09 + 0.336 + 0.294 = 0.72
W_BAR = (P_TEST**2 * W_AA
         + 2 * P_TEST * Q_TEST * W_Aa
         + Q_TEST**2 * W_aa)              # = 0.72

# delta_p = 0.21 * [0.3*0.2 + 0.7*0.2] / 0.72
#         = 0.21 * 0.2 / 0.72 = 0.042 / 0.72 = 0.058333...
DELTA_P = (P_TEST * Q_TEST
           * (P_TEST * (W_AA - W_Aa) + Q_TEST * (W_Aa - W_aa))
           / W_BAR)                       # = 0.058333...

PRIOR_ERRORS = {
    "additive_equals_multiplicative": "Treats additive and multiplicative fitness models as identical",
    "h_ignored":                      "Forgets dominance coefficient h in heterozygote fitness",
    "delta_p_no_wbar":                "Computes delta-p without dividing by mean fitness w-bar",
}
