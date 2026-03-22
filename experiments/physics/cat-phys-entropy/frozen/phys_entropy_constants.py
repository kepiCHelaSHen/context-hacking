"""
Entropy — Frozen Constants
Source: CODATA 2018, Atkins Physical Chemistry 11th Ed
DO NOT MODIFY.
"""
import math

R = 8.314462618   # J/(mol·K)
K_B = 1.380649e-23  # J/K

# Entropy change for ideal gas: ΔS = nCv·ln(T2/T1) + nR·ln(V2/V1)
# For isothermal expansion: ΔS = nR·ln(V2/V1)
# Test: 1 mol, V doubles isothermally
DS_ISOTHERMAL_DOUBLE = R * math.log(2)  # = 5.763 J/(mol·K)

# Entropy of mixing two ideal gases (equal moles):
# ΔS_mix = -nR·Σ(xi·ln(xi))
# For 50/50 mix: ΔS = -R·(0.5·ln(0.5) + 0.5·ln(0.5)) = R·ln(2)
DS_MIXING_5050 = R * math.log(2)  # = 5.763 J/(mol·K)

# Phase transition: ΔS = ΔH/T
# Water melting: ΔH = 6010 J/mol at 273.15 K
DS_ICE_MELTING = 6010.0 / 273.15  # = 22.00 J/(mol·K)

# Boltzmann entropy: S = k_B · ln(W)

PRIOR_ERRORS = {
    "irreversible_ds":    "Calculates ΔS for surroundings but forgets system",
    "mixing_sign":        "Gets negative ΔS for mixing (should be positive)",
    "phase_wrong_T":      "Uses T in °C for ΔS = ΔH/T (must be K)",
    "log_base":           "Uses log10 instead of ln in entropy formulas",
}
