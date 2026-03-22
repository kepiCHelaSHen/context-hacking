"""
Synodic Period — Frozen Constants
Source: NASA Planetary Fact Sheet, IAU orbital elements
DO NOT MODIFY.
"""

# === Synodic period formulas ===
# Synodic period S: time between successive similar configurations
# (e.g., opposition for superior planets, inferior conjunction for inferior)
#
# Superior planets (farther than Earth):  1/S = 1/P_earth - 1/P_planet
# Inferior planets (closer than Earth):   1/S = 1/P_planet - 1/P_earth
#
# KEY: The formulas are DIFFERENT for inferior vs superior!
# Using the wrong formula gives a NEGATIVE period (physically meaningless).

# === Earth sidereal period ===
P_EARTH = 365.25   # days (tropical year, standard approximation)
P_EARTH_YR = 1.0   # years

# === Superior planets (P > P_earth) ===
# Mars: sidereal period = 687.0 days
P_MARS = 687.0     # days
S_MARS = 1.0 / (1.0 / P_EARTH - 1.0 / P_MARS)  # 779.8811 days = 2.1352 yr

# Jupiter: sidereal period = 4332.59 days (11.862 yr)
P_JUPITER = 4332.59  # days
S_JUPITER = 1.0 / (1.0 / P_EARTH - 1.0 / P_JUPITER)  # 398.8765 days = 1.0921 yr

# Saturn: sidereal period = 10759.22 days (29.457 yr)
P_SATURN = 10759.22  # days
S_SATURN = 1.0 / (1.0 / P_EARTH - 1.0 / P_SATURN)  # 378.0851 days = 1.0351 yr

# === Inferior planets (P < P_earth) ===
# Venus: sidereal period = 224.7 days
P_VENUS = 224.7     # days
S_VENUS = 1.0 / (1.0 / P_VENUS - 1.0 / P_EARTH)  # 583.9322 days = 1.5987 yr

# Mercury: sidereal period = 87.97 days
P_MERCURY = 87.97   # days
S_MERCURY = 1.0 / (1.0 / P_MERCURY - 1.0 / P_EARTH)  # 115.8794 days = 0.3173 yr

# === Wrong formula demonstration (Venus with superior formula) ===
# 1/S = 1/365.25 - 1/224.7 = -0.001713 → S = -583.93 days (NEGATIVE! WRONG)
WRONG_S_VENUS = 1.0 / (1.0 / P_EARTH - 1.0 / P_VENUS)  # -583.9322 (negative!)

# === Known LLM errors ===
PRIOR_ERRORS = {
    "same_formula_all":     "Uses the same formula (typically the superior formula) for "
                            "both inferior and superior planets; the formulas DIFFER — "
                            "superior: 1/S=1/Pe-1/Pp, inferior: 1/S=1/Pp-1/Pe",
    "synodic_is_sidereal":  "Confuses synodic period with sidereal period; synodic is "
                            "the apparent period as seen from Earth, sidereal is the "
                            "true orbital period relative to the stars",
    "negative_period":      "Gets a negative synodic period from applying the wrong "
                            "formula (e.g., superior formula for an inferior planet); "
                            "a correct formula always yields S > 0",
}
