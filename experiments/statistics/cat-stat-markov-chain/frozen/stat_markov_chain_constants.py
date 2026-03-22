"""
Markov Chains — Frozen Constants
Source: Norris 1997.  DO NOT MODIFY.
"""
import math

# ── Markov Chain Basics ─────────────────────────────────────────────────
# Transition matrix P: P[i][j] = P(next state = j | current state = i)
# Rows sum to 1 (stochastic matrix).
#
# Steady state π: πP = π  with  Σπᵢ = 1  (LEFT eigenvector for eigenvalue 1)
# Equivalently: πⱼ = Σᵢ πᵢ · P[i][j]  for all j
#
# Common LLM confusion: solving Pπ = π (RIGHT eigenvector, column-vector
# convention) instead of πP = π (row-vector convention).  Both are valid
# formulations, but the row-vector form matches the standard where P[i][j]
# is the probability of transitioning FROM state i TO state j.

# ── 2-state chain: Sunny / Rainy ───────────────────────────────────────
# State 0 = Sunny, State 1 = Rainy
#
#   P = [[0.8, 0.2],      Sunny→Sunny=0.8, Sunny→Rainy=0.2
#        [0.4, 0.6]]      Rainy→Sunny=0.4, Rainy→Rainy=0.6
#
# Rows sum to 1: 0.8+0.2=1, 0.4+0.6=1  ✓

TRANS_MATRIX = [[0.8, 0.2],
                [0.4, 0.6]]

# ── Steady state derivation ────────────────────────────────────────────
# πP = π  ⟹  [π₀, π₁] [[0.8, 0.2], [0.4, 0.6]] = [π₀, π₁]
#
# Column 0:  π₀·0.8 + π₁·0.4 = π₀   →  −0.2π₀ + 0.4π₁ = 0  →  π₀ = 2π₁
# Column 1:  π₀·0.2 + π₁·0.6 = π₁   →   0.2π₀ − 0.4π₁ = 0  →  (same)
# Normalization: π₀ + π₁ = 1
#   → 2π₁ + π₁ = 1  →  π₁ = 1/3,  π₀ = 2/3
#
# π = [2/3, 1/3] ≈ [0.66667, 0.33333]

STEADY_STATE = [2 / 3, 1 / 3]

# ── Multi-step transition: P² ──────────────────────────────────────────
# P² = P × P
# P²[0][0] = 0.8·0.8 + 0.2·0.4 = 0.64 + 0.08 = 0.72
# P²[0][1] = 0.8·0.2 + 0.2·0.6 = 0.16 + 0.12 = 0.28
# P²[1][0] = 0.4·0.8 + 0.6·0.4 = 0.32 + 0.24 = 0.56
# P²[1][1] = 0.4·0.2 + 0.6·0.6 = 0.08 + 0.36 = 0.44

P_SQUARED = [[0.72, 0.28],
             [0.56, 0.44]]

# ── Prior errors catalogue ─────────────────────────────────────────────
PRIOR_ERRORS = {
    "steady_wrong_direction":
        "Solves Pπ = π (right eigenvector, column convention) instead of "
        "πP = π (left eigenvector, row convention); for non-symmetric P "
        "these give different results",
    "rows_not_summing":
        "Constructs transition matrix whose columns sum to 1 instead of "
        "rows, effectively transposing the stochastic matrix",
    "forgets_normalization":
        "Finds the eigenvector direction but does not normalize so that "
        "Σπᵢ = 1; the result is not a valid probability distribution",
}
