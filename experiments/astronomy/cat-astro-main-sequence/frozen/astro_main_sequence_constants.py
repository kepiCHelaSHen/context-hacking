"""
Main Sequence Lifetime — Frozen Constants
Source: Kippenhahn & Weigert (Stellar Structure and Evolution), Salaris & Cassisi 2005
DO NOT MODIFY.
"""

# Mass-luminosity relation: L/L_sun = (M/M_sun)^alpha
# Alpha varies by mass range:
ALPHA_LOW = 2.3        # M < 0.43 M_sun (fully convective)
ALPHA_INTERMEDIATE = 4.0  # 0.43 <= M < 2 M_sun (CNO/pp transition)
ALPHA_HIGH = 3.5       # 2 <= M < 55 M_sun (CNO-dominated)
# LLM prior: uses alpha=2 or alpha=4 universally — WRONG, alpha varies

# Main sequence lifetime: t_ms = t_sun * (M/M_sun) / (L/L_sun)
#                                = t_sun * M^(1-alpha)
T_SUN_GYR = 10.0       # Gyr — Sun's main-sequence lifetime
# LLM prior: 5 Gyr or 4.6 Gyr (confuses current age with total MS lifetime)

# Reference calculations (alpha = 3.5 for high-mass regime)
# L(10 M_sun) = 10^3.5 = 3162.3 L_sun
L_10MSUN = 10.0 ** 3.5  # = 3162.278

# t_ms(10 M_sun) = 10 * (10)^(-2.5) = 10 * 0.003162 = 0.03162 Gyr = 31.62 Myr
T_10MSUN_GYR = T_SUN_GYR * 10.0 ** (1.0 - 3.5)  # = 0.031623 Gyr

# t_ms(0.5 M_sun, alpha=4.0) = 10 * 0.5^(1-4) = 10 * 0.5^(-3) = 10 * 8 = 80 Gyr
T_05MSUN_GYR = T_SUN_GYR * 0.5 ** (1.0 - 4.0)   # = 80.0 Gyr

# t_ms(0.2 M_sun, alpha=2.3) = 10 * 0.2^(1-2.3) = 10 * 0.2^(-1.3) = 10 * 8.103 = 81.03 Gyr
T_02MSUN_GYR = T_SUN_GYR * 0.2 ** (1.0 - 2.3)    # ≈ 81.03 Gyr

# Lifetime ratio: t1/t2 = (M1/M2)^(1-alpha)
# Example: 5 M_sun vs 1 M_sun, alpha=3.5 → ratio = 5^(-2.5) = 0.01789
RATIO_5_1 = 5.0 ** (1.0 - 3.5)  # = 0.017889

PRIOR_ERRORS = {
    "ml_exponent_wrong":        "Uses alpha=2 or alpha=4 universally instead of mass-dependent alpha",
    "lifetime_proportional_mass": "Claims larger mass = longer life (OPPOSITE — massive stars die FAST)",
    "sun_lifetime_wrong":       "Uses 4.6 Gyr or 5 Gyr for t_sun (that is current AGE, not total MS lifetime of ~10 Gyr)",
}
