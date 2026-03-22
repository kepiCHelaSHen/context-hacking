"""
Present Value (NPV, IRR, Annuities) -- Frozen Constants
Source: Standard financial mathematics (Brealey, Myers & Allen; Hull)
DO NOT MODIFY.
"""
import math

# --- Test case: FV=1000, r=0.10, n=5 ---
TEST_FV           = 1000.0
TEST_RATE         = 0.10
TEST_N            = 5

# Discrete compounding: PV = FV / (1+r)^n
DISCRETE_FACTOR   = (1 + TEST_RATE) ** TEST_N          # 1.61051
DISCRETE_PV       = TEST_FV / DISCRETE_FACTOR          # 620.921...

# Continuous compounding: PV = FV * e^(-rn)
CONTINUOUS_FACTOR = math.exp(-TEST_RATE * TEST_N)       # e^(-0.5) = 0.60653...
CONTINUOUS_PV     = TEST_FV * CONTINUOUS_FACTOR          # 606.531...

# The difference proves they are NOT interchangeable
PV_DIFFERENCE     = DISCRETE_PV - CONTINUOUS_PV          # ~14.39

# --- Annuity test: PMT=100, r=0.10, n=5 ---
TEST_PMT          = 100.0
ANNUITY_FACTOR    = (1 - (1 + TEST_RATE) ** (-TEST_N)) / TEST_RATE  # 3.79079...
ANNUITY_PV        = TEST_PMT * ANNUITY_FACTOR            # 379.079...

# --- Perpetuity: PMT=100, r=0.10 ---
PERPETUITY_PV     = TEST_PMT / TEST_RATE                  # 1000.0

# --- NPV test: initial outlay -500, then 5 years of 150 at r=0.10 ---
TEST_CASHFLOWS    = [-500.0, 150.0, 150.0, 150.0, 150.0, 150.0]
NPV_EXPECTED      = sum(cf / (1 + TEST_RATE) ** t for t, cf in enumerate(TEST_CASHFLOWS))
# = -500 + 150/1.1 + 150/1.21 + 150/1.331 + 150/1.4641 + 150/1.61051
# = -500 + 136.364 + 123.967 + 112.697 + 102.452 + 93.138
# = 68.618...

PRIOR_ERRORS = {
    "continuous_discrete_swap": "uses e^(-rn) when discrete (1+r)^n is required, or vice versa",
    "annuity_perpetuity":       "uses PMT/r (perpetuity formula) for a finite n-period annuity",
    "npv_no_initial":           "computes sum of discounted CFs but forgets to subtract initial cost C0",
}
