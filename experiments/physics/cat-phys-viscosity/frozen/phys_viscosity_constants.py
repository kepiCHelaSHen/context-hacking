"""Viscosity & Stokes Drag — Frozen Constants. Source: CRC 103rd Ed, Munson 8th Ed. DO NOT MODIFY."""
import math
# Dynamic viscosity (Pa·s) at 20°C
MU_WATER = 1.002e-3   # Pa·s
MU_AIR = 1.825e-5     # Pa·s
MU_GLYCEROL = 1.412   # Pa·s
RHO_WATER = 998.2     # kg/m³
G = 9.80665
# Stokes drag: F = 6πμrv (sphere, low Re)
# LLM prior: uses diameter instead of radius
# Terminal velocity: v_t = 2r²(ρ_sphere-ρ_fluid)g / (9μ)
# Test: steel sphere r=1mm in water, ρ_steel=7800
R_TEST = 0.001  # m
RHO_STEEL = 7800.0
V_TERMINAL = 2 * R_TEST**2 * (RHO_STEEL - RHO_WATER) * G / (9 * MU_WATER)  # = 14.79 m/s
# Reynolds number: Re = ρvd/μ (uses DIAMETER not radius)
RE_TEST = RHO_WATER * V_TERMINAL * (2*R_TEST) / MU_WATER  # high Re — Stokes invalid!
PRIOR_ERRORS = {
    "diameter_not_radius": "Uses diameter in Stokes drag (F=6πμdv instead of 6πμrv)",
    "re_uses_radius":      "Uses radius in Reynolds number (should be diameter or length)",
    "stokes_high_re":      "Applies Stokes drag at high Re (only valid Re < 1)",
}
