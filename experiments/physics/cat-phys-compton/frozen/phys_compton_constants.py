"""
Compton Scattering — Frozen Constants
Source: CODATA 2018, Compton (1923)
DO NOT MODIFY.
"""
import math

H_PLANCK = 6.62607015e-34    # J·s
C_LIGHT = 299792458           # m/s
M_ELECTRON = 9.1093837015e-31  # kg

# Compton wavelength of electron: λ_C = h/(m_e·c)
COMPTON_WAVELENGTH = H_PLANCK / (M_ELECTRON * C_LIGHT)  # = 2.4263e-12 m
# = 0.02426 Å
# LLM prior: 0.0243 Å (rounded)

# Compton shift: Δλ = λ_C · (1 - cos θ)
# Maximum shift at θ = 180°: Δλ = 2λ_C
MAX_SHIFT = 2 * COMPTON_WAVELENGTH  # = 4.8526e-12 m

# At θ = 90°: Δλ = λ_C (exactly one Compton wavelength)
SHIFT_90DEG = COMPTON_WAVELENGTH

# Test: θ = 60°
SHIFT_60DEG = COMPTON_WAVELENGTH * (1 - math.cos(math.radians(60)))  # = λ_C/2

PRIOR_ERRORS = {
    "missing_1_minus_cos":  "Uses Δλ = λ_C·cosθ instead of λ_C·(1-cosθ)",
    "wavelength_rounded":   "Uses λ_C = 0.0243 Å instead of 0.02426 Å",
    "frequency_shift":      "Applies formula to frequency instead of wavelength",
    "classical_prediction": "Uses Thomson scattering (no wavelength shift)",
}
