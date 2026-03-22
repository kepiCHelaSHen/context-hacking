"""Schwarzschild Radius — Frozen Constants. Source: Misner, Thorne & Wheeler (Gravitation). DO NOT MODIFY."""
# r_s = 2GM/c²  (the factor of 2 is CRITICAL!)
# Without the 2 you get HALF the correct event horizon radius.
G = 6.674e-11          # m³ kg⁻¹ s⁻² (gravitational constant)
C = 2.998e8            # m/s (speed of light)
C_SQUARED = C ** 2     # = 8.988e16 m²/s²
M_SUN = 1.989e30       # kg (solar mass)
M_EARTH = 5.972e24     # kg (Earth mass)
M_SGR_A_STAR = 4e6 * M_SUN  # ~4 million solar masses
AU = 1.496e11          # m (astronomical unit)

# Precomputed reference values — factor of 2 included
RS_SUN = 2 * G * M_SUN / C_SQUARED                # = 2953.8 m ≈ 2.954 km
RS_EARTH = 2 * G * M_EARTH / C_SQUARED            # = 8.869e-3 m ≈ 8.87 mm
RS_SGR_A_STAR = 2 * G * M_SGR_A_STAR / C_SQUARED  # ≈ 1.18e10 m ≈ 0.079 AU

# WRONG values (missing factor of 2) — for trap detection
RS_SUN_WRONG = G * M_SUN / C_SQUARED              # = 1476.9 m ≈ 1.477 km (WRONG!)
RS_EARTH_WRONG = G * M_EARTH / C_SQUARED          # = 4.434e-3 m (WRONG!)

# Scaling: r_s ∝ M (linear in mass)
PRIOR_ERRORS = {
    "missing_factor_2": "Uses GM/c² instead of 2GM/c² — gives half the correct radius",
    "wrong_c_squared":  "Forgets c² or uses c instead of c² in denominator",
    "km_vs_m":          "Unit confusion between km and m in final answer",
}
