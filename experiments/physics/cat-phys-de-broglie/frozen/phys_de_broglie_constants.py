"""
de Broglie Wavelength — Frozen Constants
Source: CODATA 2018, de Broglie (1924)
DO NOT MODIFY.
"""
import math

H_PLANCK = 6.62607015e-34    # J·s
M_ELECTRON = 9.1093837015e-31  # kg
M_PROTON = 1.67262192369e-27   # kg
E_CHARGE = 1.602176634e-19    # C
C_LIGHT = 299792458            # m/s

# de Broglie: λ = h/p = h/(mv) for non-relativistic
# For electron accelerated through V volts: KE = eV = ½mv²
# v = √(2eV/m), so λ = h/√(2meV)

# Test: electron at 100 eV
V_TEST = 100.0  # volts
KE_TEST = E_CHARGE * V_TEST  # = 1.602e-17 J
V_ELECTRON_100EV = math.sqrt(2 * KE_TEST / M_ELECTRON)  # = 5.931e6 m/s
LAMBDA_100EV = H_PLANCK / (M_ELECTRON * V_ELECTRON_100EV)  # = 1.226e-10 m = 1.226 Å
# LLM prior: uses relativistic formula for 100 eV (unnecessary, v/c = 0.02)

# At what KE is relativistic treatment needed? When v > 0.1c
# For electron: KE_relativistic_threshold ≈ 0.005 * m_e * c² ≈ 2.6 keV

PRIOR_ERRORS = {
    "classical_always":    "Uses λ=h/(mv) for relativistic particles",
    "wrong_ke_formula":    "Uses KE = mv² instead of ½mv²",
    "proton_same_lambda":  "Claims same-energy proton has same λ as electron (heavier = shorter λ)",
    "units_confusion":     "Mixes eV and Joules without conversion",
}
