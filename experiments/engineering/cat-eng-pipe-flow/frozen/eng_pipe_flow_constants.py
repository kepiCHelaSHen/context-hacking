"""Hagen-Poiseuille Laminar Pipe Flow — Frozen Constants. Source: Munson Fluid Mechanics 8th Ed. DO NOT MODIFY."""
import math

RHO_WATER = 998.0      # kg/m³ at 20°C
MU_WATER  = 1.0e-3     # Pa·s (dynamic viscosity of water at 20°C)
RE_CRIT   = 2300        # Reynolds number transition threshold

# Hagen-Poiseuille: Q = πΔPd⁴/(128μL) — ONLY valid for laminar flow (Re < 2300)
# Equivalently:     ΔP = 128μLQ/(πd⁴)
# Or:               ΔP = 32μLv/d²  (where v = Q/A = average velocity)

# --- Test case: water in a small pipe ---
MU_TEST  = 1.0e-3    # Pa·s
L_TEST   = 10.0      # m
D_TEST   = 0.02      # m diameter
Q_TEST   = 1.0e-5    # m³/s

A_TEST   = math.pi * D_TEST**2 / 4                        # 3.14159e-4 m²
V_TEST   = Q_TEST / A_TEST                                 # 0.03183 m/s
RE_TEST  = RHO_WATER * V_TEST * D_TEST / MU_TEST           # ≈ 635.3 → laminar ✓
DP_TEST  = 128 * MU_TEST * L_TEST * Q_TEST / (math.pi * D_TEST**4)  # ≈ 25.46 Pa

# Sanity: verify ΔP via velocity form
_DP_VEL  = 32 * MU_TEST * L_TEST * V_TEST / D_TEST**2
assert abs(DP_TEST - _DP_VEL) < 0.01, "flow-rate and velocity forms must agree"

PRIOR_ERRORS = {
    "hp_for_turbulent":    "Applies Hagen-Poiseuille in turbulent regime (Re>2300) — gives WRONG results",
    "diameter_not_radius":  "Uses r⁴ formula with diameter d (off by factor of 16)",
    "velocity_not_flow":    "Confuses volumetric flow rate Q with average velocity v in HP formula",
}
