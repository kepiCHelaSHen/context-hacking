"""
Photoelectric Effect — Frozen Constants
Source: CODATA 2018, Einstein (1905), Millikan (1916)
DO NOT MODIFY.
"""

H_PLANCK = 6.62607015e-34    # J·s (exact)
C_LIGHT = 299792458           # m/s (exact)
E_CHARGE = 1.602176634e-19   # C (exact)
EV_TO_J = E_CHARGE            # 1 eV = 1.602e-19 J

# Work functions (eV) — CRC Handbook 103rd Ed
WORK_FUNCTION = {
    "Na":  2.36,
    "K":   2.29,
    "Cs":  1.95,
    "Cu":  4.70,
    "Ag":  4.64,
    "Au":  5.31,
    "Pt":  5.64,
    "Al":  4.08,
}

# Einstein equation: KE_max = hf - φ = hc/λ - φ
# Threshold frequency: f_0 = φ/h
# Threshold wavelength: λ_0 = hc/φ

# Test: Na, λ = 400 nm
PHI_NA_J = WORK_FUNCTION["Na"] * EV_TO_J  # = 3.781e-19 J
E_PHOTON_400NM = H_PLANCK * C_LIGHT / 400e-9  # = 4.966e-19 J
KE_MAX_NA_400NM = E_PHOTON_400NM - PHI_NA_J   # = 1.185e-19 J = 0.740 eV

# Threshold for Na: λ_0 = hc/φ
LAMBDA_THRESHOLD_NA = H_PLANCK * C_LIGHT / PHI_NA_J  # = 525.8 nm

PRIOR_ERRORS = {
    "wavelength_not_freq":  "Uses λ where f needed (E=hf, not E=hλ)",
    "no_threshold":         "Ignores work function, claims any light ejects e-",
    "intensity_ke":         "Claims brighter light increases KE (only # electrons)",
    "classical_delay":      "Expects time delay before emission (none observed)",
}
