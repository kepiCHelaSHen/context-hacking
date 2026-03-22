"""
Bayes' Theorem — Frozen Constants
Source: Bayes 1763 / Laplace.  DO NOT MODIFY.
"""
import math

# ── Bayes' Theorem ────────────────────────────────────────────────────
# P(A|B) = P(B|A) · P(A) / P(B)
#
# Law of total probability (binary partition):
# P(B) = P(B|A)·P(A) + P(B|¬A)·P(¬A)

# ── Test scenario: Medical screening ─────────────────────────────────
# Disease prevalence
P_DISEASE = 0.01                # P(D)   = 1 %
P_NO_DISEASE = 1 - P_DISEASE    # P(¬D)  = 0.99

# Test characteristics
SENSITIVITY = 0.95              # P(+|D)  — true-positive rate
SPECIFICITY = 0.90              # P(−|¬D) — true-negative rate
FPR = 1 - SPECIFICITY           # P(+|¬D) = 0.10 — false-positive rate

# ── Correct computation ──────────────────────────────────────────────
# P(+) = P(+|D)·P(D) + P(+|¬D)·P(¬D)
#       = 0.95·0.01  + 0.10·0.99
#       = 0.0095     + 0.099
#       = 0.1085
P_POS = SENSITIVITY * P_DISEASE + FPR * P_NO_DISEASE   # 0.1085

# P(D|+) = P(+|D)·P(D) / P(+)
#         = 0.0095 / 0.1085
#         ≈ 0.08755760368663594
POSTERIOR = (SENSITIVITY * P_DISEASE) / P_POS           # 0.087557...

# ── Common LLM error: numerator without denominator ──────────────────
# Wrong answer: P(+|D)·P(D) = 0.95 × 0.01 = 0.0095
# This is just the numerator — NOT a valid probability for P(D|+).
UNNORMALIZED = SENSITIVITY * P_DISEASE                  # 0.0095

# ── Prior errors catalogue ───────────────────────────────────────────
PRIOR_ERRORS = {
    "no_normalizing":    "Returns prior × likelihood without dividing by P(B); "
                         "gives 0.0095 instead of ≈0.0876",
    "base_rate_neglect": "Ignores low prevalence and reports P(D|+) ≈ 0.95, "
                         "confusing P(+|D) with P(D|+)",
    "complement_error":  "Uses P(+|¬D) = 1 − sensitivity (0.05) instead of "
                         "1 − specificity (0.10), corrupting P(+)",
}
