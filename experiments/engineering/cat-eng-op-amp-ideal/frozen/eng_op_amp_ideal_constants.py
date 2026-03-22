"""Ideal Op-Amp — Frozen Constants. Source: Sedra/Smith 8th Ed Ch 2. DO NOT MODIFY."""
# Ideal op-amp rules:
#   (1) V+ = V-  (virtual short / virtual ground in inverting config)
#   (2) I+ = I- = 0  (infinite input impedance)
#
# Inverting amplifier:   Vout = -(Rf/Rin) * Vin   (NEGATIVE gain!)
# Non-inverting amplifier: Vout = (1 + Rf/Rin) * Vin  (gain >= 1)
# Voltage follower:      Vout = Vin  (Rf=0, Rin=inf, gain=1)
# Difference amplifier (equal R): Vout = (Rf/Rin) * (V2 - V1)

# ── Test values ──────────────────────────────────────────────
RF = 10_000       # 10 kOhm
RIN = 2_000       # 2 kOhm
VIN = 1.0         # 1 V

# Inverting: Vout = -(Rf/Rin)*Vin = -(10000/2000)*1 = -5 V
INVERTING_GAIN = -(RF / RIN)                    # -5.0
INVERTING_VOUT = INVERTING_GAIN * VIN           # -5.0 V

# Non-inverting: Vout = (1 + Rf/Rin)*Vin = (1+5)*1 = 6 V
NONINVERTING_GAIN = 1 + (RF / RIN)              # 6.0
NONINVERTING_VOUT = NONINVERTING_GAIN * VIN     # 6.0 V

# Voltage follower: gain = 1
FOLLOWER_GAIN = 1.0
FOLLOWER_VOUT = VIN                             # 1.0 V

# Difference amplifier (equal R): Vout = (Rf/Rin)*(V2-V1)
V1_DIFF, V2_DIFF = 1.0, 3.0
DIFF_VOUT = (RF / RIN) * (V2_DIFF - V1_DIFF)   # 5.0*(3-1) = 10.0 V

PRIOR_ERRORS = {
    "inverting_positive":      "Forgets negative sign — uses Rf/Rin instead of -Rf/Rin",
    "noninverting_no_plus_1":  "Uses Rf/Rin instead of 1+Rf/Rin for non-inverting gain",
    "virtual_ground_wrong":    "Does not apply V+=V- (virtual short) at inverting input",
}
