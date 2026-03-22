"""RLC Resonance — Frozen Constants. Source: Horowitz & Hill 3rd Ed Ch 1, Irwin & Nelms 11th Ed Ch 14. DO NOT MODIFY."""
import math

# Resonance frequency: f0 = 1/(2*pi*sqrt(L*C)), omega0 = 1/sqrt(L*C)
# Q factor (series RLC): Q = (1/R)*sqrt(L/C) = omega0*L/R = 1/(omega0*R*C)
# Bandwidth: BW = f0/Q = R/(2*pi*L)
# At resonance: impedance is purely resistive — Z = R (series RLC)
# LLM prior: uses Q = R*sqrt(C/L) instead of (1/R)*sqrt(L/C) for series RLC

# Reference component values
R_REF = 10.0      # 10 Ohm
L_REF = 10e-3     # 10 mH
C_REF = 100e-6    # 100 uF

# Derived constants (frozen from reference values)
OMEGA0_REF = 1.0 / math.sqrt(L_REF * C_REF)                # 1000 rad/s
F0_REF     = OMEGA0_REF / (2.0 * math.pi)                   # 159.1549... Hz
Q_REF      = (1.0 / R_REF) * math.sqrt(L_REF / C_REF)      # 1.0
BW_REF     = F0_REF / Q_REF                                 # 159.1549... Hz
Z_AT_RES   = R_REF                                          # 10 Ohm

# Wrong Q (common LLM error: uses R instead of 1/R for series)
Q_WRONG_R  = R_REF * math.sqrt(C_REF / L_REF)              # 1.0 (coincidence for these values!)
# To expose error clearly, also test with R=50
R_ALT = 50.0
Q_ALT_CORRECT = (1.0 / R_ALT) * math.sqrt(L_REF / C_REF)  # 0.2
Q_ALT_WRONG   = R_ALT * math.sqrt(C_REF / L_REF)           # 5.0 — clearly different

PRIOR_ERRORS = {
    "q_r_not_1_over_r":  "Uses Q = R*sqrt(C/L) instead of (1/R)*sqrt(L/C) for series RLC",
    "bandwidth_wrong":   "Uses BW = f0*Q instead of f0/Q",
    "omega_vs_f":        "Confuses omega0 (rad/s) with f0 (Hz) — off by factor 2*pi",
}
