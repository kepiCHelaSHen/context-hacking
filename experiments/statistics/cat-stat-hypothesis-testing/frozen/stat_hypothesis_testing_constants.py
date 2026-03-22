"""Hypothesis Testing — Frozen Constants. Source: Neyman-Pearson 1933. DO NOT MODIFY."""
import math
# Type I error (alpha): reject H0 when H0 is true (false positive)
# Type II error (beta): fail to reject H0 when H0 is false (false negative)
# Power = 1 - beta (probability of correctly rejecting a false H0)
# p-value: P(data as extreme or more | H0 true), NOT P(H0 true | data)
#
# Test scenario: one-sample z-test, H0: mu=100, H1: mu != 100
#   n=25, xbar=104, sigma=10
#   SE = sigma / sqrt(n) = 10 / 5 = 2.0
#   z  = (xbar - mu0) / SE = (104 - 100) / 2.0 = 2.0
#   Two-tailed p-value = 2*(1 - Phi(2.0))
#     Phi(2.0) = 0.5*(1 + erf(2/sqrt(2))) = 0.97725
#     p = 2 * 0.02275 = 0.04550
#   At alpha=0.05: reject H0 (p=0.04550 < 0.05)
#   At alpha=0.01: fail to reject (p=0.04550 > 0.01)
MU_0 = 100.0
XBAR = 104.0
SIGMA = 10.0
N = 25
SE = SIGMA / math.sqrt(N)              # = 2.0
Z_STAT = (XBAR - MU_0) / SE            # = 2.0
P_VALUE_TWO = 1.0 - math.erf(abs(Z_STAT) / math.sqrt(2))  # = 0.04550
ALPHA_05 = 0.05
ALPHA_01 = 0.01
PRIOR_ERRORS = {
    "p_value_is_prob_h0":  "Claims p-value = P(H0 true) instead of P(data | H0 true)",
    "alpha_beta_swap":     "Confuses Type I (alpha) and Type II (beta) error rates",
    "one_tail_for_two":    "Forgets to double for two-tailed test (uses 1-Phi instead of 2*(1-Phi))",
}
