"""
Bootstrap — Frozen Constants
Source: Efron 1979.  DO NOT MODIFY.
"""
import math

# ── Bootstrap Resampling ─────────────────────────────────────────────
# Resample WITH replacement from original sample (size n), compute
# statistic on resample, repeat B times.
#
# KEY: must be WITH replacement.  Without replacement just gives the
# original sample in a different order (a permutation), which carries
# no new information about sampling variability.
#
# Number of distinct bootstrap samples from n items (stars and bars):
#   C(2n-1, n)
# For n=5:  C(9, 5) = 126

# ── Test data ────────────────────────────────────────────────────────
DATA = (2, 5, 8, 11, 14)
N = 5

ORIGINAL_MEAN = 8.0          # sum(DATA) / N = 40 / 5
ORIGINAL_MEDIAN = 8          # middle element of sorted DATA

# Sample variance (Bessel-corrected, ddof=1):
# Σ(xi − x̄)² / (n−1) = (36+9+0+9+36)/4 = 90/4
SAMPLE_VAR = 22.5

# Theoretical SE of the mean: s / √n
# √22.5 ≈ 4.74341649025257, SE ≈ 4.74341649025257 / √5
THEORETICAL_SE = round(math.sqrt(SAMPLE_VAR) / math.sqrt(N), 4)  # 2.1213

# ── Probability of at least one repeat in a bootstrap resample ──────
# P(all distinct) = n! / n^n   (ordered sampling without repeat)
# For n=5: 120 / 3125 = 0.0384
# P(any repeat) = 1 − P(all distinct) = 0.9616
#
# This shows that 96.16 % of bootstrap resamples contain at least one
# duplicate, proving WITH replacement matters.
P_ANY_REPEAT = round(1.0 - math.factorial(N) / (N ** N), 4)  # 0.9616

# Number of distinct bootstrap samples (stars-and-bars):
N_DISTINCT_BOOTSTRAP = math.comb(2 * N - 1, N)  # C(9,5) = 126

# ── Correct vs wrong resampling scheme ──────────────────────────────
WITH_REPLACEMENT = True       # correct — bootstrap resampling
WITHOUT_REPLACEMENT = False   # wrong — that is just a permutation

# ── Prior errors catalogue ──────────────────────────────────────────
PRIOR_ERRORS = {
    "without_replacement":       "Samples without replacement, yielding permutations "
                                 "of the original data instead of true bootstrap resamples",
    "bootstrap_n_different":     "Uses a resample size different from n; the bootstrap "
                                 "requires resamples of the same size as the original",
    "single_bootstrap_sufficient": "Uses B=1 instead of B >> 1; a single resample cannot "
                                   "estimate sampling variability",
}
