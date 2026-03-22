"""
Effect Size — Frozen Constants
Source: Cohen 1988.  DO NOT MODIFY.
"""
import math

# ── Cohen's d ───────────────────────────────────────────────────────────
# d = (M₁ − M₂) / SD_pooled
#
# CORRECT pooled SD (weights by degrees of freedom):
#   SD_pooled = √( ((n₁−1)·s₁² + (n₂−1)·s₂²) / (n₁ + n₂ − 2) )
#
# WRONG pooled SD (assumes n₁ = n₂):
#   SD_pooled_wrong = √( (s₁² + s₂²) / 2 )
#   Only valid when sample sizes are equal.

# ── Effect-size benchmarks (Cohen 1988) ────────────────────────────────
# Cohen's d:  small = 0.2,  medium = 0.5,  large = 0.8
# η² (eta²):  small = 0.01, medium = 0.06, large = 0.14
# r:          small = 0.1,  medium = 0.3,  large = 0.5

# ── Test scenario: two-group comparison ────────────────────────────────
M1 = 75        # Group 1 mean
M2 = 70        # Group 2 mean
S1 = 10        # Group 1 SD
S2 = 12        # Group 2 SD
N1 = 30        # Group 1 sample size
N2 = 25        # Group 2 sample size

# ── Correct computation ────────────────────────────────────────────────
# SD_pooled = √( (29·100 + 24·144) / 53 )
#           = √( (2900 + 3456) / 53 )
#           = √( 6356 / 53 )
#           = √119.924528…
#           ≈ 10.9510…
SD_POOLED_CORRECT = math.sqrt(((N1 - 1) * S1**2 + (N2 - 1) * S2**2)
                               / (N1 + N2 - 2))   # 10.951005812339194

# d = (75 − 70) / 10.9510… ≈ 0.4566
D_CORRECT = (M1 - M2) / SD_POOLED_CORRECT          # 0.45657906549243016

# ── Wrong computation (equal-n shortcut when n₁ ≠ n₂) ─────────────────
# SD_pooled_wrong = √( (100 + 144) / 2 ) = √122 ≈ 11.0454
SD_POOLED_WRONG = math.sqrt((S1**2 + S2**2) / 2)   # 11.045361017187261

# d_wrong = 5 / 11.0454 ≈ 0.4527
D_WRONG = (M1 - M2) / SD_POOLED_WRONG              # 0.45267873021259264

# ── Eta-squared (η²) test scenario ────────────────────────────────────
# η² = SS_between / SS_total
SS_BETWEEN = 250.0
SS_TOTAL   = 1000.0
ETA_SQUARED = SS_BETWEEN / SS_TOTAL                 # 0.25 (large)

# ── Prior errors catalogue ─────────────────────────────────────────────
PRIOR_ERRORS = {
    "pooled_sd_equal_n":    "Uses √((s₁² + s₂²)/2) when n₁ ≠ n₂; this only "
                            "equals the correct pooled SD when sample sizes are "
                            "equal. Gives 11.045 instead of 10.951.",
    "d_no_pooled":          "Uses s₁ or s₂ alone instead of the pooled SD, "
                            "ignoring variability in the other group.",
    "eta_squared_vs_partial": "Confuses η² = SS_B/SS_T with partial η² = "
                              "SS_B/(SS_B + SS_error); they differ when there "
                              "are multiple factors.",
}
