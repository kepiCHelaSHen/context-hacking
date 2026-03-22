"""Helical Spring Wahl Correction — Frozen Constants. Source: Shigley's Mechanical Engineering Design. DO NOT MODIFY."""
import math

# Helical compression spring shear stress
#   Basic (uncorrected): tau = 8*F*D / (pi * d^3)
#   Wahl correction factor: K_W = (4C-1)/(4C-4) + 0.615/C  where C = D/d
#   Corrected: tau = K_W * 8*F*D / (pi * d^3)
#
# Spring index C = D/d  (mean coil diameter / wire diameter), typical range 4-12
# Spring rate:  k = G*d^4 / (8*D^3*N)  where G=shear modulus, N=active coils
#
# LLM priors:
#   1. "no_wahl_correction" — Uses basic tau = 8FD/(pi*d^3) without K_W → underestimates stress
#   2. "c_inverted" — Computes C = d/D instead of D/d → Wahl factor wildly wrong
#   3. "spring_rate_wrong" — Wrong power on d or D in spring rate formula

# Reference spring: F=100N, D=30mm, d=5mm
F_REF = 100.0       # N
D_REF = 0.030       # m (mean coil diameter)
D_WIRE_REF = 0.005  # m (wire diameter)

# Spring index C = D/d
C_REF = D_REF / D_WIRE_REF                                  # 6.0

# WRONG — inverted C (common LLM error)
C_WRONG_INVERTED = D_WIRE_REF / D_REF                       # 0.16667

# Wahl correction factor
K_W_REF = (4 * C_REF - 1) / (4 * C_REF - 4) + 0.615 / C_REF  # 1.2525

# WRONG — Wahl factor from inverted C
K_W_WRONG_INVERTED = (4 * C_WRONG_INVERTED - 1) / (4 * C_WRONG_INVERTED - 4) + 0.615 / C_WRONG_INVERTED  # ~3.79

# Basic shear stress (uncorrected)
TAU_BASIC_REF = 8 * F_REF * D_REF / (math.pi * D_WIRE_REF**3)  # ~61.115 MPa

# Corrected shear stress (with Wahl factor)
TAU_CORRECTED_REF = K_W_REF * TAU_BASIC_REF                     # ~76.547 MPa

# Spring rate reference: G=79.3 GPa (steel), N=10 active coils
G_REF = 79.3e9      # Pa (steel shear modulus)
N_COILS_REF = 10     # active coils
K_RATE_REF = G_REF * D_WIRE_REF**4 / (8 * D_REF**3 * N_COILS_REF)  # ~22945.6 N/m

# WRONG spring rate — d^3 instead of d^4
K_RATE_WRONG_D3 = G_REF * D_WIRE_REF**3 / (8 * D_REF**3 * N_COILS_REF)  # ~4589120 N/m (200x too large!)

# WRONG spring rate — D^2 instead of D^3
K_RATE_WRONG_D2 = G_REF * D_WIRE_REF**4 / (8 * D_REF**2 * N_COILS_REF)  # ~688 N/m (30x too small!)

PRIOR_ERRORS = {
    "no_wahl_correction":  "Uses basic tau = 8FD/(pi*d^3) without Wahl factor K_W — underestimates stress by 10-50%",
    "c_inverted":          "Computes C = d/D instead of D/d — Wahl factor becomes wildly wrong (~3.79 instead of ~1.25)",
    "spring_rate_wrong":   "Wrong power on d or D in spring rate k = Gd^4/(8D^3N) — e.g. d^3 or D^2",
}
