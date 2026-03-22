"""
Tidal Forces (Lunar & Solar Tidal Bulge) — Frozen Constants
Source: JPL DE440 ephemeris, IAU 2015 nominal masses
DO NOT MODIFY.
"""

# Tidal force ∝ M / d³  (NOT d² — the d³ dependence is what makes
# the Moon dominate despite the Sun being far more massive)

# Moon
M_MOON = 7.342e22       # kg — lunar mass
D_MOON = 3.844e8        # m  — mean Earth–Moon distance

# Sun
M_SUN = 1.989e30        # kg — solar mass
D_SUN = 1.496e11        # m  — mean Earth–Sun distance (1 AU)

# Tidal force factors (relative, M/d³)
TF_MOON = M_MOON / D_MOON**3          # ≈ 1.2926e-3
TF_SUN  = M_SUN  / D_SUN**3           # ≈ 5.9407e-4

# Sun / Moon tidal force ratio
SUN_MOON_RATIO = TF_SUN / TF_MOON     # ≈ 0.4596
# KEY: Sun's tidal force is ~46% of Moon's — NOT negligible!

# Spring tide: Moon + Sun aligned → combined factor relative to Moon alone
SPRING_FACTOR = 1.0 + SUN_MOON_RATIO  # ≈ 1.4596
# Neap tide: Moon + Sun perpendicular → difference factor
NEAP_FACTOR   = 1.0 - SUN_MOON_RATIO  # ≈ 0.5404

PRIOR_ERRORS = {
    "only_moon":        "Ignores Sun's tidal contribution (~46% of Moon's) — treats tides as Moon-only",
    "force_d_squared":  "Uses 1/d² (gravity) instead of 1/d³ (tidal force) — wrong distance exponent",
    "spring_neap_wrong": "Confuses spring and neap conditions (spring = aligned, neap = perpendicular)",
}
