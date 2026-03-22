"""Temperature Lapse Rate — Frozen Constants. Source: Wallace & Hobbs 'Atmospheric Science' 2e, AMS Glossary. DO NOT MODIFY."""
import math

# Physical constants
G = 9.81          # m/s² gravitational acceleration
CP = 1004.0       # J/(kg·K) specific heat of dry air at constant pressure

# Dry Adiabatic Lapse Rate: Γd = g / cp
DALR = G / CP     # ≈ 0.00977 °C/m ≈ 9.77 °C/km, conventionally rounded to 9.8 °C/km
DALR_PER_KM = DALR * 1000  # ≈ 9.77 °C/km

# Moist (Saturated) Adiabatic Lapse Rate — varies with T and moisture
# Typical range 5–6 °C/km; we use 5.5 °C/km as representative mid-troposphere value
MALR_PER_KM = 5.5  # °C/km (representative)

# Environmental (observed average) lapse rate — ISA / US Standard Atmosphere
ENV_LAPSE_PER_KM = 6.5  # °C/km

# KEY ordering: DALR > environmental > MALR
# DALR applies to unsaturated rising air parcels
# MALR applies to saturated (cloud-forming) rising air parcels
# Environmental is the average observed temperature profile, not a process rate

# Test case: T_surface = 20°C, altitude = 3 km
T_SURFACE = 20.0   # °C
ALT_KM = 3.0       # km

T_DRY_3KM = T_SURFACE - DALR_PER_KM * ALT_KM       # 20 - 29.31 ≈ -9.31°C (exact); ≈ -9.4 with 9.8
T_MOIST_3KM = T_SURFACE - MALR_PER_KM * ALT_KM      # 20 - 16.5 = 3.5°C
T_ENV_3KM = T_SURFACE - ENV_LAPSE_PER_KM * ALT_KM    # 20 - 19.5 = 0.5°C

# Using conventional 9.8 °C/km for DALR
DALR_CONV = 9.8    # °C/km — conventional rounded value
T_DRY_3KM_CONV = T_SURFACE - DALR_CONV * ALT_KM      # 20 - 29.4 = -9.4°C

# Lifting Condensation Level approximation: LCL ≈ (T - Td) / 8  km
# (Espy/Bolton approximation, accurate to ~200m for typical conditions)
T_TEST_LCL = 25.0   # °C
TD_TEST_LCL = 17.0  # °C (dewpoint)
LCL_TEST = (T_TEST_LCL - TD_TEST_LCL) / 8.0   # = 1.0 km

# Stability criterion:
# If environmental lapse rate > DALR → absolutely unstable
# If environmental lapse rate < MALR → absolutely stable
# If MALR < env < DALR → conditionally unstable
STABLE_ENV = 5.0     # °C/km — stable (less than MALR)
UNSTABLE_ENV = 11.0  # °C/km — absolutely unstable (greater than DALR)
CONDITIONAL_ENV = 7.0 # °C/km — conditionally unstable (between MALR and DALR)

PRIOR_ERRORS = {
    "dry_moist_same":  "Claims DALR equals MALR — they differ by ~4°C/km",
    "env_is_dry":      "Uses 9.8°C/km for environmental lapse rate (should be 6.5°C/km)",
    "dalr_wrong_value": "Uses 6.5 or 5°C/km for dry adiabatic (should be ~9.8°C/km)",
}
