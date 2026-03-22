"""Stream Discharge (Manning's Equation) — Frozen Constants. Source: Chow, Open-Channel Hydraulics, 1959. DO NOT MODIFY."""
import math

# Manning's equation: v = (1/n) * R^(2/3) * S^(1/2)
# Q = v * A  (discharge = velocity x cross-sectional area)
# Hydraulic radius: R = A / P  where P = WETTED PERIMETER
# For rectangular channel: A = b*d, P = b + 2d (bottom + BOTH sides, NOT just bottom)
# KEY: R = bd/(b+2d) ≠ d (depth) and ≠ A/b (width)
# n has units s/m^(1/3) — Manning's roughness coefficient

# Test scenario: rectangular channel
B_CHANNEL = 5.0     # m — bottom width
D_CHANNEL = 2.0     # m — flow depth
N_MANNING = 0.03    # s/m^(1/3) — Manning's roughness (natural earth channel)
S_SLOPE = 0.001     # m/m — bed slope (dimensionless)

# Correct geometry
A_CHANNEL = B_CHANNEL * D_CHANNEL                    # = 10.0 m^2
P_WETTED = B_CHANNEL + 2 * D_CHANNEL                 # = 9.0 m  (NOT just 5.0!)
R_HYDRAULIC = A_CHANNEL / P_WETTED                    # = 10/9 = 1.1111 m

# Correct velocity and discharge
V_CORRECT = (1 / N_MANNING) * R_HYDRAULIC**(2/3) * S_SLOPE**0.5   # = 1.1308 m/s
Q_CORRECT = V_CORRECT * A_CHANNEL                                  # = 11.3079 m^3/s

# WRONG calculation: using depth as hydraulic radius (common LLM error)
R_WRONG_DEPTH = D_CHANNEL                                          # = 2.0 (WRONG!)
V_WRONG_DEPTH = (1 / N_MANNING) * R_WRONG_DEPTH**(2/3) * S_SLOPE**0.5  # = 1.6733 m/s
Q_WRONG_DEPTH = V_WRONG_DEPTH * A_CHANNEL                              # = 16.7327 m^3/s
ERROR_PERCENT_DEPTH = (Q_WRONG_DEPTH - Q_CORRECT) / Q_CORRECT * 100    # ≈ 48.0% too high!

# WRONG calculation: wetted perimeter = bottom only (no sides)
P_WRONG_NO_SIDES = B_CHANNEL                                       # = 5.0 (WRONG!)
R_WRONG_NO_SIDES = A_CHANNEL / P_WRONG_NO_SIDES                    # = 2.0 (same as depth error)

PRIOR_ERRORS = {
    "r_equals_depth":           "Uses R=d (depth) instead of R=A/P — inflates Q by ~48%",
    "wetted_perimeter_no_sides": "P=b only, omitting both sides — P should be b+2d",
    "manning_n_wrong_units":    "Treats n as dimensionless; n actually has units s/m^(1/3)",
}
