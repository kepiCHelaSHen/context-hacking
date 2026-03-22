"""
Rational Method & SCS Curve Number — Frozen Constants
Source: Chow et al. 1988 "Applied Hydrology"; USDA NRCS TR-55 (1986)
DO NOT MODIFY.
"""

# === Rational Method ===
# Q = C * i * A
# Q: peak runoff (m³/s when i in m/s and A in m²)
# C: runoff coefficient, dimensionless, range [0, 1]
#   C=0 → all precipitation infiltrates
#   C=1 → all precipitation runs off
# i: rainfall intensity (m/s for SI; in/hr for US customary)
# A: drainage area (m² for SI; acres for US customary)
#
# US customary: Q (ft³/s) = C * i (in/hr) * A (acres)
#   The 1.008 conversion factor is conventionally taken as 1.0.

# --- Runoff coefficient ranges by surface type ---
C_PAVEMENT_MIN  = 0.90
C_PAVEMENT_MAX  = 0.95
C_GRASS_MIN     = 0.10
C_GRASS_MAX     = 0.35
C_FOREST_MIN    = 0.05
C_FOREST_MAX    = 0.25
C_ROOFTOP_MIN   = 0.75
C_ROOFTOP_MAX   = 0.95
C_GRAVEL_MIN    = 0.35
C_GRAVEL_MAX    = 0.70

# KEY: C is ALWAYS in [0, 1]. It is dimensionless — NOT a flow rate.

# --- Reference calculation ---
# C=0.5, i=50 mm/hr = 1.38889e-5 m/s, A=10000 m²
REF_C           = 0.5
REF_I_MM_HR     = 50.0                         # mm/hr
REF_I_M_S       = REF_I_MM_HR / (1000 * 3600)  # 1.38889e-5 m/s
REF_A_M2        = 10000.0                       # 1 hectare
REF_Q_M3S       = REF_C * REF_I_M_S * REF_A_M2 # 0.069444 m³/s
REF_Q_LS        = REF_Q_M3S * 1000.0            # 69.444 L/s

# === SCS Curve Number Method ===
# S = (25400 / CN) - 254   [S in mm, CN dimensionless in (0, 100]]
# Runoff Q_mm = (P - 0.2*S)² / (P + 0.8*S)  when P > 0.2*S, else 0
# P: precipitation depth in mm
# S: potential maximum retention in mm
# CN: curve number, range (0, 100]

SCS_NUMERATOR   = 25400.0      # mm (= 1000 inches * 25.4 mm/in)
SCS_SUBTRAHEND  = 254.0        # mm (= 10 inches * 25.4 mm/in)
SCS_IA_COEFF    = 0.2          # initial abstraction ratio (Ia = 0.2*S)
SCS_DENOM_COEFF = 0.8          # denominator coefficient (P + 0.8*S)

# --- SCS Reference calculation ---
# CN=75: S = 25400/75 - 254 = 84.667 mm
# P=100 mm: Q = (100 - 0.2*84.667)² / (100 + 0.8*84.667)
#            = (100 - 16.933)² / (100 + 67.733)
#            = 83.067² / 167.733
#            = 6900.02 / 167.733 = 41.133 mm
REF_CN          = 75.0
REF_S_MM        = SCS_NUMERATOR / REF_CN - SCS_SUBTRAHEND  # 84.667 mm
REF_P_MM        = 100.0
_Ia             = SCS_IA_COEFF * REF_S_MM
REF_Q_SCS_MM    = (REF_P_MM - _Ia)**2 / (REF_P_MM + SCS_DENOM_COEFF * REF_S_MM)

PRIOR_ERRORS = {
    "c_gt_1":             "Uses C > 1 in rational method; C is dimensionless in [0,1], not a flow rate",
    "rational_units_wrong": "Mixes SI and US customary units (e.g., in/hr with m²) without conversion",
    "cn_formula_wrong":   "Wrong SCS curve number formula — e.g., omits the -254 term or swaps 0.2/0.8 coefficients",
}
