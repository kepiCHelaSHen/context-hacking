"""OLS Regression — Frozen Constants. Source: Gauss 1809 / NIST. DO NOT MODIFY."""
import math
# Simple linear regression: y_hat = beta0 + beta1 * x
# beta1 = sum((xi - x_bar)(yi - y_bar)) / sum((xi - x_bar)^2)
# beta0 = y_bar - beta1 * x_bar
# R^2 = 1 - SSR/SST   where SSR = sum of squared residuals, SST = sum of squares total
# Adjusted R^2 = 1 - (1 - R^2)(n-1)/(n-p-1)   where p = number of predictors
# KEY FACT: R^2 ALWAYS increases (or stays the same) when adding predictors,
#   even random noise predictors.  Adjusted R^2 can *decrease*.
#   Therefore model comparison across different numbers of predictors
#   MUST use adjusted R^2, not R^2.

# --- Test data ---
# x = [1, 2, 3, 4, 5],  y = [2.1, 3.9, 6.2, 7.8, 10.1]
# x_bar = 3.0,  y_bar = 6.02
# (xi - x_bar):  [-2, -1, 0, 1, 2]
# (yi - y_bar):  [-3.92, -2.12, 0.18, 1.78, 4.08]
# sum((xi-x_bar)(yi-y_bar)) = 7.84 + 2.12 + 0 + 1.78 + 8.16 = 19.9
# sum((xi-x_bar)^2) = 4 + 1 + 0 + 1 + 4 = 10
# beta1 = 19.9 / 10 = 1.99
# beta0 = 6.02 - 1.99*3 = 0.05
# y_pred = [2.04, 4.03, 6.02, 8.01, 10.00]
# residuals = [0.06, -0.13, 0.18, -0.21, 0.10]
# SSR = 0.0036 + 0.0169 + 0.0324 + 0.0441 + 0.01 = 0.107
# SST = 15.3664 + 4.4944 + 0.0324 + 3.1684 + 16.6464 = 39.708
# R^2 = 1 - 0.107/39.708 = 0.99731  (very high — near-linear data)
# Adj R^2 (p=1, n=5) = 1 - (1-0.99731)(4/3) = 1 - 0.003587 = 0.99641

X_DATA = [1, 2, 3, 4, 5]
Y_DATA = [2.1, 3.9, 6.2, 7.8, 10.1]
N = 5
P = 1  # number of predictors (simple linear regression)
X_BAR = 3.0
Y_BAR = 6.02

BETA1 = 1.99
BETA0 = 0.05
Y_PRED = [2.04, 4.03, 6.02, 8.01, 10.00]

SSR = 0.107    # sum of squared residuals (yi - y_hat_i)^2
SST = 39.708   # total sum of squares   (yi - y_bar)^2

R_SQUARED = round(1 - SSR / SST, 5)           # 0.99731
ADJ_R_SQUARED = round(1 - (1 - R_SQUARED) * (N - 1) / (N - P - 1), 5)  # 0.99641

PRIOR_ERRORS = {
    "r2_always_better":   "Uses R^2 instead of adjusted R^2 for model comparison "
                          "across different numbers of predictors — R^2 always "
                          "increases with more predictors, masking overfitting",
    "ssr_sst_swap":       "Swaps SSR and SST in R^2 formula (computes SSR/SST "
                          "instead of 1 - SSR/SST)",
    "beta1_wrong_denom":  "Uses sum(xi*yi) instead of sum((xi-x_bar)(yi-y_bar)) "
                          "for the numerator of beta1",
}
