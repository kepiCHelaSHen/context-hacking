"""Planetary Equilibrium Temperature — Frozen Constants. Source: IAU / NASA Planetary Fact Sheets. DO NOT MODIFY."""
import math

# Stefan-Boltzmann constant (NIST CODATA 2018)
SIGMA = 5.6704e-8  # W m^-2 K^-4

# Solar luminosity (IAU 2015 nominal)
L_SUN = 3.828e26  # W

# ── Earth ─────────────────────────────────────────────────────────
D_EARTH = 1.496e11    # m — semi-major axis (1 AU)
A_EARTH = 0.306       # Bond albedo
T_ACTUAL_EARTH = 288  # K — observed global mean surface temperature

# Pre-computed Earth equilibrium temperature
# T_eq = (L*(1-A) / (16*pi*sigma*d^2))^(1/4)
T_EQ_EARTH = (L_SUN * (1 - A_EARTH) / (16 * math.pi * SIGMA * D_EARTH**2))**0.25
# = 254.0 K = -19 C  (NO atmosphere)

GREENHOUSE_EARTH = T_ACTUAL_EARTH - T_EQ_EARTH  # ~34 K

# ── Venus ─────────────────────────────────────────────────────────
D_VENUS = 1.082e11    # m
A_VENUS = 0.77        # Bond albedo (very reflective clouds)
T_ACTUAL_VENUS = 737  # K — surface temperature

T_EQ_VENUS = (L_SUN * (1 - A_VENUS) / (16 * math.pi * SIGMA * D_VENUS**2))**0.25
# ~226.6 K

GREENHOUSE_VENUS = T_ACTUAL_VENUS - T_EQ_VENUS  # ~510 K (massive!)

# ── Mars ──────────────────────────────────────────────────────────
D_MARS = 2.279e11     # m
A_MARS = 0.25         # Bond albedo
T_ACTUAL_MARS = 218   # K — surface temperature

T_EQ_MARS = (L_SUN * (1 - A_MARS) / (16 * math.pi * SIGMA * D_MARS**2))**0.25
# ~210 K

GREENHOUSE_MARS = T_ACTUAL_MARS - T_EQ_MARS  # ~8 K (thin atmosphere)

# ── Wrong-value traps (for testing LLM errors) ───────────────────
PRIOR_ERRORS = {
    "teq_is_surface":      "Claims equilibrium temperature IS the actual surface temperature; "
                           "T_eq ignores greenhouse effect — Earth T_eq=254K != 288K",
    "no_albedo":           "Forgets (1-A) factor; uses full stellar flux instead of absorbed fraction",
    "greenhouse_negative": "Claims greenhouse effect cools planets (T_actual < T_eq); "
                           "greenhouse always warms: T_actual >= T_eq for any atmosphere",
}
