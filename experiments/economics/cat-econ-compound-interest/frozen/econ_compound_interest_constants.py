"""
Compound Interest — APR vs EAR — Frozen Constants
Source: Brealey Myers Allen Principles of Corporate Finance,
        Mishkin Economics of Money Banking & Financial Markets
DO NOT MODIFY.
"""
import math

# ── Test case: APR = 12%, monthly compounding (m = 12) ──────────────
APR = 0.12              # nominal annual percentage rate (stated rate)
M   = 12                # compounding periods per year (monthly)

# EAR = (1 + APR/m)^m - 1
# EAR = (1 + 0.12/12)^12 - 1 = (1.01)^12 - 1
# (1.01)^12 = 1.126825030131969...
# EAR = 0.126825030131969... ≈ 12.683%
EAR_EXPECTED = (1 + APR / M) ** M - 1     # 0.12682503013196972

# Continuous compounding: EAR = e^APR - 1
# e^0.12 = 1.12749685157...
# EAR_continuous = 0.12749685157... ≈ 12.750%
EAR_CONTINUOUS_EXPECTED = math.exp(APR) - 1  # 0.12749685157...

# ── Common wrong answer: treating APR as EAR ────────────────────────
# If you simply use 0.12 as EAR, you underestimate by 0.683 pp
EAR_WRONG_APR_AS_EAR = APR                   # 0.12 (WRONG)

# ── Compound amount: P * (1 + APR/m)^(m*t) ─────────────────────────
# Test: P=1000, APR=12%, monthly, 5 years
P_PRINCIPAL = 1000.0
T_YEARS     = 5
# FV = 1000 * (1 + 0.01)^60 = 1000 * 1.8166966986... = 1816.6967...
COMPOUND_AMOUNT_EXPECTED = P_PRINCIPAL * (1 + APR / M) ** (M * T_YEARS)
# 1816.6966986...

# ── Rule of 72 ──────────────────────────────────────────────────────
# Approximate doubling time ≈ 72 / r  (r in percent)
RATE_PCT = 12.0                       # 12 percent
RULE_72_APPROX = 72.0 / RATE_PCT     # 6.0 years

# Exact doubling time = ln(2) / ln(1 + r)
# ln(2) / ln(1.12) = 0.693147... / 0.113329... = 6.11625...
EXACT_DOUBLING_TIME = math.log(2) / math.log(1 + APR)  # 6.11625...

# ── PRIOR_ERRORS: known LLM mistakes ────────────────────────────────
PRIOR_ERRORS = {
    "apr_equals_ear":    "Treats APR as EAR (uses 12% instead of 12.683%)",
    "rule72_exact":      "Treats Rule of 72 as exact formula (6.0 years instead of 6.116)",
    "continuous_wrong":  "Uses e^r - 1 for discrete compounding instead of (1+r/m)^m - 1",
}
