"""
Thermodynamic Processes — Frozen Constants
Source: CODATA 2018, Zemansky & Dittman Heat & Thermodynamics 8th Ed
DO NOT MODIFY.
"""
import math

R = 8.314462618  # J/(mol·K)

# For ideal gas: PV = nRT
# Isothermal work: W = nRT·ln(V2/V1)
# Adiabatic: PV^γ = const, TV^(γ-1) = const
# Isobaric work: W = PΔV = nRΔT
# Isochoric work: W = 0

# γ values (Cp/Cv)
GAMMA_MONO = 5.0 / 3.0    # = 1.6667 (He, Ar, Ne)
GAMMA_DI = 7.0 / 5.0      # = 1.4000 (N2, O2 at room T)

# Test: 1 mol ideal gas, isothermal expansion 1L → 2L at 300K
N_TEST = 1.0
T_TEST = 300.0
V1_TEST = 0.001  # m³ = 1L
V2_TEST = 0.002  # m³ = 2L
W_ISOTHERMAL = N_TEST * R * T_TEST * math.log(V2_TEST / V1_TEST)  # = 1729.0 J
# LLM prior: uses ln(2) ≈ 0.7 → gets 1746 J (wrong R), or uses log10

# Adiabatic: T1*V1^(γ-1) = T2*V2^(γ-1)
# For diatomic gas, γ=1.4, V doubles:
T2_ADIABATIC_DI = T_TEST * (V1_TEST / V2_TEST) ** (GAMMA_DI - 1)  # = 227.4 K

PRIOR_ERRORS = {
    "work_sign":        "Wrong sign: work done BY gas is positive",
    "isothermal_log":   "Uses log10 instead of ln in isothermal work",
    "cv_cp_confusion":  "Uses Cv where Cp needed (or vice versa)",
    "adiabatic_gamma":  "Uses γ=1.4 for monatomic gas (should be 5/3)",
}
