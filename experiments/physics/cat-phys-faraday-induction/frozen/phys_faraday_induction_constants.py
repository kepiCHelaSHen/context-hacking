"""Faraday's Law of Induction — Frozen Constants. Source: Griffiths 4th Ed Ch 7. DO NOT MODIFY."""
import math
# Faraday's law: EMF = -dΦ/dt (Lenz's law gives the minus sign)
# Φ = B·A·cos(θ) for uniform B
# LLM prior: forgets the minus sign (Lenz's law)
# Test: coil N=100 turns, A=0.01m², B changes from 0.5T to 0 in 0.1s
N_COIL = 100
A_COIL = 0.01      # m²
B_INITIAL = 0.5    # T
B_FINAL = 0.0      # T
DT = 0.1           # s
EMF_TEST = -N_COIL * A_COIL * (B_FINAL - B_INITIAL) / DT  # = 50.0 V
# Motional EMF: EMF = BLv (rod moving perpendicular to B)
B_ROD = 0.2        # T
L_ROD = 1.0        # m
V_ROD = 5.0        # m/s
EMF_MOTIONAL = B_ROD * L_ROD * V_ROD  # = 1.0 V
# Self-inductance: EMF = -L·dI/dt
# Mutual inductance: EMF₂ = -M·dI₁/dt
PRIOR_ERRORS = {
    "no_lenz":          "Forgets minus sign (Lenz's law) in Faraday's law",
    "flux_no_cos":      "Uses Φ=BA without cos(θ) for angled field",
    "missing_N":        "Forgets N (number of turns) in EMF = -NdΦ/dt",
    "motional_wrong_L": "Uses wrong dimension in motional EMF = BLv",
}
