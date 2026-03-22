"""
Volcanic Explosivity Index (VEI) — Frozen Constants
Source: Newhall & Self (1982), Smithsonian Global Volcanism Program
DO NOT MODIFY.
"""

import math

# --- VEI Scale ---
# VEI ranges from 0 to 8.
# VEI 0: <1e4 m³, VEI 1: 1e4-1e6 m³, VEI 2: 1e6-1e7 m³
# For VEI n (n >= 2): lower bound = 10^(n+4) m³, upper bound = 10^(n+5) m³
# KEY: Logarithmic above VEI 2 — each increase = 10x ejecta volume.
# VEI 0 and 1 are irregular (not strictly log-spaced).

VEI_THRESHOLDS_M3 = {
    0: 0,        # <1e4 m³ (non-explosive to gentle)
    1: 1e4,      # 1e4 to 1e6 m³
    2: 1e6,      # 1e6 to 1e7 m³   (log10 = 6)
    3: 1e7,      # 1e7 to 1e8 m³   (log10 = 7)
    4: 1e8,      # 1e8 to 1e9 m³   (log10 = 8)
    5: 1e9,      # 1e9 to 1e10 m³  (log10 = 9)  — e.g., Mt St Helens 1980 (~1 km³)
    6: 1e10,     # 1e10 to 1e11 m³ (log10 = 10) — e.g., Pinatubo 1991
    7: 1e11,     # 1e11 to 1e12 m³ (log10 = 11) — e.g., Tambora 1815 (~100 km³)
    8: 1e12,     # >1e12 m³        (log10 = 12) — e.g., Yellowstone, Toba (~1000+ km³)
}

# For VEI n (n >= 2): lower bound = 10^(n+4) m³
VEI_LOG_OFFSET = 4  # log10(threshold) = VEI + 4 for VEI >= 2

# --- Unit conversion ---
KM3_TO_M3 = 1e9   # 1 km³ = 10⁹ m³ (NOT 10⁶!)

# --- Notable eruption references ---
NOTABLE_ERUPTIONS = {
    "Mt St Helens 1980":  {"vei": 5, "volume_km3": 1.0},
    "Pinatubo 1991":      {"vei": 6, "volume_km3": 10.0},
    "Tambora 1815":       {"vei": 7, "volume_km3": 100.0},
    "Yellowstone (last)": {"vei": 8, "volume_km3": 1000.0},
}

# --- Recurrence estimates ---
RECURRENCE_YEARS = {
    5: 10,            # VEI 5: roughly every decade
    6: 100,           # VEI 6: roughly every century
    7: 1_000,         # VEI 7: roughly every millennium
    8: 50_000,        # VEI 8: every 50,000-100,000 years
}

# --- Test case: volume = 5e10 m³ (50 km³) ---
# 5e10 = 50 km³ = 10^10.699 m³
# VEI thresholds: VEI 6 covers 10^10 to 10^11 m³
# So 5e10 m³ -> VEI 6 (NOT VEI 7)
REF_VOLUME_M3       = 5e10
REF_VOLUME_KM3      = 50.0
REF_VEI_EXPECTED     = 6      # 10^10 <= 5e10 < 10^11 -> VEI 6
REF_LOG10_VOLUME     = math.log10(REF_VOLUME_M3)  # ~10.699

PRIOR_ERRORS = {
    "vei_linear":             "Treats VEI as a linear scale — it is logarithmic (10x volume per step above VEI 2)",
    "volume_thresholds_wrong": "Uses wrong volume boundaries for VEI levels (e.g., off by a factor of 10)",
    "km3_m3_confusion":       "Confuses km³ and m³ conversion: 1 km³ = 10⁹ m³, NOT 10⁶ m³",
}
