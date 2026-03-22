"""
Earthquake Magnitude (Richter vs Moment Magnitude) — Frozen Constants
Source: Kanamori 1977, Hanks & Kanamori 1979, USGS Earthquake Hazards Program
DO NOT MODIFY.
"""

import math

# --- Moment magnitude formula constants ---
# Mw = (2/3) * (log10(M0) - 9.1)  where M0 in N·m
# Equivalent: Mw = (2/3) * log10(M0) - 6.0667
MW_COEFF       = 2.0 / 3.0          # 0.6667
MW_OFFSET_NM   = 9.1                # offset for M0 in N·m
MW_OFFSET_DYNE = 10.7               # offset for M0 in dyne·cm (1 N·m = 1e7 dyne·cm)

# --- Energy-magnitude relation ---
# log10(E) = 1.5 * Mw + 4.8   (E in joules)
# Gutenberg-Richter energy-magnitude relation
ENERGY_SLOPE   = 1.5
ENERGY_OFFSET  = 4.8                # joules

# --- Scaling per unit magnitude change ---
AMPLITUDE_FACTOR_PER_UNIT = 10.0             # 10x amplitude per +1 magnitude
ENERGY_FACTOR_PER_UNIT    = 10 ** 1.5        # ~31.623x energy per +1 magnitude
LOG10_ENERGY_PER_UNIT     = 1.5              # log10 of energy ratio per +1 Mw

# --- ML saturation threshold ---
# Richter local magnitude (ML) saturates for large earthquakes
ML_SATURATION_THRESHOLD = 7.0       # ML unreliable above ~7

# --- Reference values for validation ---
# M0 = 1e20 N·m -> Mw = (2/3)*(20 - 9.1) = (2/3)*10.9 = 7.2667
REF_M0_NM       = 1e20              # N·m
REF_MW_EXPECTED  = MW_COEFF * (math.log10(REF_M0_NM) - MW_OFFSET_NM)  # 7.2667
REF_ENERGY_RATIO = 10 ** 1.5        # 31.623 (energy ratio for +1 Mw)

PRIOR_ERRORS = {
    "10x_energy":         "claims 10x energy per unit magnitude, actual is ~31.6x (10^1.5)",
    "richter_not_moment": "uses ML formula for large quakes; ML saturates above ~7",
    "magnitude_linear":   "treats magnitude as linear scale; it is logarithmic",
}
