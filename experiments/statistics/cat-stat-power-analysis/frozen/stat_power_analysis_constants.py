"""Power Analysis — Frozen Constants. Source: Cohen 1988. DO NOT MODIFY."""
import math

# ---------------------------------------------------------------------------
# Cohen's d conventions (standardized effect size = (mu1 - mu2) / sigma_pooled)
# ---------------------------------------------------------------------------
D_SMALL = 0.2
D_MEDIUM = 0.5
D_LARGE = 0.8

# ---------------------------------------------------------------------------
# Test parameters: two-tailed alpha = 0.05, power = 0.80 (beta = 0.20)
# ---------------------------------------------------------------------------
ALPHA = 0.05
POWER = 0.80
Z_ALPHA2 = 1.96          # z_{alpha/2} for two-tailed test at alpha = 0.05
Z_BETA = 0.8416          # z_{power} = z_{0.80}

# ---------------------------------------------------------------------------
# Reference scenario: two populations differ by Delta = 5, sigma = 10
# Correct standardisation: d = Delta / sigma = 5 / 10 = 0.5
# ---------------------------------------------------------------------------
DELTA_RAW = 5.0
SIGMA = 10.0
D_CORRECT = 0.5          # = DELTA_RAW / SIGMA

# ---------------------------------------------------------------------------
# Correct sample size per group (two-sample t-test, equal groups):
#   n = ceil( ((z_alpha2 + z_beta)^2 * 2) / d^2 )
#   n = ceil( ((1.96 + 0.8416)^2 * 2) / 0.5^2 )
#   n = ceil( (7.8490 * 2) / 0.25 )
#   n = ceil( 62.7917 )  =  63
# ---------------------------------------------------------------------------
N_PER_GROUP = 63

# ---------------------------------------------------------------------------
# Prior errors LLMs commonly make
# ---------------------------------------------------------------------------
PRIOR_ERRORS = {
    "raw_not_standardized": (
        "Uses raw difference Delta in the sample-size formula instead of "
        "the standardised effect size d = Delta / sigma"
    ),
    "forgets_round_up": (
        "Returns the floating-point result instead of rounding up to the "
        "next integer (sample sizes must be whole numbers)"
    ),
    "one_group_n": (
        "Reports the per-group n as the total sample size, or gives "
        "total n instead of per-group n"
    ),
}
