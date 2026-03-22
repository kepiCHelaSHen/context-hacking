"""RC Circuit — Frozen Constants. Source: Horowitz & Hill 3rd Ed Ch 1, IEEE. DO NOT MODIFY."""
import math

# Time constant: tau = RC
# Cutoff frequency: f_c = 1/(2*pi*R*C) — the 2*pi is CRITICAL!
# Angular cutoff:  omega_c = 1/(R*C) = 2*pi*f_c  (no 2*pi in angular form)
# LLM prior: omits 2*pi, giving f_c = 1/(RC) which is omega_c, not f_c

# Reference component values
R_REF = 1000.0       # 1 kOhm
C_REF = 1e-6         # 1 uF

# Derived constants (frozen from reference values)
TAU_REF = R_REF * C_REF                          # 1e-3 s = 1 ms
FC_REF  = 1.0 / (2.0 * math.pi * R_REF * C_REF) # 159.1549... Hz
WC_REF  = 1.0 / (R_REF * C_REF)                  # 1000 rad/s
FC_WRONG = 1.0 / (R_REF * C_REF)                 # 1000 Hz — WRONG (missing 2*pi)

# At cutoff: gain = 1/sqrt(2) ~ 0.7071 (-3 dB point)
GAIN_AT_CUTOFF = 1.0 / math.sqrt(2.0)            # 0.70710678...

# Charging:    V(t) = V0 * (1 - exp(-t/tau))
# Discharging: V(t) = V0 * exp(-t/tau)
# Test: V0=5V, t=tau => charging = 5*(1-1/e)=3.1606..., discharging = 5/e=1.8394...
V0_TEST = 5.0
V_CHARGE_AT_TAU   = V0_TEST * (1.0 - math.exp(-1.0))  # 3.16060...
V_DISCHARGE_AT_TAU = V0_TEST * math.exp(-1.0)          # 1.83939...

PRIOR_ERRORS = {
    "fc_no_2pi":            "Uses f_c = 1/(RC) instead of 1/(2*pi*RC) — off by factor 2*pi",
    "tau_wrong":            "Wrong R or C in tau calculation",
    "charge_discharge_swap": "Swaps charging and discharging equations",
}
