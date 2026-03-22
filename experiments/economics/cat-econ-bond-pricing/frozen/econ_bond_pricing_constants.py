"""
Bond Pricing (YTM, Duration, Convexity) — Frozen Constants
Source: Fabozzi Fixed Income Analysis 3rd Ed; Hull Options, Futures & Other Derivatives 11th Ed Ch4
DO NOT MODIFY.
"""

# Bond parameters
# FV = face (par) value, coupon_rate = annual coupon rate, ytm = annual yield to maturity
# years = time to maturity, m = coupon payments per year
# Most US bonds pay SEMI-ANNUALLY (m=2), not annually!

FACE_VALUE   = 1000
COUPON_RATE  = 0.06    # 6% annual coupon rate
YTM          = 0.08    # 8% annual yield to maturity
YEARS        = 5
M            = 2       # semi-annual (US convention)

# Derived quantities
COUPON_PER_PERIOD = FACE_VALUE * COUPON_RATE / M   # 30.0
NUM_PERIODS       = int(YEARS * M)                  # 10
YIELD_PER_PERIOD  = YTM / M                         # 0.04

# Bond price:  P = C * [(1 - (1+y)^(-n)) / y] + FV / (1+y)^n
#   where C = coupon per period, y = yield per period, n = total periods
# P = 30 * [(1 - 1.04^(-10)) / 0.04] + 1000 / 1.04^10
# P = 30 * 8.1109 + 1000 * 0.6756
# P = 243.3269 + 675.5642 = 918.8910
BOND_PRICE_SEMI = 918.8910   # correct (semi-annual)

# WRONG: annual coupon convention
# P = 60 * [(1 - 1.08^(-5)) / 0.08] + 1000 / 1.08^5
# P = 60 * 3.9927 + 680.5832 = 239.5626 + 680.5832 = 920.1458
BOND_PRICE_ANNUAL_WRONG = 920.1458

# WRONG: YTM not halved (uses 0.08 per semi-annual period instead of 0.04)
# P = 30 * [(1 - 1.08^(-10)) / 0.08] + 1000 / 1.08^10 = 664.4959
BOND_PRICE_YTM_WRONG = 664.4959

# Macaulay duration (semi-annual, in years)
# D = (1/P) * sum_{t=1..n} [ t * CF_t / (1+y)^t ] / m
# where CF_t = C for t < n, CF_n = C + FV
# D = (1/918.8910) * 8015.4091 / 2 = 4.3615 years
MACAULAY_DURATION_YEARS = 4.3615

# WRONG: duration without discounting cash flows
# Uses sum of t*CF_t (undiscounted) / P / m = 6.3392 years
MACAULAY_DURATION_NO_DISCOUNT_WRONG = 6.3392

# Current yield = annual coupon / market price
# CY = 60 / 918.8910 = 0.065296
CURRENT_YIELD = 0.065296

PRIOR_ERRORS = {
    "annual_not_semi":    "Uses annual coupons for US bonds (m=1) instead of semi-annual (m=2)",
    "ytm_not_halved":     "Uses full annual YTM per period instead of y/m for discounting",
    "duration_no_discount": "Forgets to discount cash flows in Macaulay duration formula",
}
