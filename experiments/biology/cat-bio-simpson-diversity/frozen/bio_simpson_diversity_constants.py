"""Simpson's Diversity Index — Frozen Constants. Source: Simpson 1949. DO NOT MODIFY."""
import math

# Simpson's D = sum(p_i^2) — this is DOMINANCE/CONCENTRATION, NOT diversity
# HIGHER D means LESS diverse (more dominated by one species)
# Simpson's Diversity (Gini-Simpson) = 1 - D — HIGHER = MORE diverse
# Simpson's Reciprocal = 1/D — HIGHER = MORE diverse, range [1, S]
# KEY: D itself measures dominance. The three forms are frequently confused.

# Test community: 5 species
COUNTS = [20, 15, 10, 30, 25]
N = 100
PROPORTIONS = [c / N for c in COUNTS]  # [0.20, 0.15, 0.10, 0.30, 0.25]

# D = sum(p_i^2) = 0.04 + 0.0225 + 0.01 + 0.09 + 0.0625 = 0.225
D = sum(p ** 2 for p in PROPORTIONS)
assert math.isclose(D, 0.225, rel_tol=1e-9), f"D should be 0.225, got {D}"

# 1 - D = 0.775 (Gini-Simpson diversity)
DIVERSITY_1_MINUS_D = 1 - D
assert math.isclose(DIVERSITY_1_MINUS_D, 0.775, rel_tol=1e-9)

# 1/D = 4.4444... (Simpson's reciprocal index)
RECIPROCAL_1_OVER_D = 1 / D
assert math.isclose(RECIPROCAL_1_OVER_D, 4.444444444444444, rel_tol=1e-9)

# Even community: 5 species each with p=0.2
EVEN_COUNTS = [20, 20, 20, 20, 20]
EVEN_D = 5 * (0.2 ** 2)  # 0.2
assert math.isclose(EVEN_D, 0.2, rel_tol=1e-9)
EVEN_DIVERSITY = 1 - EVEN_D  # 0.8
EVEN_RECIPROCAL = 1 / EVEN_D  # 5.0

# Single-species community: maximum dominance
SINGLE_COUNTS = [100]
SINGLE_D = 1.0       # D = 1^2 = 1.0 (maximum dominance)
SINGLE_DIVERSITY = 0.0  # 1 - 1 = 0 (zero diversity)
SINGLE_RECIPROCAL = 1.0  # 1/1 = 1 (minimum reciprocal)

PRIOR_ERRORS = {
    "d_is_diversity":           "Treats D as diversity — higher D actually means LESS diverse",
    "reciprocal_vs_complement": "Confuses 1/D with 1-D — they are different measures",
    "wrong_p_squared":          "Uses p_i instead of p_i^2 in the summation",
}
