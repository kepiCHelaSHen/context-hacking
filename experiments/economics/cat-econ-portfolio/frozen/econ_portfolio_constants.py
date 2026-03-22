"""Portfolio Theory (Markowitz) — Frozen Constants. Source: Markowitz (1952), Bodie/Kane/Marcus 12th Ed Ch 7. DO NOT MODIFY."""
import math

# Portfolio return: E(Rp) = sum(wi * E(Ri))
# Portfolio variance: sigma_p^2 = sum_i sum_j wi*wj*sigma_ij  (includes ALL cross terms!)
# For 2 assets: sigma_p^2 = w1^2*s1^2 + w2^2*s2^2 + 2*w1*w2*sigma12
# KEY: The covariance term (2*w1*w2*sigma12) is critical. Without it, variance is WRONG.
# If rho < 1, diversification reduces risk below the weighted average.
# sigma12 = rho * s1 * s2  (covariance = correlation * product of std devs)

# Test scenario: 2-asset portfolio
W1, W2 = 0.6, 0.4
ER1, ER2 = 0.10, 0.15          # expected returns
S1, S2 = 0.12, 0.20            # std devs
RHO = 0.3                       # correlation

# Derived values
ER_P = W1 * ER1 + W2 * ER2                          # = 0.12 (12%)
COV12 = RHO * S1 * S2                                # = 0.3 * 0.12 * 0.20 = 0.0072
VAR_P = W1**2 * S1**2 + W2**2 * S2**2 + 2 * W1 * W2 * COV12
# = 0.36*0.0144 + 0.16*0.04 + 2*0.24*0.0072
# = 0.005184 + 0.0064 + 0.003456 = 0.01504
STD_P = math.sqrt(VAR_P)                             # = 0.12264 (12.26%)

# Wrong answer WITHOUT covariance term
VAR_P_WRONG = W1**2 * S1**2 + W2**2 * S2**2          # = 0.011584
STD_P_WRONG = math.sqrt(VAR_P_WRONG)                  # = 0.10763 (10.76%)

# Diversification benefit = weighted avg std - portfolio std
WEIGHTED_AVG_STD = W1 * S1 + W2 * S2                  # = 0.6*0.12 + 0.4*0.20 = 0.152
DIV_BENEFIT = WEIGHTED_AVG_STD - STD_P                 # > 0 when rho < 1

PRIOR_ERRORS = {
    "no_covariance":      "Omits 2*w1*w2*sigma12 term from portfolio variance",
    "variance_weighted_avg": "Uses w1*s1 + w2*s2 as portfolio std (not a variance formula)",
    "correlation_ignored": "Assumes rho=0, losing the cross-correlation term",
}
