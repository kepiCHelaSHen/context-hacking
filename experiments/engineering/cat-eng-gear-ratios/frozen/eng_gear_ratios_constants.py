"""Gear Train Analysis — Frozen Constants. Source: Shigley's Mechanical Engineering Design, 11th Ed. DO NOT MODIFY."""
import math

# Gear ratio: GR = N_driven / N_driver = omega_driver / omega_driven
# Speed:      omega_driven = omega_driver * (N_driver / N_driven)
# Torque:     tau_driven = tau_driver * GR  (ignoring friction losses)
# Direction:  each external mesh REVERSES rotation direction
#   - Even number of external meshes -> same direction as input
#   - Odd  number of external meshes -> reversed direction
# Compound gear train: total GR = product of individual stage ratios

# LLM priors:
#   1. "direction_same"   — forgets that an odd number of meshes reverses direction
#   2. "ratio_inverted"   — uses N_driver/N_driven for speed ratio (inverts GR)
#   3. "torque_decreases" — claims torque decreases with speed reduction (opposite is true)

# --- Simple gear pair: Driver N1=20 teeth at 1000 RPM -> Driven N2=60 teeth ---
N1 = 20          # driver teeth
N2 = 60          # driven teeth
OMEGA_IN = 1000.0  # RPM input speed

GR_SIMPLE = N2 / N1                       # 60/20 = 3.0 (speed reduction)
OMEGA_OUT = OMEGA_IN * (N1 / N2)          # 1000 * 20/60 = 333.333... RPM
TAU_IN_REF = 10.0                         # reference input torque (N*m)
TAU_OUT_SIMPLE = TAU_IN_REF * GR_SIMPLE   # 10 * 3 = 30.0 N*m (torque increases!)
N_MESHES_SIMPLE = 1                       # 1 external mesh -> reversed

# WRONG values — common LLM errors
GR_INVERTED = N1 / N2                     # 20/60 = 0.333... (wrong: using N_driver/N_driven)
OMEGA_OUT_WRONG = OMEGA_IN * (N2 / N1)    # 1000 * 60/20 = 3000 RPM (wrong: speed UP)
TAU_OUT_WRONG = TAU_IN_REF / GR_SIMPLE    # 10/3 = 3.333... N*m (wrong: torque "decreases")

# --- Compound gear train: N1=20->N2=40 (stage 1), N3=15->N4=45 (stage 2) ---
# N2 and N3 are on the same shaft
NC1_DRIVER = 20   # stage 1 driver
NC1_DRIVEN = 40   # stage 1 driven
NC2_DRIVER = 15   # stage 2 driver (same shaft as NC1_DRIVEN)
NC2_DRIVEN = 45   # stage 2 driven

GR_STAGE1 = NC1_DRIVEN / NC1_DRIVER      # 40/20 = 2.0
GR_STAGE2 = NC2_DRIVEN / NC2_DRIVER      # 45/15 = 3.0
GR_COMPOUND = GR_STAGE1 * GR_STAGE2      # 2 * 3 = 6.0
N_MESHES_COMPOUND = 2                     # 2 external meshes -> same direction

OMEGA_COMPOUND_OUT = OMEGA_IN / GR_COMPOUND  # 1000/6 = 166.666... RPM

PRIOR_ERRORS = {
    "direction_same":    "Forgets that meshing gears reverse direction; odd meshes -> reversed, even -> same",
    "ratio_inverted":    "Uses N_driver/N_driven for gear ratio instead of N_driven/N_driver",
    "torque_decreases":  "Claims torque decreases with speed reduction (actually torque INCREASES by GR)",
}
