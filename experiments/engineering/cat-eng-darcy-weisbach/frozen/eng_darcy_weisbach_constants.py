"""Darcy-Weisbach Pipe Friction — Frozen Constants. Source: Moody (1944), Colebrook (1939), White Fluid Mechanics. DO NOT MODIFY."""

# Darcy-Weisbach equation:  h_f = f_D * (L/D) * (v^2 / (2*g))
#   f_D = Darcy friction factor  (sometimes called Moody friction factor)
#   f_F = Fanning friction factor = f_D / 4  (4x SMALLER!)
#
# KEY TRAP: Many references (especially chemical engineering) use Fanning.
#   Plugging f_F into the Darcy-Weisbach equation gives a result 4x too small!
#
# Laminar flow (Re < 2300):
#   f_D = 64 / Re   (Darcy)
#   f_F = 16 / Re   (Fanning)
#
# LLM priors:
#   1. Uses Fanning f in Darcy equation — 4x error
#   2. Uses 32/Re or other wrong formula for laminar f
#   3. Wrong g value or unit mismatch in head loss

# Reference test conditions (laminar flow)
RE_REF = 1000.0       # Reynolds number (laminar: Re < 2300)
L_REF = 10.0          # pipe length, m
D_PIPE_REF = 0.05     # pipe diameter, m
V_REF = 1.0           # flow velocity, m/s
G_REF = 9.81          # gravitational acceleration, m/s^2

# Darcy friction factor (laminar): f_D = 64/Re
FD_REF = 64.0 / RE_REF                              # 0.064

# Fanning friction factor (laminar): f_F = 16/Re = f_D/4
FF_REF = 16.0 / RE_REF                              # 0.016

# Velocity head: v^2 / (2g)
VEL_HEAD_REF = V_REF**2 / (2.0 * G_REF)             # 0.050968...

# Correct head loss using Darcy: h_f = f_D * (L/D) * (v^2/(2g))
HF_DARCY_REF = FD_REF * (L_REF / D_PIPE_REF) * VEL_HEAD_REF  # 0.65239...

# WRONG head loss: Fanning f plugged into Darcy equation (4x too small!)
HF_FANNING_WRONG = FF_REF * (L_REF / D_PIPE_REF) * VEL_HEAD_REF  # 0.16310...

# Other wrong values for catching LLM mistakes
FD_WRONG_32 = 32.0 / RE_REF                         # 0.032 — wrong formula
FD_WRONG_128 = 128.0 / RE_REF                       # 0.128 — wrong formula

PRIOR_ERRORS = {
    "darcy_fanning_swap":  "Uses Fanning f (16/Re) in Darcy-Weisbach equation — head loss 4x too small",
    "laminar_f_wrong":     "Uses 32/Re or other incorrect formula for laminar friction factor",
    "head_loss_units":     "Wrong g value (e.g. 32.2 ft/s^2 in SI problem) or unit mismatch",
}
