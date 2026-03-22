"""
Bonferroni Correction — Frozen Constants
Source: Bonferroni 1936 / Benjamini-Hochberg 1995.  DO NOT MODIFY.
"""
import math

# ── Bonferroni Correction ───────────────────────────────────────────────
# Controls Family-Wise Error Rate (FWER):
#   α_adjusted = α / m   where m = number of tests
#
# Conservative: high Type II error (misses true positives).

# ── Benjamini-Hochberg (BH) Procedure ──────────────────────────────────
# Controls False Discovery Rate (FDR) — less conservative.
#   1. Sort p-values: p_(1) ≤ p_(2) ≤ ... ≤ p_(m)
#   2. Find largest k where p_(k) ≤ (k/m) · α
#   3. Reject all H_1 ... H_k

# ── Test scenario: m = 10 simultaneous hypothesis tests ────────────────
M = 10
ALPHA = 0.05

P_VALUES = (0.001, 0.003, 0.008, 0.01, 0.02,
            0.04,  0.06,  0.10,  0.50, 0.90)

# ── Bonferroni computation ──────────────────────────────────────────────
# α_adjusted = α / m = 0.05 / 10 = 0.005
BONFERRONI_THRESHOLD = ALPHA / M                          # 0.005

# Reject p < α_adjusted:
#   p=0.001 < 0.005 ✓  p=0.003 < 0.005 ✓  p=0.008 ✗ ...
BONFERRONI_REJECTIONS = 2                                 # tests 1, 2

# ── Benjamini-Hochberg computation ──────────────────────────────────────
# BH thresholds: (k/m) · α for k = 1..10
#   [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05]
#
# k=1: 0.001 ≤ 0.005 ✓
# k=2: 0.003 ≤ 0.01  ✓
# k=3: 0.008 ≤ 0.015 ✓
# k=4: 0.01  ≤ 0.02  ✓
# k=5: 0.02  ≤ 0.025 ✓
# k=6: 0.04  > 0.03  ✗  ← stops here
# Largest k = 5 → reject tests 1-5

BH_LARGEST_K = 5
BH_REJECTIONS = 5                                         # tests 1-5

# BH rejects 5 vs Bonferroni's 2 — Bonferroni misses 3 true positives!

# ── Prior errors catalogue ──────────────────────────────────────────────
PRIOR_ERRORS = {
    "bonferroni_sufficient":  "Always uses Bonferroni, ignoring FDR methods; "
                              "rejects only 2 instead of 5 discoveries",
    "bh_wrong_threshold":     "Computes BH threshold as α/k instead of (k/m)·α; "
                              "yields incorrect rejection set",
    "no_correction_needed":   "Applies no multiple-comparisons correction at all; "
                              "inflates the family-wise error rate to 1-(1-α)^m ≈ 0.40",
}
