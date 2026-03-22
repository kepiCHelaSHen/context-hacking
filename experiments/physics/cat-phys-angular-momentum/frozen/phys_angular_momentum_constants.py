"""Angular Momentum — Frozen Constants. Source: Halliday 12th Ed Ch 11. DO NOT MODIFY."""
import math
# L = Iω for rotation, L = mvr sin(θ) for particle
# Conservation: if no external torque, L = const
# Test: figure skater, I1=4.0 kg·m², ω1=2.0 rad/s, pulls in to I2=1.0 kg·m²
I1_SKATER, OMEGA1_SKATER = 4.0, 2.0
I2_SKATER = 1.0
OMEGA2_SKATER = I1_SKATER * OMEGA1_SKATER / I2_SKATER  # = 8.0 rad/s
L_SKATER = I1_SKATER * OMEGA1_SKATER  # = 8.0 kg·m²/s (conserved)
# KE changes! KE1 = ½Iω² = 8J, KE2 = 32J — energy comes from work done pulling in
KE1 = 0.5 * I1_SKATER * OMEGA1_SKATER**2   # = 8.0 J
KE2 = 0.5 * I2_SKATER * OMEGA2_SKATER**2   # = 32.0 J
PRIOR_ERRORS = {
    "l_mvr_no_sin":     "Uses L=mvr without sin(θ) for non-perpendicular",
    "ke_conserved":      "Claims KE is conserved when I changes (only L is)",
    "omega_vs_v":        "Confuses ω (rad/s) with v (m/s) in L=Iω",
}
