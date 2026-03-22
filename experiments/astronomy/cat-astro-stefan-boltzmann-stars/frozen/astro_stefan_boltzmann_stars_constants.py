"""Spectral Type from Temperature (Wien's Law) — Frozen Constants. Source: NIST / IAU. DO NOT MODIFY."""

# Wien's displacement law: lambda_max = b / T
# b = Wien's displacement constant
WIEN_B = 2.898e-3  # m*K (NIST CODATA value: 2.8977719e-3)

# Spectral type temperature boundaries (Harvard classification)
# O: T > 30000 K  (hottest, blue)
# B: 10000 < T <= 30000
# A: 7500 < T <= 10000
# F: 6000 < T <= 7500
# G: 5200 < T <= 6000
# K: 3700 < T <= 5200
# M: 2400 < T <= 3700  (coolest main-sequence, red)
SPECTRAL_BOUNDARIES = {
    "O": (30000, None),    # T > 30000
    "B": (10000, 30000),
    "A": (7500, 10000),
    "F": (6000, 7500),
    "G": (5200, 6000),
    "K": (3700, 5200),
    "M": (2400, 3700),
}

# Reference stars
T_SUN = 5778           # K — spectral type G2
T_SIRIUS = 9940        # K — spectral type A1
T_BETELGEUSE = 3600    # K — spectral type M2

# Pre-computed peak wavelengths (Wien's law)
LAMBDA_SUN = WIEN_B / T_SUN              # 5.016e-7 m = 501.6 nm (green-yellow)
LAMBDA_SIRIUS = WIEN_B / T_SIRIUS        # 2.916e-7 m = 291.6 nm (UV)
LAMBDA_BETELGEUSE = WIEN_B / T_BETELGEUSE  # 8.050e-7 m = 805.0 nm (near-IR)

# Verification (nm)
LAMBDA_SUN_NM = LAMBDA_SUN * 1e9          # ~501.6 nm
LAMBDA_SIRIUS_NM = LAMBDA_SIRIUS * 1e9    # ~291.5 nm
LAMBDA_BETELGEUSE_NM = LAMBDA_BETELGEUSE * 1e9  # ~805.0 nm

# Wrong-value traps (for testing LLM errors)
WIEN_B_WRONG = 2.898e-4   # common mistake: wrong exponent (1e-4 vs 1e-3)

PRIOR_ERRORS = {
    "wien_constant_wrong":       "Uses wrong Wien constant (e.g. 2.898e-4 or 2.898e-2 instead of 2.898e-3 m*K)",
    "spectral_boundaries_wrong": "Uses wrong temperature boundaries for spectral classes (e.g. G starts at 5000 instead of 5200)",
    "peak_is_color":             "Claims star perceived color = peak wavelength color; perceived color integrates full Planck spectrum",
}
