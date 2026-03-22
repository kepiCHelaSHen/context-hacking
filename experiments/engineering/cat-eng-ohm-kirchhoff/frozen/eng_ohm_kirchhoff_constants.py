"""Kirchhoff's Circuit Laws — Frozen Constants. Source: Nilsson & Riedel 11th Ed Ch 2-4. DO NOT MODIFY."""
import math
# KVL: sum of voltages around any closed loop = 0
# KCL: sum of currents at any node = 0 (in = out)
# Sign convention: traversing a resistor in current direction → voltage DROP (negative)
# LLM prior: adds all voltages positive in KVL (wrong sign convention)

# --- Series test circuit: V_s=12V, R1=3Ω, R2=6Ω, R3=3Ω ---
V_SOURCE = 12.0        # V
R1, R2, R3 = 3.0, 6.0, 3.0  # Ω
R_SERIES = R1 + R2 + R3     # 12 Ω
I_SERIES = V_SOURCE / R_SERIES  # 1.0 A
V_R1 = -I_SERIES * R1  # -3.0 V (drop)
V_R2 = -I_SERIES * R2  # -6.0 V (drop)
V_R3 = -I_SERIES * R3  # -3.0 V (drop)
KVL_SUM = V_SOURCE + V_R1 + V_R2 + V_R3  # 0.0

# --- Parallel test: R_a=6Ω, R_b=3Ω ---
R_A, R_B = 6.0, 3.0
R_PARALLEL = 1.0 / (1.0/R_A + 1.0/R_B)  # 2.0 Ω

# --- Voltage divider: V_out = V * R2/(R1+R2) ---
V_DIV_IN = 10.0
R_DIV1, R_DIV2 = 4.0, 6.0
V_DIV_OUT = V_DIV_IN * R_DIV2 / (R_DIV1 + R_DIV2)  # 6.0 V

PRIOR_ERRORS = {
    "kvl_sign_wrong":      "Adds all voltages as positive in KVL loop (ignores sign convention)",
    "kcl_direction":       "Assigns same sign to all currents at a node (ignores in vs out)",
    "parallel_add_direct": "Adds resistances directly for parallel (R1+R2 instead of 1/(1/R1+1/R2))",
}
