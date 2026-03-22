"""Multiple Regression — Frozen Constants. Source: Kutner et al. DO NOT MODIFY."""
import math

# Multiple regression: Y = beta0 + beta1*X1 + beta2*X2 + ... + epsilon
# VIF (Variance Inflation Factor) = 1 / (1 - R^2_j)
#   where R^2_j is R^2 from regressing predictor j on all other predictors
# VIF > 10 → severe multicollinearity
# VIF >  5 → moderate multicollinearity
# KEY FACT: Partial regression coefficient ≠ total correlation.
#   When predictors are collinear, individual coefficients become unstable
#   (large standard errors) and cannot be interpreted as "the effect of Xj
#   holding all else constant" because the other variables *cannot* be held
#   constant when they move in lockstep with Xj.

# --- Test scenario ---
# True model: Y = 3 + 2*X1 + 0.5*X2  (deterministic, no noise)
# X1 and X2 are nearly collinear (r ≈ 0.995)
#
# X1 = [1, 2, 3, 4, 5]
# X2 = [1.1, 2.2, 2.8, 4.1, 4.9]
# mean_x1 = 3.0,  mean_x2 = 3.02
#
# Pearson r(X1, X2):
#   dx1 = [-2, -1, 0, 1, 2]
#   dx2 = [-1.92, -0.82, -0.22, 1.08, 1.88]
#   num  = (-2)(-1.92) + (-1)(-0.82) + 0(-0.22) + 1(1.08) + 2(1.88)
#        = 3.84 + 0.82 + 0 + 1.08 + 3.76 = 9.5
#   ss_x1 = 4 + 1 + 0 + 1 + 4 = 10
#   ss_x2 = 3.6864 + 0.6724 + 0.0484 + 1.1664 + 3.5344 = 9.108
#   r = 9.5 / sqrt(10 * 9.108) = 9.5 / 9.54357... ≈ 0.99543
#
# R^2 (X1 on X2) ≈ 0.99089
# VIF = 1 / (1 - 0.99089) ≈ 109.7  → SEVERE multicollinearity
#
# Y (deterministic) = [5.55, 8.1, 10.4, 13.05, 15.45]

X1_DATA = [1, 2, 3, 4, 5]
X2_DATA = [1.1, 2.2, 2.8, 4.1, 4.9]
Y_DATA = [5.55, 8.1, 10.4, 13.05, 15.45]

N = 5
MEAN_X1 = 3.0
MEAN_X2 = 3.02

CORR_X1_X2 = round(9.5 / math.sqrt(10 * 9.108), 5)              # 0.99543
R_SQ_X1_ON_X2 = round(CORR_X1_X2 ** 2, 5)                        # 0.99089
VIF_X1 = round(1 / (1 - R_SQ_X1_ON_X2), 1)                       # 109.7

VIF_THRESHOLD_MODERATE = 5
VIF_THRESHOLD_SEVERE = 10

# True coefficients (known because we generated the data)
TRUE_BETA0 = 3.0
TRUE_BETA1 = 2.0
TRUE_BETA2 = 0.5

PRIOR_ERRORS = {
    "ignores_vif":                  "Doesn't check VIF before interpreting partial "
                                    "regression coefficients — high VIF means the "
                                    "coefficient estimates are unstable and unreliable",
    "partial_as_total":             "Treats the partial regression coefficient of X1 as "
                                    "the total effect of X1 on Y, ignoring that X2 is "
                                    "confounded with X1",
    "collinear_coefficients_stable": "Assumes individual coefficient estimates remain "
                                     "stable and meaningful despite VIF >> 10 — in "
                                     "reality, small data perturbations cause wild "
                                     "swings in the coefficient values",
}
