"""
Reynolds Number — CHP Engineering Sprint
Flow regime classification: Re = ρvD/μ = vD/ν.
D must be DIAMETER (not radius!) for pipe flow.
All constants from frozen spec.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_reynolds_number_constants import (
    WATER_RHO, WATER_MU, WATER_NU,
    RE_LAMINAR, RE_TURBULENT,
    TEST_VELOCITY, TEST_DIAMETER,
)


def reynolds_number(rho, v, D, mu):
    """Re = ρvD/μ.  D = DIAMETER, not radius."""
    return rho * v * D / mu


def reynolds_kinematic(v, D, nu):
    """Re = vD/ν where ν = μ/ρ is kinematic viscosity (m²/s)."""
    return v * D / nu


def flow_regime(Re):
    """Classify flow: laminar (Re<2300), transition (2300-4000), turbulent (Re>4000)."""
    if Re < RE_LAMINAR:
        return "laminar"
    elif Re <= RE_TURBULENT:
        return "transition"
    else:
        return "turbulent"


def hydraulic_diameter(A, P):
    """Dh = 4A/P for non-circular cross-sections.
    A = cross-sectional area, P = wetted perimeter.
    For circular pipe: A=πD²/4, P=πD → Dh = D (sanity check).
    """
    return 4.0 * A / P


if __name__ == "__main__":
    import math

    print("=== Reynolds Number ===\n")

    # Standard test case: water in pipe
    Re = reynolds_number(WATER_RHO, TEST_VELOCITY, TEST_DIAMETER, WATER_MU)
    print(f"Pipe flow: Re = {Re:.1f}  ({flow_regime(Re)})")
    print(f"  rho={WATER_RHO} kg/m^3, v={TEST_VELOCITY} m/s, D={TEST_DIAMETER} m, mu={WATER_MU} Pa.s")

    # Same via kinematic viscosity
    Re_kin = reynolds_kinematic(TEST_VELOCITY, TEST_DIAMETER, WATER_NU)
    print(f"Via kinematic: Re = {Re_kin:.1f}  (should ~ {Re:.1f})")

    # Common error: using radius
    Re_wrong = reynolds_number(WATER_RHO, TEST_VELOCITY, TEST_DIAMETER / 2, WATER_MU)
    print(f"\nERROR demo (radius): Re = {Re_wrong:.1f}  (half the correct value!)")

    # Hydraulic diameter for circular pipe (sanity check)
    A_circ = math.pi * TEST_DIAMETER**2 / 4
    P_circ = math.pi * TEST_DIAMETER
    Dh = hydraulic_diameter(A_circ, P_circ)
    print(f"\nHydraulic diameter (circular): Dh = {Dh:.4f} m  (should = D = {TEST_DIAMETER})")

    # Hydraulic diameter for square duct (side = 0.05 m)
    side = 0.05
    Dh_sq = hydraulic_diameter(side**2, 4 * side)
    print(f"Hydraulic diameter (square 50mm): Dh = {Dh_sq:.4f} m  (should = side = {side})")
