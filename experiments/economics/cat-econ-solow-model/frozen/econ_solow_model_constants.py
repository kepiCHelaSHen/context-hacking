"""
Solow Growth Model — Frozen Constants
Source: Solow (1956), "A Contribution to the Theory of Economic Growth", QJE 70(1).
        Mankiw, Macroeconomics 10th Ed Ch8-9; Romer, Advanced Macroeconomics 5th Ed Ch1.
DO NOT MODIFY.
"""

# Solow model in per-worker (intensive) form:
#   k_dot = s*f(k) - (n + delta)*k
# where k = K/L (capital per worker), s = savings rate,
# n = population growth rate, delta = depreciation rate
#
# With Cobb-Douglas f(k) = k^alpha:
#   k_dot = s*k^alpha - (n + delta)*k
#
# Steady state: s*k*^alpha = (n + delta)*k*
# Solving:  k* = (s / (n + delta))^(1/(1-alpha))
#
# KEY: denominator is (n + delta), NOT just delta!
# Population growth dilutes capital per worker just like depreciation does.
#
# Golden rule: maximise c* = f(k*) - (n+delta)*k*
#   => f'(k*) = n + delta  =>  MPK = n + delta
#   => alpha * k_gold^(alpha-1) = n + delta
#   => k_gold = (alpha / (n + delta))^(1/(1-alpha))

# --- Test parameters ---
S_TEST = 0.3        # savings rate
ALPHA_TEST = 1 / 3  # capital share (Cobb-Douglas exponent)
N_TEST = 0.02       # population growth rate
DELTA_TEST = 0.05   # depreciation rate

# Effective depreciation (break-even rate)
N_PLUS_DELTA = N_TEST + DELTA_TEST  # 0.07

# --- Steady-state capital per worker ---
# k* = (s / (n + delta))^(1/(1-alpha))
# k* = (0.3 / 0.07)^(1/(2/3)) = (4.28571...)^1.5
K_STAR = (S_TEST / N_PLUS_DELTA) ** (1 / (1 - ALPHA_TEST))  # ~8.8723

# --- Steady-state output per worker ---
# y* = k*^alpha
Y_STAR = K_STAR ** ALPHA_TEST  # ~2.0702

# --- Verify steady-state condition: s*f(k*) = (n+delta)*k* ---
ACTUAL_INV_STAR = S_TEST * K_STAR ** ALPHA_TEST        # s * k*^alpha
BREAK_EVEN_STAR = N_PLUS_DELTA * K_STAR                # (n+delta) * k*
assert abs(ACTUAL_INV_STAR - BREAK_EVEN_STAR) < 1e-9, "Steady-state condition violated"

# --- WRONG result: using only delta (common LLM error) ---
K_STAR_WRONG = (S_TEST / DELTA_TEST) ** (1 / (1 - ALPHA_TEST))  # ~14.6969
K_STAR_ERROR_PCT = (K_STAR_WRONG - K_STAR) / K_STAR * 100       # ~65.7% too high!

# --- Golden rule capital per worker ---
# MPK = n + delta  =>  k_gold = (alpha / (n+delta))^(1/(1-alpha))
K_GOLD = (ALPHA_TEST / N_PLUS_DELTA) ** (1 / (1 - ALPHA_TEST))  # ~10.3913
# Verify: MPK at golden rule = alpha * k_gold^(alpha-1) should equal n+delta
MPK_GOLD = ALPHA_TEST * K_GOLD ** (ALPHA_TEST - 1)
assert abs(MPK_GOLD - N_PLUS_DELTA) < 1e-9, "Golden rule MPK != n+delta"

# Golden rule savings rate (the s that makes k* = k_gold): s_gold = alpha*(n+delta)*k_gold / k_gold^alpha
# Simplifies to s_gold = alpha (for Cobb-Douglas)
S_GOLD = ALPHA_TEST  # 1/3

# --- Additional test point: transition dynamics ---
# At k=4 (below steady state): k_dot > 0 (capital accumulating)
K_LOW = 4.0
KDOT_LOW = S_TEST * K_LOW ** ALPHA_TEST - N_PLUS_DELTA * K_LOW  # should be > 0
assert KDOT_LOW > 0, "Capital should be accumulating below steady state"

# At k=20 (above steady state): k_dot < 0 (capital decumulating)
K_HIGH = 20.0
KDOT_HIGH = S_TEST * K_HIGH ** ALPHA_TEST - N_PLUS_DELTA * K_HIGH  # should be < 0
assert KDOT_HIGH < 0, "Capital should be decumulating above steady state"

PRIOR_ERRORS = {
    "only_depreciation":    "Uses delta instead of (n+delta) in steady-state formula — ignores population growth dilution",
    "golden_rule_s":        "Sets s=alpha for golden rule instead of deriving MPK = n+delta condition",
    "steady_state_formula": "Wrong algebraic form for k* — e.g. (s/(n+delta))^(1/alpha) instead of ^(1/(1-alpha))",
}
