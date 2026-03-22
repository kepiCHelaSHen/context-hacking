"""Escape Velocity — Frozen Constants. Source: NASA Planetary Fact Sheet. DO NOT MODIFY."""
import math
# v_esc = sqrt(2GM/R) where R = distance from CENTER of body (mean radius)
# KEY: R must be mean radius, NOT equatorial, NOT surface altitude
G = 6.674e-11  # gravitational constant (m³ kg⁻¹ s⁻²)

# Earth — mean radius 6371 km (NOT equatorial 6378 km)
M_EARTH = 5.972e24   # kg
R_EARTH_MEAN = 6.371e6   # m (mean radius — correct)
R_EARTH_EQUATORIAL = 6.378e6  # m (equatorial — WRONG for v_esc)
V_ESC_EARTH = math.sqrt(2 * G * M_EARTH / R_EARTH_MEAN)  # 11185.7 m/s ≈ 11.19 km/s

# Moon
M_MOON = 7.342e22   # kg
R_MOON = 1.737e6    # m
V_ESC_MOON = math.sqrt(2 * G * M_MOON / R_MOON)  # 2375.3 m/s ≈ 2.38 km/s

# Mars
M_MARS = 6.417e23   # kg
R_MARS = 3.390e6    # m
V_ESC_MARS = math.sqrt(2 * G * M_MARS / R_MARS)  # 5026.6 m/s ≈ 5.03 km/s

# Jupiter
M_JUPITER = 1.898e27  # kg
R_JUPITER = 6.991e7   # m
V_ESC_JUPITER = math.sqrt(2 * G * M_JUPITER / R_JUPITER)  # 60198.6 m/s ≈ 60.20 km/s

# Surface gravity for reference: g = GM/R²
G_EARTH = G * M_EARTH / R_EARTH_MEAN**2   # 9.820 m/s²
G_MOON  = G * M_MOON / R_MOON**2          # 1.624 m/s²
G_MARS  = G * M_MARS / R_MARS**2          # 3.727 m/s²

# Scaling law: v_esc ∝ sqrt(M/R) — for same density, larger planet has larger v_esc

PRIOR_ERRORS = {
    "wrong_radius":      "Uses equatorial 6378km instead of mean 6371km for Earth",
    "no_sqrt":           "Forgets square root — computes 2GM/R instead of sqrt(2GM/R)",
    "mass_radius_swapped": "Swaps M and R — computes sqrt(2GR/M) instead of sqrt(2GM/R)",
}
