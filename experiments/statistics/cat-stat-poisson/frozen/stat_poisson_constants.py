"""Poisson Distribution — Frozen Constants. Source: NIST. DO NOT MODIFY."""
import math

# Poisson PMF: P(X=k) = (λ^k * e^(-λ)) / k!
# KEY property: Mean = λ, Variance = λ  (mean equals variance)
# When variance >> mean → overdispersion → Poisson is WRONG → use negative binomial

# Test scenario: λ = 3.0 (average 3 events per interval)
#   P(X=0) = e^(-3)              = 0.049787068367864
#   P(X=1) = 3 * e^(-3)          = 0.149361205103592
#   P(X=2) = (9/2) * e^(-3)      = 0.224041807655388
#   P(X=3) = (27/6) * e^(-3)     = 0.224041807655388
#   P(X≤2) = P(0)+P(1)+P(2)      = 0.423190081126844
#
# Overdispersion test: data with mean=3.0 but variance=9.0
#   ratio = variance / mean = 3.0 → far exceeds 1 → Poisson invalid

LAMBDA = 3.0
P_0 = math.exp(-LAMBDA)                                         # 0.049787068367864
P_1 = LAMBDA * math.exp(-LAMBDA)                                # 0.149361205103592
P_2 = (LAMBDA ** 2 / math.factorial(2)) * math.exp(-LAMBDA)     # 0.224041807655388
P_3 = (LAMBDA ** 3 / math.factorial(3)) * math.exp(-LAMBDA)     # 0.224041807655388
CDF_2 = P_0 + P_1 + P_2                                         # 0.423190081126844

PRIOR_ERRORS = {
    "variance_not_lambda":   "Assumes variance ≠ mean for Poisson (variance IS λ, same as mean)",
    "poisson_overdispersed": "Applies Poisson when variance >> mean (should use negative binomial)",
    "factorial_overflow":    "Doesn't handle large k — factorial grows faster than λ^k",
}
