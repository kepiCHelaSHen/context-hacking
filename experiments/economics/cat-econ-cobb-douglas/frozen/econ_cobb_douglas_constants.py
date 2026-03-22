"""
Cobb-Douglas Production Function — Frozen Constants
Source: Cobb & Douglas (1928), Solow (1956), Varian Microeconomic Analysis 3rd Ed Ch18
DO NOT MODIFY.
"""

# General Cobb-Douglas: Y = A * K^alpha * L^beta
# A = total factor productivity, K = capital, L = labor
# alpha = output elasticity of capital, beta = output elasticity of labor

# KEY: alpha + beta does NOT have to equal 1!
# alpha + beta > 1 => increasing returns to scale (IRS)
# alpha + beta = 1 => constant returns to scale (CRS)
# alpha + beta < 1 => decreasing returns to scale (DRS)

# --- Test parameters (IRS case: alpha + beta = 1.1) ---
A_TEST = 1
ALPHA_TEST = 0.4
BETA_TEST = 0.7
SUM_EXPONENTS = ALPHA_TEST + BETA_TEST  # 1.1 — increasing returns!

# Baseline inputs
K1 = 100
L1 = 200

# Y(100, 200) = 1 * 100^0.4 * 200^0.7
# 100^0.4 = 6.30957...
# 200^0.7 = 40.80604...
# Y = 6.30957 * 40.80604 = 257.474
Y1 = A_TEST * K1 ** ALPHA_TEST * L1 ** BETA_TEST  # ~257.47

# Double all inputs
K2 = 200
L2 = 400

# Y(200, 400) = 1 * 200^0.4 * 400^0.7
# 200^0.4 = 8.32586...
# 400^0.7 = 66.28899...
# Y = 8.32586 * 66.28899 = 551.893
Y2 = A_TEST * K2 ** ALPHA_TEST * L2 ** BETA_TEST  # ~551.89

# Output ratio when inputs doubled: 2^(alpha+beta) = 2^1.1 = 2.1435
DOUBLE_INPUT_RATIO = Y2 / Y1  # ~2.1435 > 2 => confirms IRS
THEORETICAL_RATIO = 2 ** SUM_EXPONENTS  # 2^1.1 = 2.1435

# --- CRS special case (alpha + beta = 1) ---
ALPHA_CRS = 0.3
BETA_CRS = 0.7  # alpha + beta = 1.0

# Factor shares under CRS: labor gets beta fraction, capital gets alpha fraction
# MPL * L / Y = beta, MPK * K / Y = alpha (Euler's theorem)
LABOR_SHARE_CRS = BETA_CRS   # 0.7
CAPITAL_SHARE_CRS = ALPHA_CRS  # 0.3

# --- Marginal products ---
# MPK = alpha * A * K^(alpha-1) * L^beta      (note: alpha-1, NOT alpha)
# MPL = beta  * A * K^alpha     * L^(beta-1)  (note: beta-1,  NOT beta)
MPK_TEST = ALPHA_TEST * A_TEST * K1 ** (ALPHA_TEST - 1) * L1 ** BETA_TEST  # ~1.0299
MPL_TEST = BETA_TEST * A_TEST * K1 ** ALPHA_TEST * L1 ** (BETA_TEST - 1)   # ~0.9011

PRIOR_ERRORS = {
    "exponents_sum_1":   "Claims alpha+beta must equal 1 (only true for CRS, not in general)",
    "mpk_wrong_exponent": "Uses K^alpha instead of K^(alpha-1) in marginal product of capital",
    "irs_impossible":    "Claims increasing returns to scale is impossible in Cobb-Douglas",
}
