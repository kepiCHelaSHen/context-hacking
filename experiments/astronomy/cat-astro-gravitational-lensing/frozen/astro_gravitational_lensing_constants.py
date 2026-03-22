"""Gravitational Lensing — Frozen Constants. Source: Schneider, Kochanek & Wambsganss (Gravitational Lensing). DO NOT MODIFY."""
# Einstein ring: theta_E = sqrt(4GM/c^2 * D_ls / (D_l * D_s))
# GR deflection:  alpha  = 4GM / (c^2 * b)    (Einstein's result — 2x Newtonian!)
# Newtonian:      alpha  = 2GM / (c^2 * b)    (WRONG by factor of 2)
import math

G = 6.674e-11          # m^3 kg^-1 s^-2 (gravitational constant)
C = 2.998e8            # m/s (speed of light)
C_SQUARED = C ** 2     # = 8.988e16 m^2/s^2
M_SUN = 1.989e30       # kg (solar mass)
R_SUN = 6.957e8        # m (solar radius)
KPC = 3.086e19         # m (1 kiloparsec)
RAD_TO_ARCSEC = 206265 # 1 radian in arcseconds

# --- Test geometry: stellar-mass lens at 4 kpc, source at 8 kpc ---
D_L_TEST = 4 * KPC                  # 1.2344e20 m
D_S_TEST = 8 * KPC                  # 2.4688e20 m
D_LS_TEST = 4 * KPC                 # 1.2344e20 m (= D_s - D_l, valid for nearby/non-cosmological)

# Precomputed reference values
RS_SUN = 2 * G * M_SUN / C_SQUARED                                          # 2953.845 m
FOUR_GM_C2_SUN = 4 * G * M_SUN / C_SQUARED                                  # 5907.690 m
THETA_E_TEST = math.sqrt(FOUR_GM_C2_SUN * D_LS_TEST / (D_L_TEST * D_S_TEST))  # ~4.892e-9 rad
THETA_E_TEST_MAS = THETA_E_TEST * RAD_TO_ARCSEC * 1000                      # ~1.009 milliarcsec

# Solar limb deflection (Eddington 1919: ~1.75 arcsec)
DEFLECTION_SOLAR_LIMB = 4 * G * M_SUN / (C_SQUARED * R_SUN)  # ~8.49e-6 rad = ~1.751 arcsec
DEFLECTION_SOLAR_LIMB_ARCSEC = DEFLECTION_SOLAR_LIMB * RAD_TO_ARCSEC  # ~1.751

# WRONG: Newtonian deflection (half of GR) — for trap detection
DEFLECTION_SOLAR_LIMB_NEWTONIAN = 2 * G * M_SUN / (C_SQUARED * R_SUN)  # WRONG! ~0.876 arcsec
DEFLECTION_SOLAR_LIMB_NEWTONIAN_ARCSEC = DEFLECTION_SOLAR_LIMB_NEWTONIAN * RAD_TO_ARCSEC

# WRONG: D_ls = D_s - D_l for cosmological distances (angular diameter distances don't subtract!)
# For our test geometry (non-cosmological), this happens to be correct.
# But at z > 0.1, the error is significant.

PRIOR_ERRORS = {
    "newtonian_deflection":  "Uses 2GM/(c^2*b) instead of 4GM/(c^2*b) — factor of 2 wrong (Newtonian, not GR)",
    "distance_subtraction":  "Assumes D_ls = D_s - D_l for cosmological distances — angular diameter distances don't subtract",
    "no_einstein_ring":      "Claims gravitational lensing only produces point deflection, not an Einstein ring",
}
