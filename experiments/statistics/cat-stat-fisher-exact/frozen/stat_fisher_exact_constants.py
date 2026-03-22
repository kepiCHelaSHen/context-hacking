"""Fisher's Exact Test — Frozen Constants. Source: Fisher 1922. DO NOT MODIFY."""
import math

# === Lady Tasting Tea (Fisher's original example, simplified) ===
# 2x2 table: [[a, b], [c, d]]
TABLE = [[3, 1],
         [1, 3]]

# Margins
R1 = 4          # a + b (row 1 total)
R2 = 4          # c + d (row 2 total)
C1 = 4          # a + c (col 1 total)
C2 = 4          # b + d (col 2 total)
N  = 8          # grand total

# Central binomial coefficient C(8,4)
C_8_4 = math.comb(8, 4)  # = 70

# === Hypergeometric probability for observed cell ===
# P(a) = C(R1,a) * C(R2, C1-a) / C(N, C1)
#       = (R1! R2! C1! C2!) / (N! a! b! c! d!)
# For a=3: C(4,3)*C(4,1)/C(8,4) = 4*4/70 = 16/70
P_EXACT = 16 / 70   # P(a=3) = 0.22857142857142856

# === One-tailed p-value (direction="greater", P(a >= 3)) ===
# P(a=3) + P(a=4) = 16/70 + 1/70 = 17/70
# P(a=4) = C(4,4)*C(4,0)/C(8,4) = 1/70
P_ONE_TAIL = 17 / 70  # 0.24285714285714285

# === Two-tailed p-value ===
# Sum all P(a) where P(a) <= P(observed = 3)
# Full distribution:
#   P(a=0) = C(4,0)*C(4,4)/70 =  1/70 = 0.01429  (<= 16/70, include)
#   P(a=1) = C(4,1)*C(4,3)/70 = 16/70 = 0.22857  (<= 16/70, include)
#   P(a=2) = C(4,2)*C(4,2)/70 = 36/70 = 0.51429  (> 16/70, exclude)
#   P(a=3) = C(4,3)*C(4,1)/70 = 16/70 = 0.22857  (<= 16/70, include)
#   P(a=4) = C(4,4)*C(4,0)/70 =  1/70 = 0.01429  (<= 16/70, include)
# Two-tailed = (1 + 16 + 16 + 1) / 70 = 34/70
P_TWO_TAIL = 34 / 70  # 0.4857142857142857

PRIOR_ERRORS = {
    "hypergeom_wrong":  "Wrong combinatorial formula for hypergeometric probability",
    "one_tail_only":    "Reports one-tailed p when two-tailed is needed",
    "chi_sq_instead":   "Uses chi-squared approximation for small expected counts (<5)",
}
