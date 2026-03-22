"""Digital Logic — Frozen Constants. Source: Mano & Ciletti 6th Ed. DO NOT MODIFY."""
# De Morgan's Laws (correct forms):
# NOT(A AND B) = (NOT A) OR (NOT B)   ← NAND decomposition
# NOT(A OR B)  = (NOT A) AND (NOT B)  ← NOR decomposition
# LLM prior: applies wrong operator — writes NOT(A AND B) = NOT(A) AND NOT(B)

# SOP (Sum of Products): canonical form — OR of ANDed minterms
# POS (Product of Sums): dual form — AND of ORed maxterms
# LLM prior: confuses SOP with POS

# Karnaugh map: group adjacent 1-cells in powers of 2
# Don't-cares (X) can be treated as 1 OR 0, chosen to MAXIMIZE grouping
# LLM prior: treats don't-cares as mandatory 1s (forces them into the ON-set)

# Test function: F(A,B,C) = Σm(1,3,5,7)
# Truth table (A B C | F):
#  0 0 0 | 0    m0
#  0 0 1 | 1    m1  ← B=0? No, B is middle var. Let's index: A=MSB, B=mid, C=LSB
#  0 1 0 | 0    m2
#  0 1 1 | 1    m3
#  1 0 0 | 0    m4
#  1 0 1 | 1    m5
#  1 1 0 | 0    m6
#  1 1 1 | 1    m7
# Minterms 1,3,5,7 → all rows where C=1 → F simplifies to C
VARIABLES = ["A", "B", "C"]
N_VARS = 3
MINTERMS = (1, 3, 5, 7)
# Full truth table: input tuples → output
TRUTH_TABLE = {
    (0, 0, 0): 0,
    (0, 0, 1): 1,
    (0, 1, 0): 0,
    (0, 1, 1): 1,
    (1, 0, 0): 0,
    (1, 0, 1): 1,
    (1, 1, 0): 0,
    (1, 1, 1): 1,
}
SIMPLIFIED = "C"  # F = C (variable index 2, the LSB)

# De Morgan verification: NOT(A AND B) for A=1, B=0
# Correct: NOT(1 AND 0) = NOT(0) = 1
# Wrong:   NOT(1) AND NOT(0) = 0 AND 1 = 0  ← INCORRECT
DEMORGAN_NAND_TEST = {"a": True, "b": False, "correct": True, "wrong": False}
DEMORGAN_NOR_TEST = {"a": True, "b": False, "correct": False, "wrong": False}
# NOT(A OR B) for A=1, B=0: NOT(1 OR 0) = NOT(1) = False
# Correct: NOT(1) AND NOT(0) = False AND True = False (matches)

PRIOR_ERRORS = {
    "demorgan_wrong":  "NOT(A AND B) = NOT(A) AND NOT(B) — uses AND instead of OR",
    "dont_care_forced": "Treats don't-cares as mandatory 1s instead of optional",
    "sop_vs_pos":       "Confuses Sum-of-Products with Product-of-Sums form",
}
