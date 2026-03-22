"""
Plate Motion — Velocity from Hotspot Tracks — Frozen Constants
Source: Müller et al. (2008), Pacific plate motion, Hawaiian-Emperor chain.
DO NOT MODIFY.
"""
import math

R_EARTH = 6371.0  # km — mean Earth radius (IUGG)

# --- Hawaiian chain reference data ---
# Hotspot track: distance from Kilauea to Emperor Seamount bend ≈ 3500 km
# Age at bend (Detroit Seamount): ≈ 43 Ma
HAWAII_DIST_KM = 3500.0
HAWAII_AGE_MA = 43.0
HAWAII_V_MMYR = HAWAII_DIST_KM / HAWAII_AGE_MA  # km/Ma = mm/yr ≈ 81.40 mm/yr
HAWAII_V_CMYR = HAWAII_V_MMYR / 10.0             # ≈ 8.14 cm/yr

# --- Simple test case ---
# distance = 600 km, age = 10 Ma
TEST_DIST_KM = 600.0
TEST_AGE_MA = 10.0
TEST_V_MMYR = TEST_DIST_KM / TEST_AGE_MA   # = 60.0 mm/yr
TEST_V_CMYR = TEST_V_MMYR / 10.0            # = 6.0 cm/yr
# LLM trap: 60 m/yr is 1000× too fast! Plates move mm/yr or cm/yr, NOT m/yr.

# --- Great circle distance reference ---
# Honolulu (21.3°N, 157.8°W) to Midway (28.2°N, 177.4°W)
LAT1_HON, LON1_HON = 21.3, -157.8
LAT2_MID, LON2_MID = 28.2, -177.4
# Haversine:
_phi1 = math.radians(LAT1_HON)
_phi2 = math.radians(LAT2_MID)
_dphi = math.radians(LAT2_MID - LAT1_HON)
_dlam = math.radians(LON2_MID - LON1_HON)
_a = math.sin(_dphi / 2)**2 + math.cos(_phi1) * math.cos(_phi2) * math.sin(_dlam / 2)**2
GC_DIST_HON_MID = R_EARTH * 2 * math.atan2(math.sqrt(_a), math.sqrt(1 - _a))  # ≈ 2097 km

# --- Euler pole velocity ---
# v = ω · R · sin(θ)  where θ = angular distance from Euler pole
# Pacific plate Euler pole (HS3-NUVEL1A): ω ≈ 0.967 °/Myr
OMEGA_PACIFIC_DEG_MYR = 0.967
# At θ = 60° from Euler pole:
TEST_THETA_DEG = 60.0
# v = ω(rad/Myr) · R(km) · sin(θ) → km/Myr = mm/yr
EULER_V_TEST = math.radians(OMEGA_PACIFIC_DEG_MYR) * R_EARTH * math.sin(math.radians(TEST_THETA_DEG))
# ≈ 0.01688 rad/Myr × 6371 km × 0.8660 ≈ 93.10 mm/yr

# Typical plate velocities: 1–10 cm/yr = 10–100 mm/yr
# LLM trap: values in m/yr (60 m/yr) are 1000× too fast
# LLM trap: straight-line distance on Mercator projection ≠ great circle distance
# LLM trap: velocity is NOT uniform across plate — it varies with angular distance from Euler pole

PRIOR_ERRORS = {
    "units_m_per_yr":        "Uses m/yr instead of mm/yr or cm/yr (1000× too fast)",
    "straight_line_distance": "Uses Euclidean map distance instead of great circle (haversine)",
    "euler_pole_ignored":     "Assumes uniform velocity across plate (ignores Euler pole rotation)",
}
