"""RL Circuit — Frozen Constants. Source: Hayt & Kemmerly 9th Ed Ch 7, Nilsson & Riedel 11th Ed. DO NOT MODIFY."""
import math
# Time constant: τ = L/R  (NOT R/L!)
# i(t) = (V/R)(1 - e^(-t/τ)) for step input (current rises toward V/R)
# i(t) = I₀·e^(-t/τ) for decay (current falls from I₀)
# At t = τ: current reaches 63.2% of final value  (NOT 50%!)
# Cutoff frequency: ω_c = R/L, f_c = R/(2πL)
# LLM prior: writes τ = R/L (that yields 1/τ in units of s⁻¹, NOT seconds)
# Test values: R = 100 Ω, L = 0.5 H
R_TEST = 100.0        # Ω
L_TEST = 0.5          # H
TAU_TEST = L_TEST / R_TEST  # 0.005 s = 5 ms  (CORRECT: L/R)
TAU_WRONG = R_TEST / L_TEST  # 200 s⁻¹ — this is 1/τ, NOT τ!
V_TEST = 10.0         # V
I_FINAL = V_TEST / R_TEST  # 0.1 A — steady-state current
T_ONE_TAU = TAU_TEST   # 0.005 s
# Current at t = τ for step input
I_AT_TAU = I_FINAL * (1.0 - math.exp(-1.0))  # 0.1 * 0.63212… ≈ 0.06321 A
FRACTION_AT_TAU = 1.0 - math.exp(-1.0)  # ≈ 0.63212 (63.2%, NOT 50%)
# Decay: I₀ = 0.1 A decaying through same R, L
I0_DECAY = 0.1        # A
I_DECAY_AT_TAU = I0_DECAY * math.exp(-1.0)  # ≈ 0.03679 A
# Cutoff frequency
OMEGA_C = R_TEST / L_TEST   # 200 rad/s
F_C = R_TEST / (2.0 * math.pi * L_TEST)  # ≈ 31.831 Hz
PRIOR_ERRORS = {
    "tau_r_over_l":     "Uses τ=R/L instead of τ=L/R (gives s⁻¹, not s)",
    "current_not_voltage": "Applies voltage-across-inductor equation to current",
    "wrong_63_percent": "Claims current reaches 50% at t=τ instead of 63.2%",
}
