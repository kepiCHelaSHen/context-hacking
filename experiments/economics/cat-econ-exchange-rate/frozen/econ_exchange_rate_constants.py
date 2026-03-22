"""
Exchange Rate Determination — Frozen Constants
PPP and Interest Rate Parity reference values.
Source: IMF IFS, OECD PPP dataset, standard international finance textbooks.
DO NOT MODIFY.
"""

# --- PPP Test Case ---
P_US                = 120       # US price level (index)
P_UK                = 100       # UK price level (index)
PPP_RATE_USD_PER_GBP = 1.20    # = P_US / P_UK = 120/100

# --- Relative PPP Test Case ---
INFLATION_US        = 0.03      # 3% US inflation
INFLATION_UK        = 0.01      # 1% UK inflation
EXPECTED_PCT_CHANGE = 0.02      # π_dom - π_for = 3% - 1% = 2% ($ depreciates)
EXPECTED_NEXT_E     = 1.224     # 1.20 * (1 + 0.02) = 1.224 $/£

# --- Interest Rate Parity Test Case ---
I_US                = 0.05      # 5% US interest rate
I_UK                = 0.03      # 3% UK interest rate
# IRP expected change: (1+i_d)/(1+i_f) - 1 = 1.05/1.03 - 1 ≈ 0.019417
IRP_EXPECTED_CHANGE = 0.019417  # expected depreciation of domestic currency

# --- Real Exchange Rate Test Case ---
# q = E * P_f / P_d (E in domestic/foreign units, i.e. $/£)
# q = 1.20 * 100 / 120 = 1.0 (PPP holds => real rate = 1)
REAL_EXCHANGE_RATE_PPP = 1.0

PRIOR_ERRORS = {
    "appreciation_wrong_direction": "higher inflation -> appreciation (should be depreciation)",
    "ppp_inverted":                 "uses P_foreign/P_domestic instead of P_domestic/P_foreign",
    "irp_same_direction":           "higher interest -> appreciation instead of expected depreciation",
}
