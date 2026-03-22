"""Heat Transfer — Frozen Constants. Source: Incropera 8th Ed, CRC 103rd Ed. DO NOT MODIFY."""
import math
STEFAN_BOLTZMANN = 5.670374419e-8  # W/(m²·K⁴)
# Conduction: q = kA(T1-T2)/L (Fourier's law)
K_COPPER = 401.0    # W/(m·K)
K_ALUMINUM = 237.0
K_STEEL = 50.2
K_GLASS = 1.05
K_WOOD = 0.15
K_AIR = 0.0262     # at 300K
# Radiation: q = εσA(T⁴-T_surr⁴) — T must be in KELVIN, T⁴ not T
# LLM prior: uses T not T⁴, or uses Celsius
# Test: 1m² black surface at 500K, surroundings at 300K
Q_RAD_TEST = STEFAN_BOLTZMANN * 1.0 * (500**4 - 300**4)  # = 3087.2 W
# Newton's cooling: q = hA(T_s - T_inf)
H_NATURAL_CONV = 10.0   # W/(m²·K) typical natural convection
H_FORCED_CONV = 100.0   # W/(m²·K) typical forced convection
PRIOR_ERRORS = {
    "radiation_T_not_T4": "Uses T instead of T⁴ in Stefan-Boltzmann radiation",
    "radiation_celsius":  "Uses T in °C instead of K for radiation",
    "conduction_no_area": "Forgets area A in Fourier's law",
    "k_values_swapped":   "Swaps thermal conductivity values between materials",
}
