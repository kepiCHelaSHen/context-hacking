"""Leslie Matrix — Stable Age Distribution — Frozen Constants. Source: Leslie 1945. DO NOT MODIFY."""
import math

# Leslie matrix L: first row = fecundity (F_i), sub-diagonal = survival (S_i)
# n(t+1) = L × n(t)
# Dominant eigenvalue λ₁ = asymptotic growth rate
#   λ > 1: growing population
#   λ < 1: declining population
#   λ = 1: stable population
# Stable age distribution: proportional to dominant eigenvector

# Test case: 3 age classes
#   F1=0 (juveniles don't reproduce), F2=2, F3=1
#   S1=0.5 (juvenile survival), S2=0.8 (adult survival)
#
#   L = [[0,   2,   1  ],
#        [0.5, 0,   0  ],
#        [0,   0.8, 0  ]]
#
#   Characteristic equation: det(L - λI) = 0
#     -λ³ + 2*0.5*λ + 1*0.5*0.8 = 0
#     -λ³ + λ + 0.4 = 0
#     λ³ - λ - 0.4 = 0
#
#   Dominant eigenvalue λ₁ ≈ 1.15970 (growing population)
#   r = ln(λ₁) ≈ 0.14817 (intrinsic rate of increase)
#   NOTE: λ ≠ r.  λ is the finite growth rate; r is the Malthusian parameter.

LESLIE_MATRIX = [
    [0.0, 2.0, 1.0],
    [0.5, 0.0, 0.0],
    [0.0, 0.8, 0.0],
]

FECUNDITY = [0.0, 2.0, 1.0]       # first row of L
SURVIVAL  = [0.5, 0.8]             # sub-diagonal of L

N0 = [100.0, 50.0, 30.0]          # initial population vector

# One-step projection: L × n0
N1_EXPECTED = [130.0, 50.0, 40.0]  # [0*100+2*50+1*30, 0.5*100, 0.8*50]

# Dominant eigenvalue (verified numerically: λ³ - λ - 0.4 = 0)
LAMBDA_DOMINANT = 1.1597048528     # asymptotic growth rate
R_INTRINSIC = math.log(LAMBDA_DOMINANT)  # ≈ 0.14817

# Verify: λ ≠ r — they are fundamentally different quantities
assert not math.isclose(LAMBDA_DOMINANT, R_INTRINSIC, rel_tol=0.01), \
    "λ and r must differ; confusing them is a common LLM error"

# Verify: λ satisfies characteristic equation
assert math.isclose(LAMBDA_DOMINANT**3 - LAMBDA_DOMINANT - 0.4, 0.0, abs_tol=1e-6), \
    "Dominant eigenvalue must satisfy λ³ - λ - 0.4 = 0"

# Verify: one-step projection
_n1 = [
    sum(LESLIE_MATRIX[i][j] * N0[j] for j in range(3))
    for i in range(3)
]
for i in range(3):
    assert math.isclose(_n1[i], N1_EXPECTED[i], rel_tol=1e-9), \
        f"One-step projection mismatch at age class {i}"

# Leslie structure: fecundity in FIRST ROW, survival on SUB-DIAGONAL
# WRONG: putting survival in the first row or fecundity on the diagonal
assert all(LESLIE_MATRIX[0][j] == FECUNDITY[j] for j in range(3)), \
    "First row must be fecundity"
assert LESLIE_MATRIX[1][0] == SURVIVAL[0] and LESLIE_MATRIX[2][1] == SURVIVAL[1], \
    "Sub-diagonal must be survival probabilities"

PRIOR_ERRORS = {
    "lambda_is_r":            "Confuses λ (finite growth rate) with r=ln(λ) (intrinsic rate)",
    "eigenvector_is_growth":  "Confuses eigenvalue (growth rate) with eigenvector (age structure)",
    "leslie_wrong_structure": "Puts survival in wrong position (must be sub-diagonal, not first row)",
}
