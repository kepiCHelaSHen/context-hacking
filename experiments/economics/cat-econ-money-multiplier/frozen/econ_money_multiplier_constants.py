"""Money Multiplier — Frozen Constants. Source: Mishkin Money & Banking 13th Ed Ch 14, Mankiw Macro 10th Ed Ch 18. DO NOT MODIFY."""

# ── Core Formula ──────────────────────────────────────────────
# Simple money multiplier: m = 1 / rr
# where rr = required reserve ratio (fraction of deposits held as reserves)
# LLM prior: uses 1/(1-rr) — confuses money multiplier with fiscal multiplier

# ── Extended Formula (with currency drain) ────────────────────
# m = (1 + cr) / (rr + cr)
# where cr = currency/deposit ratio (fraction public holds as cash)
# LLM prior: ignores currency drain, uses simple 1/rr even when cr given

# ── Deposit Expansion (Geometric Series) ─────────────────────
# Each deposit: bank keeps rr fraction, lends out (1-rr)
# That loan gets redeposited → process repeats
# Total deposits = D₀ * (1 + (1-rr) + (1-rr)² + ...) = D₀ / rr
# Total reserves = Total deposits * rr = D₀ (initial deposit)
# LLM prior: assumes banks lend 100% (rr=0), infinite multiplier

# ── Money Supply Identity ─────────────────────────────────────
# M = m × MB   (money supply = multiplier × monetary base)

# ── Test Vector: rr = 0.10 (10% reserve requirement) ─────────
RR = 0.10
SIMPLE_MULTIPLIER = 1.0 / RR                            # 10.0
WRONG_MULTIPLIER = 1.0 / (1.0 - RR)                     # 1.1111... (WRONG!)

# With currency drain cr = 0.05
CR = 0.05
EXTENDED_MULTIPLIER = (1.0 + CR) / (RR + CR)            # 1.05 / 0.15 = 7.0

# Deposit expansion from $1000 initial deposit
INITIAL_DEPOSIT = 1000.0
TOTAL_DEPOSITS = INITIAL_DEPOSIT / RR                    # 10000.0
TOTAL_RESERVES = TOTAL_DEPOSITS * RR                     # 1000.0 (equals initial deposit)

# Money supply: MB = $5000
MB = 5000.0
MONEY_SUPPLY_SIMPLE = MB * SIMPLE_MULTIPLIER             # 50000.0
MONEY_SUPPLY_EXTENDED = MB * EXTENDED_MULTIPLIER         # 35000.0

# ── Exact Rational Values ────────────────────────────────────
# Simple: 1/0.10 = 10  (exact integer)
# Extended: 1.05/0.15 = 105/15 = 7  (exact integer)
EXTENDED_EXACT_NUMER = 7
EXTENDED_EXACT_DENOM = 1

PRIOR_ERRORS = {
    "multiplier_1_minus_rr": "Uses 1/(1-rr) instead of 1/rr — confuses money multiplier with fiscal multiplier",
    "no_currency_drain":     "Ignores currency/deposit ratio (cr) in extended model, always uses simple 1/rr",
    "reserves_lent_fully":   "Assumes banks lend 100% of deposits (rr=0), yielding infinite multiplier",
}
