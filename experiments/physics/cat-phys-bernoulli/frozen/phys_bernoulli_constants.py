"""Bernoulli's Equation — Frozen Constants. Source: Munson Fluid Mechanics 8th Ed. DO NOT MODIFY."""
import math
RHO_WATER = 998.2    # kg/m³ at 20°C
RHO_AIR = 1.225      # kg/m³ at sea level 15°C
G = 9.80665
# Bernoulli: P + ½ρv² + ρgh = const (along streamline, inviscid, incompressible)
# Continuity: A1*v1 = A2*v2
# Test: pipe narrows from A1=0.01m² to A2=0.005m², v1=2m/s, h=0
V1_TEST, A1_TEST, A2_TEST = 2.0, 0.01, 0.005
V2_TEST = V1_TEST * A1_TEST / A2_TEST  # = 4.0 m/s
# Pressure drop: ΔP = ½ρ(v2²-v1²) = ½(998.2)(16-4) = 5989.2 Pa
DP_TEST = 0.5 * RHO_WATER * (V2_TEST**2 - V1_TEST**2)  # = 5989.2 Pa
# Torricelli: v = √(2gh) for tank draining
V_TORRICELLI_1M = math.sqrt(2 * G * 1.0)  # = 4.429 m/s
PRIOR_ERRORS = {
    "missing_height":    "Forgets ρgh term in Bernoulli equation",
    "wrong_half_rho_v2": "Uses ρv² instead of ½ρv²",
    "compressible":      "Applies Bernoulli to compressible flow (invalid)",
    "viscous_flow":      "Applies Bernoulli to viscous pipe flow (need friction loss)",
}
