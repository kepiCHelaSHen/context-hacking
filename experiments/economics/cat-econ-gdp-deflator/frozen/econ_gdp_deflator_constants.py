"""GDP Deflator — Frozen Constants. Source: Mankiw Macroeconomics 10th Ed Ch 2, BEA methodology. DO NOT MODIFY."""

# Nominal GDP: Σ Pᵢ_current × Qᵢ_current  (current prices × current quantities)
# Real GDP:    Σ Pᵢ_base × Qᵢ_current       (BASE YEAR prices × current quantities)
# GDP Deflator = (Nominal GDP / Real GDP) × 100
# KEY: Real GDP uses BASE YEAR prices, not current prices
# In base year: deflator = 100 (by definition, nominal = real)
# Inflation rate from deflator: (deflator_t − deflator_{t−1}) / deflator_{t−1} × 100
# LLM prior: uses current prices for real GDP (wrong base year handling)

# --- Test Economy: Two goods (A, B) ---
# Base year (year 0): P_A=2, Q_A=100, P_B=5, Q_B=50
BASE_PRICES  = [2, 5]
BASE_QUANTS  = [100, 50]

# Year 1: P_A=3, Q_A=110, P_B=6, Q_B=55
YEAR1_PRICES = [3, 6]
YEAR1_QUANTS = [110, 55]

# Year 0 calculations
NOMINAL_Y0 = 2*100 + 5*50          # = 450
REAL_Y0    = 2*100 + 5*50          # = 450 (base year: same prices)
DEFLATOR_Y0 = (NOMINAL_Y0 / REAL_Y0) * 100  # = 100.0

# Year 1 calculations
NOMINAL_Y1 = 3*110 + 6*55          # = 330 + 330 = 660
REAL_Y1    = 2*110 + 5*55          # = 220 + 275 = 495
DEFLATOR_Y1 = (NOMINAL_Y1 / REAL_Y1) * 100  # = 133.333...

# Inflation rate year 0 → year 1
INFLATION_01 = (DEFLATOR_Y1 - DEFLATOR_Y0) / DEFLATOR_Y0 * 100  # = 33.333...%

PRIOR_ERRORS = {
    "real_current_prices": "Uses current prices for real GDP (should use BASE YEAR prices)",
    "deflator_inverted":   "Uses Real/Nominal instead of Nominal/Real",
    "base_year_not_100":   "Deflator ≠ 100 in base year (must equal 100 by definition)",
}
