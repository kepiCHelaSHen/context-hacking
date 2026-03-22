"""
Hohmann Transfer Orbit — Frozen Constants
Source: NASA JPL, IAU 2012 nominal constants
DO NOT MODIFY.
"""
import math

# Gravitational parameter of the Sun: mu = GM_sun
MU_SUN = 1.327124400e20  # m^3/s^2  (IAU 2012 nominal)

# Orbital radii
R_EARTH = 1.496e11   # m  (1 AU, Earth mean orbital radius)
R_MARS  = 2.279e11   # m  (1.524 AU, Mars mean orbital radius)

# --- Transfer orbit semi-major axis: a_t = (r1 + r2) / 2 ---
A_TRANSFER = (R_EARTH + R_MARS) / 2  # 1.8875e11 m

# --- Circular velocities ---
V_CIRC_EARTH = math.sqrt(MU_SUN / R_EARTH)   # 29784.48 m/s ~ 29.78 km/s
V_CIRC_MARS  = math.sqrt(MU_SUN / R_MARS)    # 24131.46 m/s ~ 24.13 km/s

# --- Transfer orbit velocities (vis-viva: v = sqrt(mu*(2/r - 1/a_t))) ---
V_TRANSFER_DEPARTURE = math.sqrt(MU_SUN * (2 / R_EARTH - 1 / A_TRANSFER))
# = 32727.94 m/s ~ 32.73 km/s

V_TRANSFER_ARRIVAL = math.sqrt(MU_SUN * (2 / R_MARS - 1 / A_TRANSFER))
# = 21483.55 m/s ~ 21.48 km/s

# --- Delta-v burns ---
# Departure burn: speed up from circular Earth orbit to transfer orbit at r1
DV1 = V_TRANSFER_DEPARTURE - V_CIRC_EARTH  # 2943.46 m/s ~ 2.94 km/s

# Arrival burn: speed up from transfer orbit to circular Mars orbit at r2
DV2 = V_CIRC_MARS - V_TRANSFER_ARRIVAL     # 2647.92 m/s ~ 2.65 km/s

# Total delta-v: BOTH burns needed (common LLM error: forgets second burn)
TOTAL_DV = abs(DV1) + abs(DV2)             # 5591.38 m/s ~ 5.59 km/s

# --- Transfer time: half the transfer orbit period ---
# T_transfer = pi * sqrt(a_t^3 / mu)  (NOT the full period!)
T_TRANSFER = math.pi * math.sqrt(A_TRANSFER**3 / MU_SUN)
# = 22362713.31 s ~ 258.83 days

# Full orbit period (for error detection — LLMs sometimes use this instead)
T_FULL_ORBIT = 2 * math.pi * math.sqrt(A_TRANSFER**3 / MU_SUN)
# = 44725426.62 s ~ 517.66 days (WRONG if used as transfer time)

PRIOR_ERRORS = {
    "single_burn":           "Computes only dv1 (departure), forgets dv2 (arrival circularization burn)",
    "transfer_time_wrong":   "Uses full orbit period (2*pi*sqrt(a^3/mu)) instead of half period (pi*sqrt(a^3/mu))",
    "delta_v_wrong_formula": "Wrong vis-viva application: uses sqrt(mu/r) instead of sqrt(mu*(2/r-1/a)) for transfer orbit velocity",
}
