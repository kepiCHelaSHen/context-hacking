"""CMB Temperature — Frozen Constants. Source: COBE/FIRAS (Mather et al. 1999), NIST CODATA. DO NOT MODIFY."""

# CMB temperature — COBE/FIRAS measurement (most precise value)
T_CMB = 2.7255  # K  (Fixsen 2009, uncertainty ±0.0006 K)

# Physical constants
WIEN_B = 2.898e-3          # m*K — Wien displacement constant (wavelength form)
WIEN_B_FREQ = 5.879e10     # Hz/K — Wien displacement constant (frequency form)
C_LIGHT = 2.998e8          # m/s — speed of light

# Pre-computed Wien peak wavelength:  lambda_max = b / T_CMB
LAMBDA_MAX_M = WIEN_B / T_CMB          # 1.06329e-3 m
LAMBDA_MAX_MM = LAMBDA_MAX_M * 1e3     # 1.06329 mm (microwave!)

# Pre-computed Wien peak frequency:  nu_max = b_nu * T_CMB
NU_MAX_HZ = WIEN_B_FREQ * T_CMB        # ~1.6023e11 Hz
NU_MAX_GHZ = NU_MAX_HZ / 1e9           # ~160.23 GHz (microwave band)

# Last scattering surface
Z_LAST_SCATTERING = 1089               # redshift of CMB decoupling
T_LAST_SCATTERING = T_CMB * (1 + Z_LAST_SCATTERING)  # ~2970.8 K

# The CMB is the most perfect blackbody ever measured
# Deviations from Planck spectrum: < 0.01% (50 parts per million)

# ── Wrong-value traps (for testing LLM errors) ──────────────────
T_CMB_WRONG_3K = 3.0       # Common rounding: 3 K instead of 2.7255 K (10.1% error)

PRIOR_ERRORS = {
    "t_cmb_3k":        "Rounds CMB temperature to 3 K instead of precise 2.7255 K — 10% error that propagates to Wien peak",
    "peak_wrong_band": "Claims CMB peak is in visible or infrared instead of microwave (1.063 mm = microwave)",
    "not_blackbody":   "Claims CMB deviates significantly from blackbody; in fact it is the most perfect blackbody ever measured (<0.01%)",
}
