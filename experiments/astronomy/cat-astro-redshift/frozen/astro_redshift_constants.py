"""Cosmological Redshift — Frozen Constants. Source: Weinberg Cosmology, Peebles 1993, Hogg 1999. DO NOT MODIFY."""
import math

C_KMS = 299792.458  # speed of light, km/s (exact)

# Redshift: z = (lambda_obs - lambda_emit) / lambda_emit = lambda_obs / lambda_emit - 1
# Low-z approximation: v ≈ cz (valid only for z << 1, say z < 0.1)
# Special relativistic Doppler: v/c = ((1+z)² - 1) / ((1+z)² + 1)
# KEY: Cosmological redshift is NOT a Doppler shift — it is spacetime expansion.
# LLM prior: uses v = cz for large z, yielding v > c — physically impossible.

# Test wavelength pair: Lyman-alpha rest = 121.567 nm, observed at 243.134 nm → z = 1.0
LAMBDA_EMIT_TEST = 121.567  # nm, Lyman-alpha rest wavelength
LAMBDA_OBS_TEST  = 243.134  # nm, observed wavelength → z ≈ 1.0

Z_TEST = LAMBDA_OBS_TEST / LAMBDA_EMIT_TEST - 1  # ≈ 1.0

# z = 1 test values
Z1 = 1.0
V_LOW_Z_1 = C_KMS * Z1                                      # 299792.458 km/s = c (WRONG for z=1!)
V_SR_DOPPLER_1 = ((1 + Z1)**2 - 1) / ((1 + Z1)**2 + 1)     # 3/5 = 0.6 (v/c ratio)

# z = 3 test values
Z3 = 3.0
V_LOW_Z_3 = C_KMS * Z3                                      # 899377.374 km/s = 3c (IMPOSSIBLE!)
V_SR_DOPPLER_3 = ((1 + Z3)**2 - 1) / ((1 + Z3)**2 + 1)     # 15/17 ≈ 0.88235 (v/c ratio)

# z = 0.05 — safely in low-z regime
Z_LOW = 0.05
V_LOW_Z_LOW = C_KMS * Z_LOW                                                 # ≈ 14989.6 km/s
V_SR_DOPPLER_LOW = ((1 + Z_LOW)**2 - 1) / ((1 + Z_LOW)**2 + 1)             # ≈ 0.04878 (v/c)
# For z << 1, cz and SR Doppler should nearly agree:
V_SR_DOPPLER_LOW_KMS = V_SR_DOPPLER_LOW * C_KMS                             # ≈ 14625.5 km/s

# Threshold for low-z validity
Z_THRESHOLD = 0.1

PRIOR_ERRORS = {
    "v_cz_all_z":             "Uses v = cz for z > 0.1 (gives v > c at z ≥ 1 — physically wrong)",
    "superluminal_allowed":   "Reports v > c from naive v = cz without flagging it as invalid",
    "doppler_not_cosmological": "Treats cosmological redshift as a Doppler effect in flat spacetime",
}
