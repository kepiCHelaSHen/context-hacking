"""
Kepler's Third Law — Frozen Constants
Source: CODATA 2018 (G), IAU 2012 (AU), NASA Planetary Fact Sheets
DO NOT MODIFY.
"""
import math

# === Fundamental constants ===
G_NEWTON = 6.67430e-11     # N·m²/kg² (CODATA 2018, ±0.00015e-11)
# LLM prior: 6.674e-11 or 6.67e-11

# === Masses ===
M_SUN = 1.98892e30         # kg (solar mass)
# LLM prior: 1.989e30 (close but imprecise)

# === Unit conversions ===
AU_METERS = 1.496e11       # m per AU (IAU 2012: 1.495978707e11)
YR_SECONDS = 3.15576e7     # s per Julian year (365.25 days * 86400 s/day)

# === Kepler's 3rd law: T² = (4π²/(GM)) · a³ ===
# The Kepler constant k = 4π²/(GM) has units s²/m³
# KEY INSIGHT: k depends on the central mass M!
#   - Solar system: k_sun  = 4π²/(G·M_sun)
#   - Binary star with 2M_sun: k = 4π²/(G·2M_sun) = k_sun/2
#   - Exoplanet system: k depends on the host star mass

KEPLER_CONSTANT_SUN = 4 * math.pi**2 / (G_NEWTON * M_SUN)
# = 39.4784 / (6.67430e-11 * 1.98892e30)
# = 39.4784 / 1.32749e20
# = 2.9746e-19 s²/m³

# === Solar system convenience: T²/a³ = 1 yr²/AU³ ===
# When T in years and a in AU, the constant is ~1 for the solar system.
# This ONLY works for the solar system (M = M_sun).
KEPLER_RATIO_SOLAR_YR_AU = 1.0  # yr²/AU³ (by definition of these units)

# === Verification: Earth orbit ===
A_EARTH = AU_METERS                    # 1 AU
T_EARTH = 2 * math.pi * math.sqrt(A_EARTH**3 / (G_NEWTON * M_SUN))
# ≈ 3.156e7 s ≈ 365.26 days ✓
T_EARTH_DAYS = T_EARTH / 86400

# Ratio check: T²/a³ should equal KEPLER_CONSTANT_SUN
RATIO_EARTH = T_EARTH**2 / A_EARTH**3
# ≈ 2.9746e-19 s²/m³ ✓

# === Double-mass star verification ===
# For a star with M = 2*M_sun, the constant halves
M_DOUBLE_SUN = 2 * M_SUN
KEPLER_CONSTANT_DOUBLE = 4 * math.pi**2 / (G_NEWTON * M_DOUBLE_SUN)
# = KEPLER_CONSTANT_SUN / 2 ≈ 1.4873e-19 s²/m³

# Period of a planet at 1 AU around a 2M_sun star:
T_DOUBLE_AT_1AU = 2 * math.pi * math.sqrt(A_EARTH**3 / (G_NEWTON * M_DOUBLE_SUN))
# ≈ T_EARTH / sqrt(2) ≈ 258.3 days (faster orbit for same distance)
T_DOUBLE_AT_1AU_DAYS = T_DOUBLE_AT_1AU / 86400

# === Known LLM errors ===
PRIOR_ERRORS = {
    "constant_universal":  "Claims T²/a³ is the same constant for ALL systems "
                           "(ignores that k = 4π²/(GM) depends on central mass M)",
    "mass_not_included":   "Omits M from the Kepler constant; writes T² = C·a³ "
                           "with C fixed, instead of C = 4π²/(GM)",
    "uses_1_au_yr":        "Uses the simplified T²/a³ = 1 yr²/AU³ for non-solar "
                           "systems where the host star mass differs from M_sun",
}
