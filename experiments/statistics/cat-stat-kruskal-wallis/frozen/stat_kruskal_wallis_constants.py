"""Kruskal-Wallis Test — Frozen Constants. Source: Kruskal & Wallis 1952. DO NOT MODIFY."""
import math

# === Kruskal-Wallis H Test (Non-parametric one-way ANOVA) ===
# H = (12 / (N(N+1))) * Σ(Rᵢ² / nᵢ) - 3(N+1)
# where Rᵢ = sum of ranks in group i, nᵢ = group size, N = total observations
#
# Tie correction: H_corrected = H / (1 - Σ(t³ - t) / (N³ - N))
# where t = number of tied values in each tie group
#
# Under H₀: H ~ χ²(k-1) approximately

# === Test data: 3 groups, no ties ===
GROUP_A = [4, 5, 6]
GROUP_B = [1, 2, 3]
GROUP_C = [7, 8, 9]
GROUPS = [GROUP_A, GROUP_B, GROUP_C]
K = 3                       # number of groups
N = 9                       # total observations

# Combined sorted: 1,2,3,4,5,6,7,8,9 → ranks are values themselves
# B=[1,2,3] → ranks 1,2,3 → R_B = 6
# A=[4,5,6] → ranks 4,5,6 → R_A = 15
# C=[7,8,9] → ranks 7,8,9 → R_C = 24
R_A = 15
R_B = 6
R_C = 24
RANK_SUMS = [R_A, R_B, R_C]

# H = (12 / (9 * 10)) * (15²/3 + 6²/3 + 24²/3) - 3 * 10
#   = (12 / 90) * (75 + 12 + 192) - 30
#   = (12 / 90) * 279 - 30
#   = 37.2 - 30 = 7.2
H_STAT = (12 / (N * (N + 1))) * sum(r ** 2 / n for r, n in
          zip(RANK_SUMS, [len(g) for g in GROUPS])) - 3 * (N + 1)  # = 7.2

DF = K - 1  # = 2

# === Tie example ===
# If two observations are tied at value 5 → one tie group of size t=2
TIE_EXAMPLE_T = 2
# correction = 1 - Σ(t³ - t) / (N³ - N) = 1 - (8 - 2)/(729 - 9) = 1 - 6/720
TIE_CORRECTION = 1 - (TIE_EXAMPLE_T ** 3 - TIE_EXAMPLE_T) / (N ** 3 - N)  # ≈ 0.99167
# H_corrected = H / TIE_CORRECTION (slightly larger than H when ties exist)
# Without tie correction: H is used directly → underestimates significance

# === Prior LLM errors ===
PRIOR_ERRORS = {
    "no_tie_correction":  "Ignores tie correction entirely — uses raw H even with tied ranks",
    "wrong_tie_formula":  "Uses t²-t instead of t³-t in tie correction denominator",
    "df_wrong":           "Uses k or N-1 instead of k-1 for degrees of freedom",
}
