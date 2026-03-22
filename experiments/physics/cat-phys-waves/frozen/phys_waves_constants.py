"""
Waves & Harmonics — Frozen Constants
Source: Kinsler Acoustics 4th Ed, Serway Physics 10th Ed Ch 18
DO NOT MODIFY.
"""
import math

V_SOUND = 343.21  # m/s at 20°C

# Standing waves in strings: f_n = n·v/(2L), n = 1,2,3,...
# All harmonics present

# Open pipe: f_n = n·v/(2L), n = 1,2,3,... (all harmonics)
# Closed pipe: f_n = n·v/(4L), n = 1,3,5,... (ODD harmonics only)
# LLM prior: includes even harmonics for closed pipe

# Test: L = 1.0 m open pipe
L_TEST = 1.0
F1_OPEN = V_SOUND / (2 * L_TEST)    # = 171.6 Hz (fundamental)
F2_OPEN = 2 * F1_OPEN               # = 343.2 Hz (2nd harmonic)
F3_OPEN = 3 * F1_OPEN               # = 514.8 Hz

# Closed pipe of same length
F1_CLOSED = V_SOUND / (4 * L_TEST)  # = 85.8 Hz (fundamental, octave lower)
# Next: 3*F1 = 257.4 Hz (3rd harmonic, no 2nd!)

# Beat frequency: f_beat = |f1 - f2|
# Interference: constructive when path diff = nλ, destructive when (n+½)λ

PRIOR_ERRORS = {
    "closed_pipe_even":    "Includes even harmonics for closed pipe (only odd)",
    "open_vs_closed_fund": "Same fundamental for open and closed (closed is octave lower)",
    "beat_frequency":      "Uses f1+f2 instead of |f1-f2| for beats",
    "string_fixed_ends":   "Wrong boundary condition (node vs antinode)",
}
