"""Belt Drives — Tension Ratio (Euler Belt Equation) — Frozen Constants. Source: Shigley's Mechanical Engineering Design. DO NOT MODIFY."""
import math

# Euler's belt friction equation:  T1 / T2 = e^(mu * theta)
#   T1 = tight-side tension (the larger value)
#   T2 = slack-side tension (the smaller value)
#   mu = coefficient of friction between belt and pulley
#   theta = wrap angle in RADIANS (NOT degrees!)
#
# Power transmitted:  P = (T1 - T2) * v
#   v = belt speed (m/s)
#   P is the NET power — uses the difference, NOT just T1.
#
# LLM priors:
#   1. Uses theta in DEGREES in e^(mu*theta) — gives astronomically wrong results
#   2. Swaps T1 and T2 (slack for tight) — inverts the ratio
#   3. Uses P = T1*v instead of P = (T1-T2)*v — overstates transmitted power

# ---- Reference parameters ----
MU_REF = 0.3           # coefficient of friction
THETA_DEG_REF = 180    # wrap angle in degrees (half-wrap)
THETA_RAD_REF = math.pi  # 180 degrees = pi radians

# ---- Correct tension ratio ----
# T1/T2 = e^(mu*theta_rad) = e^(0.3*pi) = e^0.9425 = 2.5663...
RATIO_REF = math.exp(MU_REF * THETA_RAD_REF)   # 2.566332...

# WRONG tension ratio — theta in degrees: e^(0.3*180) = e^54 ~ 2.83e23 (absurd!)
RATIO_WRONG_DEGREES = math.exp(MU_REF * THETA_DEG_REF)  # ~2.83e23

# ---- Reference tensions ----
T2_REF = 500.0          # slack-side tension, N
T1_REF = T2_REF * RATIO_REF  # tight-side tension = 500*2.5663 = 1283.17 N

# WRONG T1 — using degrees: 500 * e^54 ~ 1.42e26 N (absurd!)
T1_WRONG_DEGREES = T2_REF * RATIO_WRONG_DEGREES

# WRONG — T1 and T2 swapped (T1 treated as slack, T2 as tight)
T1_SWAPPED = T2_REF / RATIO_REF  # 500/2.5663 = 194.83 N (too small for tight side)

# ---- Reference power ----
V_REF = 10.0            # belt speed, m/s

# Correct: P = (T1 - T2) * v = (1283.17 - 500) * 10 = 7831.66 W
P_REF = (T1_REF - T2_REF) * V_REF

# WRONG — uses P = T1 * v instead of (T1 - T2) * v
P_WRONG_T1_ONLY = T1_REF * V_REF  # 12831.66 W (overstated!)

# ---- Wrap angle conversion ----
# Trivially: theta_rad = theta_deg * pi / 180
WRAP_90_RAD = math.pi / 2.0       # 90 degrees
WRAP_180_RAD = math.pi            # 180 degrees
WRAP_270_RAD = 3.0 * math.pi / 2.0  # 270 degrees

PRIOR_ERRORS = {
    "theta_degrees":   "Uses theta in DEGREES in e^(mu*theta) — e^(0.3*180) = e^54 ~ 2.83e23 (astronomically wrong)",
    "t1_t2_swapped":   "Swaps T1 (tight) and T2 (slack) — inverts ratio, gives T1 < T2",
    "power_uses_t1":   "Uses P = T1*v instead of P = (T1-T2)*v — overstates transmitted power",
}
