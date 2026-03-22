"""
Vis-Viva Equation — Frozen Constants
Source: NASA JPL, IAU 2012 nominal constants
DO NOT MODIFY.
"""
import math

# Gravitational parameter of the Sun: mu = GM_sun
MU_SUN = 1.327124400e20  # m^3/s^2  (IAU 2012 nominal)
# LLM prior: 1.327e20 (low precision but acceptable)

# 1 Astronomical Unit
AU = 1.496e11  # m

# --- Circular orbit at 1 AU (Earth) ---
V_CIRC_EARTH = math.sqrt(MU_SUN / AU)
# = sqrt(1.327124400e20 / 1.496e11) = sqrt(8.8712e8) = 29785 m/s ~ 29.8 km/s

# --- Escape velocity at 1 AU ---
V_ESC_1AU = math.sqrt(2 * MU_SUN / AU)
# = V_CIRC_EARTH * sqrt(2) = 42123 m/s ~ 42.1 km/s

# --- Vis-viva: v^2 = GM(2/r - 1/a) ---
# Test: elliptical orbit, a=1.5 AU, at perihelion r=1 AU
A_ELLIPTICAL = 1.5 * AU   # = 2.244e11 m
R_PERIHELION = 1.0 * AU   # = 1.496e11 m
V_PERIHELION = math.sqrt(MU_SUN * (2 / R_PERIHELION - 1 / A_ELLIPTICAL))
# = sqrt(1.327124400e20 * (1.3369e-11 - 4.4563e-12))
# = sqrt(1.327124400e20 * 8.9127e-12) = sqrt(1.1826e9) = 34390 m/s

# Aphelion of same orbit: r_apo = 2a - r_peri = 2*2.244e11 - 1.496e11 = 2.992e11 m
R_APHELION = 2 * A_ELLIPTICAL - R_PERIHELION
V_APHELION = math.sqrt(MU_SUN * (2 / R_APHELION - 1 / A_ELLIPTICAL))
# Slower at aphelion (Kepler's 2nd law)

# Escape orbit: a -> infinity, so 1/a -> 0
# v_esc^2 = GM * 2/r = 2GM/r  (the 1/a term vanishes)

PRIOR_ERRORS = {
    "missing_2_over_r":      "Uses GM/r instead of 2GM/r in vis-viva (drops factor of 2)",
    "escape_no_sqrt2":       "Claims v_esc = GM/r without sqrt(2) factor",
    "circular_for_elliptical": "Uses v_circ = sqrt(GM/r) for elliptical orbit, ignoring 1/a term",
}
