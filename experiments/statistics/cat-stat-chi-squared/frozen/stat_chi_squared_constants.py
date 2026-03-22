"""Chi-Squared Test — Frozen Constants. Source: Pearson 1900 / NIST. DO NOT MODIFY."""
import math

# === Goodness-of-Fit Test ===
# df = k - 1 (k = number of categories)
# Test scenario: die fairness test, 6 categories, n=60
GOF_OBSERVED = [8, 12, 10, 14, 8, 8]
GOF_EXPECTED = [10, 10, 10, 10, 10, 10]
GOF_K = 6
GOF_DF = GOF_K - 1  # = 5
# chi2 = (8-10)^2/10 + (12-10)^2/10 + (10-10)^2/10 + (14-10)^2/10 + (8-10)^2/10 + (8-10)^2/10
#       = 4/10 + 4/10 + 0/10 + 16/10 + 4/10 + 4/10 = 32/10 = 3.2
GOF_CHI2 = sum((o - e) ** 2 / e for o, e in zip(GOF_OBSERVED, GOF_EXPECTED))  # = 3.2

# === Independence Test (Contingency Table) ===
# df = (r-1)(c-1), NOT r*c-1, NOT (r-1)+(c-1)
# Test scenario: 2x3 contingency table
IND_TABLE = [[10, 20, 30],
             [20, 15, 25]]
IND_ROWS = 2
IND_COLS = 3
IND_DF = (IND_ROWS - 1) * (IND_COLS - 1)  # = 2 (NOT 5, NOT 3)
# Row totals: [60, 60], Col totals: [30, 35, 55], Grand total: 120
IND_ROW_TOTALS = [sum(row) for row in IND_TABLE]                  # [60, 60]
IND_COL_TOTALS = [sum(IND_TABLE[i][j] for i in range(IND_ROWS))
                  for j in range(IND_COLS)]                        # [30, 35, 55]
IND_GRAND_TOTAL = sum(IND_ROW_TOTALS)                              # 120
# Expected = row_total * col_total / grand
IND_EXPECTED = [[IND_ROW_TOTALS[i] * IND_COL_TOTALS[j] / IND_GRAND_TOTAL
                 for j in range(IND_COLS)]
                for i in range(IND_ROWS)]  # [[15, 17.5, 27.5], [15, 17.5, 27.5]]
IND_CHI2 = sum((IND_TABLE[i][j] - IND_EXPECTED[i][j]) ** 2 / IND_EXPECTED[i][j]
               for i in range(IND_ROWS) for j in range(IND_COLS))  # ≈ 4.5022

# Wrong-df values that LLMs frequently produce
WRONG_DF_RC_MINUS_1 = IND_ROWS * IND_COLS - 1  # = 5 (WRONG)
WRONG_DF_SUM = (IND_ROWS - 1) + (IND_COLS - 1)  # = 3 (WRONG)

PRIOR_ERRORS = {
    "df_rc_minus_1":        "Uses r*c-1 instead of (r-1)(c-1) for contingency df",
    "df_sum_not_product":   "Uses (r-1)+(c-1) instead of (r-1)*(c-1) for contingency df",
    "no_expected_freq_check": "Doesn't verify expected frequencies >= 5 for validity",
}
