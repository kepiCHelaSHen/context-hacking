"""Feedback Stability (Routh-Hurwitz) — Frozen Constants. Source: Ogata, Modern Control Engineering 5th Ed; Dorf & Bishop, Modern Control Systems. DO NOT MODIFY."""

# Routh-Hurwitz Stability Criterion (3rd-order polynomials)
# Given characteristic polynomial  a3*s³ + a2*s² + a1*s + a0
# Build the Routh array:
#   Row 3:  a3,  a1
#   Row 2:  a2,  a0
#   Row 1:  (a2*a1 - a3*a0) / a2,  0
#   Row 0:  a0
# First column: [a3, a2, (a2*a1 - a3*a0)/a2, a0]
# Number of sign changes in first column = number of RHP poles
# Stable iff ALL first-column entries positive (zero sign changes)

# LLM prior errors:
#   "sign_changes_wrong" — miscounts sign changes in first column
#   "routh_array_wrong"  — wrong computation of intermediate row entries
#   "necessary_not_sufficient" — only checks positive coefficients (necessary
#       condition) but skips the full Routh test, missing unstable systems
#       where all coefficients are positive

# ── Stable example ──────────────────────────────────────────────
# Polynomial: s³ + 2s² + 3s + 4   →  coeffs = [1, 2, 3, 4]
STABLE_COEFFS = [1, 2, 3, 4]
# Routh array first column:
#   Row 3: a3 = 1
#   Row 2: a2 = 2
#   Row 1: (2*3 - 1*4) / 2 = (6-4)/2 = 1
#   Row 0: a0 = 4
STABLE_FIRST_COL = [1, 2, 1, 4]
STABLE_SIGN_CHANGES = 0
STABLE_IS_STABLE = True

# ── Unstable example ────────────────────────────────────────────
# Polynomial: s³ + s² + 2s + 8   →  coeffs = [1, 1, 2, 8]
UNSTABLE_COEFFS = [1, 1, 2, 8]
# Routh array first column:
#   Row 3: a3 = 1
#   Row 2: a2 = 1
#   Row 1: (1*2 - 1*8) / 1 = -6
#   Row 0: a0 = 8
UNSTABLE_FIRST_COL = [1, 1, -6, 8]
UNSTABLE_SIGN_CHANGES = 2       # 1→-6 (pos→neg), -6→8 (neg→pos)
UNSTABLE_RHP_POLES = 2
UNSTABLE_IS_STABLE = False

# ── Necessary condition (all coefficients positive) ─────────────
# For the UNSTABLE polynomial [1, 1, 2, 8], all coefficients are positive.
# The necessary condition passes, but the system is UNSTABLE.
# This proves the necessary condition alone is NOT sufficient.
UNSTABLE_NECESSARY_PASSES = True   # all coeffs > 0
# A polynomial with a negative coefficient: s³ - s² + 2s + 4 → [1, -1, 2, 4]
NEG_COEFF_COEFFS = [1, -1, 2, 4]
NEG_COEFF_NECESSARY_PASSES = False  # -1 < 0 → fails necessary condition

# ── Second stable example (for extra coverage) ──────────────────
# Polynomial: s³ + 4s² + 5s + 2   →  coeffs = [1, 4, 5, 2]
STABLE2_COEFFS = [1, 4, 5, 2]
# Row 3: 1
# Row 2: 4
# Row 1: (4*5 - 1*2)/4 = (20-2)/4 = 18/4 = 4.5
# Row 0: 2
STABLE2_FIRST_COL = [1, 4, 4.5, 2]
STABLE2_SIGN_CHANGES = 0
STABLE2_IS_STABLE = True

PRIOR_ERRORS = {
    "sign_changes_wrong":      "Miscounts sign changes in the first column of the Routh array",
    "routh_array_wrong":       "Computes intermediate Routh row entries incorrectly (wrong cross-multiply or division)",
    "necessary_not_sufficient": "Only checks that all polynomial coefficients are positive (necessary condition) but does not perform the full Routh array test — misses unstable systems like s³+s²+2s+8",
}
