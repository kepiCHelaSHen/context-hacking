"""Correlation — Frozen Constants. Source: Pearson 1896 / Spearman 1904. DO NOT MODIFY."""
import math

# Pearson r = sum((xi - x_bar)(yi - y_bar)) / sqrt(sum((xi - x_bar)^2) * sum((yi - y_bar)^2))
# Spearman rho = Pearson r computed on ranks of x and y (handles ties via average-rank)
# Shortcut (no ties only): rho = 1 - 6*sum(d^2) / (n*(n^2 - 1))
# r is in [-1, 1];  r^2 = proportion of variance explained
# CORRELATION DOES NOT IMPLY CAUSATION (confounders, reverse causation, coincidence)

# --- Test data ---
# x = [1, 2, 3, 4, 5],  y = [2, 4, 5, 4, 5]
# x_bar = 3.0,  y_bar = 4.0
# (xi - x_bar):  [-2, -1, 0, 1, 2]
# (yi - y_bar):  [-2,  0, 1, 0, 1]
# sum((xi-x_bar)(yi-y_bar)) = 4 + 0 + 0 + 0 + 2 = 6
# sum((xi-x_bar)^2) = 4 + 1 + 0 + 1 + 4 = 10
# sum((yi-y_bar)^2) = 4 + 0 + 1 + 0 + 1 = 6
# r = 6 / sqrt(10 * 6) = 6 / sqrt(60) = 6 / 7.74597 = 0.77460
# r^2 = 36 / 60 = 0.6  (60% of variance explained)
#
# Spearman: ranks via average-rank method
#   sorted y = [2, 4, 4, 5, 5]  positions [1, 2, 3, 4, 5]
#   y=2 -> rank 1,  y=4 -> avg(2,3) = 2.5,  y=5 -> avg(4,5) = 4.5
#   ranks_x = [1, 2, 3, 4, 5]
#   ranks_y = [1, 2.5, 4.5, 2.5, 4.5]
#   rx_bar = 3.0,  ry_bar = 3.0
#   (rxi - rx_bar): [-2, -1, 0, 1, 2]
#   (ryi - ry_bar): [-2, -0.5, 1.5, -0.5, 1.5]
#   num = 4 + 0.5 + 0 - 0.5 + 3 = 7
#   den_x = 10,  den_y = 4 + 0.25 + 2.25 + 0.25 + 2.25 = 9
#   rho = 7 / sqrt(10 * 9) = 7 / sqrt(90) = 7 / 9.48683 = 0.73786
#
# NOTE: the no-tie shortcut rho = 1 - 6*sum(d^2)/(n*(n^2-1)) gives a WRONG
# answer here because y has ties.  d^2 = [0, 0.25, 2.25, 2.25, 0.25] = 5.0
# shortcut would give 1 - 6*5/(5*24) = 1 - 30/120 = 0.75  (WRONG: 0.75 != 0.73786)
# The correct approach with ties is Pearson-on-ranks.

X_DATA = [1, 2, 3, 4, 5]
Y_DATA = [2, 4, 5, 4, 5]
N = 5
X_BAR = 3.0
Y_BAR = 4.0

PEARSON_R = 6 / math.sqrt(60)                   # 0.7745966692414834
R_SQUARED = 0.6                                  # 36/60
SPEARMAN_RHO = 7 / math.sqrt(90)                # 0.7378647873726218

PRIOR_ERRORS = {
    "correlation_causation":  "Infers that a high correlation coefficient means one "
                              "variable causes changes in the other — correlation "
                              "does not establish causation (confounders may exist)",
    "r_squared_is_r":         "Confuses r with r^2: reports r as if it were the "
                              "proportion of variance explained (r^2 is, r is not)",
    "spearman_no_ties":       "Uses the shortcut formula rho = 1 - 6*sum(d^2)/(n*(n^2-1)) "
                              "when ties are present — this gives wrong results; "
                              "must compute Pearson r on averaged ranks instead",
}
