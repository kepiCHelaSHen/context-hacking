"""
Gravitational Physics — Frozen Constants
Source: CODATA 2018, NASA Planetary Fact Sheets
DO NOT MODIFY.
"""
import math

G_NEWTON = 6.67430e-11     # N·m²/kg² (CODATA 2018, ±0.00015e-11)
# LLM prior: 6.67e-11 or 6.674e-11

# Solar system data (NASA)
M_SUN = 1.98892e30         # kg
M_EARTH = 5.9722e24        # kg
M_MOON = 7.342e22          # kg
R_EARTH = 6.371e6          # m (mean radius)
R_EARTH_ORBIT = 1.496e11   # m (1 AU)
R_MOON_ORBIT = 3.844e8     # m

# Escape velocity: v_esc = √(2GM/R)
V_ESC_EARTH = math.sqrt(2 * G_NEWTON * M_EARTH / R_EARTH)  # = 11186 m/s
# LLM prior: 11.2 km/s (close but imprecise)

# Orbital velocity: v_orb = √(GM/R)
V_ORB_EARTH = math.sqrt(G_NEWTON * M_SUN / R_EARTH_ORBIT)  # = 29784 m/s

# Kepler's 3rd law: T² = (4π²/GM)·a³
T_EARTH = 2 * math.pi * math.sqrt(R_EARTH_ORBIT**3 / (G_NEWTON * M_SUN))
# = 3.156e7 s ≈ 365.25 days

# Surface gravity: g = GM/R²
G_SURFACE = G_NEWTON * M_EARTH / R_EARTH**2  # ≈ 9.82 m/s²

PRIOR_ERRORS = {
    "g_rounded":          "Uses G=6.67e-11 instead of 6.67430e-11",
    "escape_vs_orbital":  "Confuses escape velocity (√2 factor) with orbital",
    "r_not_r2":           "Uses r instead of r² in gravitational force",
    "altitude_vs_radius": "Uses altitude above surface instead of distance from center",
}
