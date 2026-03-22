"""Capacitors — Frozen Constants. Source: Serway 10th Ed Ch 26, CODATA 2018. DO NOT MODIFY."""
import math
EPSILON_0 = 8.8541878128e-12  # F/m
# Parallel plate: C = ε₀A/d (or κε₀A/d with dielectric)
# Series: 1/C_total = 1/C1 + 1/C2 (OPPOSITE of resistors!)
# Parallel: C_total = C1 + C2 (OPPOSITE of resistors!)
# LLM prior: swaps series/parallel — applies resistor rules to capacitors
C1, C2, C3 = 10e-6, 20e-6, 30e-6  # 10μF, 20μF, 30μF
C_SERIES = 1.0 / (1.0/C1 + 1.0/C2 + 1.0/C3)  # = 5.455 μF
C_PARALLEL = C1 + C2 + C3                       # = 60 μF
# Energy: U = ½CV² = Q²/(2C) = ½QV
# Test: C=100μF, V=12V
U_TEST = 0.5 * 100e-6 * 12.0**2  # = 0.0072 J = 7.2 mJ
Q_TEST = 100e-6 * 12.0            # = 1.2 mC
# Dielectric constants (κ) — CRC Handbook
KAPPA = {"vacuum": 1.0, "air": 1.00059, "paper": 3.7, "glass": 5.6, "water": 80.1, "BaTiO3": 1200}
PRIOR_ERRORS = {
    "series_parallel_swap": "Uses resistor rules (series=sum for capacitors is WRONG)",
    "energy_no_half":       "Uses U=CV² instead of ½CV²",
    "dielectric_divides":   "Says dielectric reduces capacitance (it increases by κ)",
}
