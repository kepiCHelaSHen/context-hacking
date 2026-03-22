"""
Stellar Magnitude — Frozen Constants
Source: IAU 2015 Resolution B2, Pogson (1856), HIPPARCOS catalog
DO NOT MODIFY.
"""
import math

# === Distance Modulus ===
# m - M = 5*log10(d) - 5   where d in parsecs
# Equivalently: m - M = 5*log10(d/10)
# KEY: Reference distance is 10 pc, NOT 1 pc!
# The -5 comes from 5*log10(10) = 5

# === Pogson's Flux Ratio ===
# F1/F2 = 10^((m2 - m1) / 2.5)
# 5 magnitudes = exactly 100x flux ratio (by definition)
# Lower m = brighter (inverted scale!)

# --- Test star: d=100 pc, M=0 ---
D_TEST = 100.0       # pc
M_TEST = 0.0         # absolute magnitude
DM_TEST = 5 * math.log10(D_TEST) - 5              # = 5.0
M_APP_TEST = M_TEST + DM_TEST                      # = 5.0
# WRONG formula (5*log10(d), no -5): would give m=10.0 — 5 mag too faint!
DM_TEST_WRONG = 5 * math.log10(D_TEST)             # = 10.0

# --- Sun ---
M_SUN_APP = -26.74   # apparent magnitude (from Earth)
M_SUN_ABS = 4.83     # absolute magnitude (at 10 pc)
DM_SUN = M_SUN_APP - M_SUN_ABS                     # = -31.57
AU_IN_PC = 1.0 / 206265.0                          # = 4.8481e-6 pc
DM_SUN_CHECK = 5 * math.log10(AU_IN_PC) - 5        # = -31.57

# --- Sirius: brightest star ---
M_SIRIUS_ABS = 1.42
D_SIRIUS = 2.64      # pc
DM_SIRIUS = 5 * math.log10(D_SIRIUS) - 5           # ~ -2.892
M_SIRIUS_APP = M_SIRIUS_ABS + DM_SIRIUS            # ~ -1.472 (actual: -1.46)

# --- Star at 10 pc: distance modulus = 0 (m = M by definition) ---
DM_AT_10PC = 5 * math.log10(10.0) - 5              # = 0.0

# --- Flux ratio: 5 magnitudes = 100x ---
FLUX_RATIO_5MAG = 10 ** (5.0 / 2.5)                # = 100.0
FLUX_RATIO_1MAG = 10 ** (1.0 / 2.5)                # ~ 2.512

PRIOR_ERRORS = {
    "distance_modulus_no_minus_5": "Uses 5*log10(d) instead of 5*log10(d)-5 (forgets 10pc reference)",
    "brighter_is_larger":          "Claims brighter stars have larger m — WRONG, lower m = brighter",
    "flux_ratio_wrong":            "Wrong exponent in Pogson's ratio (e.g. 10^(dm/5) instead of 10^(dm/2.5))",
}
