"""Gini Coefficient — Frozen Constants. Source: Sen (1997) On Economic Inequality, Cowell (2011) Measuring Inequality. DO NOT MODIFY."""

# ── Core Formula ──────────────────────────────────────────────
# Gini = A / (A + B) where:
#   A = area between perfect equality line (diagonal) and Lorenz curve
#   A + B = 0.5 (total area under the diagonal)
# So: Gini = 2A = 1 - 2B, where B = area under Lorenz curve
#
# Alternative (mean absolute difference):
#   G = Σᵢ Σⱼ |xᵢ - xⱼ| / (2 * n² * μ)
#
# Range: 0 (perfect equality) to 1 (perfect inequality)

# ── Lorenz Curve ──────────────────────────────────────────────
# Plot cumulative population share (X) vs cumulative income share (Y)
# KEY: Data must be SORTED ASCENDING before computing cumulative shares
# LLM prior: does not sort incomes → wrong Lorenz curve
#
# Trapezoid formula for Gini:
#   G = 1 - Σᵢ (Xᵢ - Xᵢ₋₁)(Yᵢ + Yᵢ₋₁)
# where X = cumulative population share, Y = cumulative income share

# ── Test Vector ───────────────────────────────────────────────
INCOMES = [10, 20, 30, 40, 100]
INCOMES_SORTED = [10, 20, 30, 40, 100]
INCOMES_UNSORTED = [40, 10, 100, 30, 20]

TOTAL = 200
N = 5

# Cumulative population shares (including origin)
CUM_POP_SHARES = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

# Cumulative income shares (including origin): [0, 10/200, 30/200, 60/200, 100/200, 200/200]
CUM_INCOME_SHARES = [0.0, 0.05, 0.15, 0.30, 0.50, 1.00]

# B (area under Lorenz) via trapezoid:
# B = Σ (Xᵢ - Xᵢ₋₁) * (Yᵢ + Yᵢ₋₁) / 2
#   = 0.1*(0 + 0.05) + 0.1*(0.05 + 0.15) + 0.1*(0.15 + 0.30) + 0.1*(0.30 + 0.50) + 0.1*(0.50 + 1.00)
#   = 0.005 + 0.02 + 0.045 + 0.08 + 0.15
#   = 0.30
LORENZ_AREA_B = 0.30

# Gini = 1 - 2 * B = 1 - 2 * 0.30 = 0.40
GINI_TEST = 0.40

# ── Perfect Equality ─────────────────────────────────────────
EQUAL_INCOMES = [50, 50, 50, 50, 50]
# Lorenz curve = diagonal → B = 0.5 → Gini = 0.0
GINI_EQUAL = 0.0

# ── Extreme Inequality ───────────────────────────────────────
EXTREME_INCOMES = [0, 0, 0, 0, 100]
# Cumulative income: [0, 0, 0, 0, 0, 1.0]
# B = 0.1*(0+0) + 0.1*(0+0) + 0.1*(0+0) + 0.1*(0+0) + 0.1*(0+1.0) = 0.1
# Gini = 1 - 2*0.1 = 0.8
GINI_EXTREME = 0.80

# ── Prior Error Catalog ──────────────────────────────────────
PRIOR_ERRORS = {
    "unsorted_data":        "Does not sort incomes before computing Lorenz curve",
    "lorenz_no_cumulative": "Uses raw income shares instead of cumulative income shares",
    "gini_range_wrong":     "Claims Gini coefficient can exceed 1",
}
