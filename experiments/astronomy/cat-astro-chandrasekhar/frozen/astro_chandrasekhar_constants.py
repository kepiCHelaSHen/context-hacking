"""Chandrasekhar Limit — Frozen Constants. Source: Chandrasekhar (1931), Shapiro & Teukolsky. DO NOT MODIFY."""
# M_Ch = 5.83 * M_sun / μ_e²  (for C/O white dwarf, μ_e ≈ 2)
# M_Ch = 5.83 * 1.989e30 / 4 = 2.894e30 kg ≈ 1.456 M_sun ≈ 1.44 M_sun (standard textbook)
# KEY: 1.44 M_sun, NOT 1.4 M_sun — the extra 0.04 matters for precision!

M_SUN = 1.989e30           # kg (solar mass)
OMEGA_CH = 5.83            # dimensionless Chandrasekhar constant (5.83/(μ_e)² × M_sun)
MU_E_CO = 2.0              # mean molecular weight per electron for C/O white dwarf
MU_E_HE = 2.0              # mean molecular weight per electron for He white dwarf
MU_E_FE = 2.154            # mean molecular weight per electron for Fe white dwarf

# Chandrasekhar limit in solar masses for C/O WD (μ_e = 2)
M_CH_MSUN = OMEGA_CH / MU_E_CO ** 2     # = 5.83 / 4 = 1.4575 M_sun ≈ 1.44 M_sun
M_CH_KG = M_CH_MSUN * M_SUN             # = 2.899e30 kg

# TOV limit (neutron star) — NOT the same as Chandrasekhar!
M_TOV_MSUN = 2.16          # approximate TOV limit in solar masses (Margalit & Metzger 2017)

# Precomputed reference values
M_CH_FE_MSUN = OMEGA_CH / MU_E_FE ** 2  # ≈ 1.256 M_sun (iron-core WD)

# White dwarf mass-radius relation: R ∝ M^(-1/3)
# More massive = SMALLER (inverse cube root)
WD_RADIUS_EXPONENT = -1.0 / 3.0

# WRONG values — for trap detection
M_CH_WRONG_ROUNDED = 1.4   # WRONG: rounds away 0.04 M_sun
M_CH_WRONG_TOV = M_TOV_MSUN  # WRONG: confuses Chandrasekhar with TOV limit

PRIOR_ERRORS = {
    "limit_1_point_4":          "Rounds 1.44 to 1.4 M_sun — loses 0.04 M_sun of precision",
    "bigger_mass_bigger_radius": "Claims more massive WD is larger — actually R ∝ M^(-1/3), more mass = SMALLER",
    "applies_to_neutron_stars":  "Confuses Chandrasekhar limit (~1.44 M_sun) with TOV limit (~2-3 M_sun)",
}
