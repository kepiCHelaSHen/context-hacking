"""Mann-Whitney U Test — Frozen Constants. Source: Mann & Whitney 1947. DO NOT MODIFY."""
import math
# U₁ = n₁n₂ + n₁(n₁+1)/2 - R₁   where R₁ = sum of ranks of group 1
# U₂ = n₁n₂ - U₁                  (equivalently: n₁n₂ + n₂(n₂+1)/2 - R₂)
# U  = min(U₁, U₂) is the test statistic
# KEY identity: U₁ + U₂ = n₁·n₂ always
# For large samples: z = (U - n₁n₂/2) / √(n₁n₂(n₁+n₂+1)/12)

# Test data
GROUP_A = [3, 5, 7, 9]
GROUP_B = [1, 2, 4, 6, 8]
# Combined sorted: [1,2,3,4,5,6,7,8,9]  ranks: [1,2,3,4,5,6,7,8,9]
# Group A ranks: 3→3, 5→5, 7→7, 9→9  → R₁ = 24
# Group B ranks: 1→1, 2→2, 4→4, 6→6, 8→8  → R₂ = 21
N1 = len(GROUP_A)   # 4
N2 = len(GROUP_B)   # 5
R1 = 24
R2 = 21
U1 = N1 * N2 + N1 * (N1 + 1) // 2 - R1   # 20 + 10 - 24 = 6
U2 = N1 * N2 - U1                          # 20 - 6 = 14
U_STAT = min(U1, U2)                       # 6
assert U1 + U2 == N1 * N2, "identity violated"
PRIOR_ERRORS = {
    "u_formula_wrong": "Uses R1 - n1(n1+1)/2 without the n1*n2 term",
    "u_not_min":       "Reports U1 or U2 instead of min(U1, U2)",
    "ranks_from_1":    "Starts ranking from 0 instead of 1",
}
