"""
Stellar Parallax — Frozen Constants
Source: IAU 2012/2015 nominal values, Hipparcos/Gaia catalogs
DO NOT MODIFY.
"""

# === Parallax formula ===
# d(pc) = 1 / p(arcsec)
# where p = parallax SEMI-ANGLE (half the total annual shift)
# KEY: p is the SEMI-angle, not the full angular shift across 6 months

# === Parsec definition ===
# 1 parsec = distance at which 1 AU subtends an angle of 1 arcsecond
# 1 pc = 206265 AU = 3.08567758e16 m = 3.26156 ly
PC_IN_AU = 206265             # AU per parsec (exact: 648000/pi)
PC_IN_METERS = 3.08567758e16  # m per parsec (IAU 2015)
PC_IN_LY = 3.26156            # light-years per parsec

# === Unit conversions ===
ARCSEC_PER_RADIAN = 206265    # 1 radian = 206265 arcseconds (= 648000/pi)
LY_IN_METERS = 9.4607e15      # m per light-year

# === Proxima Centauri (nearest star) ===
P_PROXIMA_ARCSEC = 0.7687     # parallax semi-angle in arcseconds (Gaia DR3)
D_PROXIMA_PC = 1.0 / P_PROXIMA_ARCSEC  # = 1.30091 pc
D_PROXIMA_LY = D_PROXIMA_PC * PC_IN_LY  # = 4.2441 ly

# === Gaia mission precision limit ===
P_GAIA_LIMIT_ARCSEC = 0.001   # ~1 mas precision floor
D_GAIA_LIMIT_PC = 1.0 / P_GAIA_LIMIT_ARCSEC  # = 1000 pc = 1 kpc

# === Test case: p = 0.1 arcsec ===
P_TEST_ARCSEC = 0.1
D_TEST_PC = 1.0 / P_TEST_ARCSEC  # = 10 pc
D_TEST_LY = D_TEST_PC * PC_IN_LY  # = 32.6156 ly
D_TEST_M = D_TEST_PC * PC_IN_METERS  # = 3.08567758e17 m

# === Additional reference stars ===
# Barnard's Star: p = 0.5469" → d = 1.8285 pc = 5.963 ly
P_BARNARD_ARCSEC = 0.5469
D_BARNARD_PC = 1.0 / P_BARNARD_ARCSEC  # = 1.8285 pc
D_BARNARD_LY = D_BARNARD_PC * PC_IN_LY  # = 5.963 ly

# Sirius: p = 0.3792" → d = 2.637 pc = 8.601 ly
P_SIRIUS_ARCSEC = 0.3792
D_SIRIUS_PC = 1.0 / P_SIRIUS_ARCSEC  # = 2.6371 pc
D_SIRIUS_LY = D_SIRIUS_PC * PC_IN_LY  # = 8.601 ly

# === Known LLM errors ===
PRIOR_ERRORS = {
    "parsec_wrong_definition":  "Claims 1 pc = 1 ly or 1 pc = 1 AU; correct: "
                                "1 pc = 3.262 ly = 206265 AU = 3.086e16 m",
    "full_angle_not_semi":      "Uses the full annual parallax shift (2p) instead of "
                                "the semi-angle p; d = 1/p uses the SEMI-angle",
    "arcsec_to_rad_wrong":      "Uses wrong conversion factor for arcsec→rad; "
                                "correct: 1 arcsec = 1/206265 rad (not 1/3600)",
}
