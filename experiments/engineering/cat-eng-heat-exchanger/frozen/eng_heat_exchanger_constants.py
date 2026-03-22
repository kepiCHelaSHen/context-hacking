"""LMTD Method — Heat Exchanger Design — Frozen Constants. Source: Incropera Fundamentals of Heat and Mass Transfer 8th Ed. DO NOT MODIFY."""
import math

# Q = U * A * LMTD
# LMTD = (ΔT₁ - ΔT₂) / ln(ΔT₁ / ΔT₂)
# Counter-flow: ΔT₁ = T_h,in - T_c,out ;  ΔT₂ = T_h,out - T_c,in   (CROSSED endpoints)
# Parallel-flow: ΔT₁ = T_h,in - T_c,in ;  ΔT₂ = T_h,out - T_c,out  (SAME-SIDE endpoints)

# Test case temperatures (°C)
TH_IN  = 90.0
TH_OUT = 60.0
TC_IN  = 30.0
TC_OUT = 50.0

# Counter-flow deltas
DT1_COUNTER = TH_IN - TC_OUT    # 90 - 50 = 40 °C
DT2_COUNTER = TH_OUT - TC_IN    # 60 - 30 = 30 °C

# Parallel-flow deltas
DT1_PARALLEL = TH_IN - TC_IN    # 90 - 30 = 60 °C
DT2_PARALLEL = TH_OUT - TC_OUT  # 60 - 50 = 10 °C

# LMTD values
LMTD_COUNTER  = (DT1_COUNTER - DT2_COUNTER) / math.log(DT1_COUNTER / DT2_COUNTER)
# = (40 - 30) / ln(40/30) = 10 / 0.28768 = 34.76 °C
LMTD_PARALLEL = (DT1_PARALLEL - DT2_PARALLEL) / math.log(DT1_PARALLEL / DT2_PARALLEL)
# = (60 - 10) / ln(60/10) = 50 / 1.79176 = 27.90 °C

# Counter-flow LMTD > parallel-flow LMTD — always true
assert LMTD_COUNTER > LMTD_PARALLEL

# Test heat-transfer calc: U = 500 W/(m²·K), A = 2 m²
U_TEST = 500.0   # W/(m²·K)
A_TEST = 2.0     # m²
Q_COUNTER_TEST  = U_TEST * A_TEST * LMTD_COUNTER   # = 34760.7 W
Q_PARALLEL_TEST = U_TEST * A_TEST * LMTD_PARALLEL  # = 27903.1 W

PRIOR_ERRORS = {
    "counter_parallel_swap":  "Uses parallel-flow ΔT assignments for counter-flow (pairs hot-in with cold-in)",
    "lmtd_arithmetic_mean":   "Uses arithmetic mean (ΔT₁+ΔT₂)/2 instead of log-mean (ΔT₁-ΔT₂)/ln(ΔT₁/ΔT₂)",
    "wrong_endpoint_pairing": "Pairs hot-in with cold-in for counter-flow instead of hot-in with cold-out",
}
