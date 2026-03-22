"""F-Distribution / One-Way ANOVA — Frozen Constants. Source: Fisher 1925 / NIST. DO NOT MODIFY."""
import math

# One-way ANOVA: F = MSB / MSW  (between / within — NOT within / between)
# df_between = k - 1   (k = number of groups)
# df_within  = N - k   (N = total observations)

# Test scenario: 3 groups, n = 5 each  (k=3, N=15)
K_GROUPS = 3
N_PER_GROUP = 5
N_TOTAL = K_GROUPS * N_PER_GROUP  # 15

GROUP_MEANS = [20.0, 25.0, 30.0]
OVERALL_MEAN = sum(GROUP_MEANS) / len(GROUP_MEANS)  # 25.0

# SSB = n * Σ(mean_i - overall_mean)²
#     = 5 * ((20-25)² + (25-25)² + (30-25)²)
#     = 5 * (25 + 0 + 25) = 250
SSB = N_PER_GROUP * sum((m - OVERALL_MEAN) ** 2 for m in GROUP_MEANS)  # 250.0

# df_between = k - 1 = 2;  df_within = N - k = 12
DF_BETWEEN = K_GROUPS - 1        # 2
DF_WITHIN = N_TOTAL - K_GROUPS   # 12

# MSB = SSB / df_between = 250 / 2 = 125
MSB = SSB / DF_BETWEEN  # 125.0

# Assume SSW = 120
SSW = 120.0
MSW = SSW / DF_WITHIN   # 10.0

# F = MSB / MSW = 125 / 10 = 12.5
F_STAT = MSB / MSW  # 12.5

# Critical value at α = 0.05, df1 = 2, df2 = 12
F_CRIT_005 = 3.8853

PRIOR_ERRORS = {
    "df_swapped":          "Uses df1=N-k, df2=k-1 — numerator and denominator df backwards",
    "f_msw_over_msb":      "Computes F = MSW/MSB instead of MSB/MSW (ratio inverted)",
    "df_within_n_minus_1": "Uses N-1 instead of N-k for df_within",
}
