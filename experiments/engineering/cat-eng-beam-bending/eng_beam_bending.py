"""Euler-Bernoulli Beam Bending — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_beam_bending_constants import *


def rect_I(b, h):
    """Second moment of area for rectangular cross-section: I = b*h^3/12."""
    return b * h**3 / 12.0


def circular_I(d):
    """Second moment of area for circular cross-section: I = pi*d^4/64 (NOT polar J)."""
    return math.pi * d**4 / 64.0


def bending_stress(M, y, I):
    """Bending stress sigma = M*y/I (Euler-Bernoulli)."""
    return M * y / I


def simply_supported_deflection(P, L, E, I):
    """Max deflection of simply-supported beam with center point load: delta = P*L^3/(48*E*I)."""
    return P * L**3 / (48.0 * E * I)


if __name__ == "__main__":
    b, h = 0.05, 0.1  # 50 mm x 100 mm rectangular beam
    I_rect = rect_I(b, h)
    print(f"Rectangular I = {I_rect:.6e} m^4  (NOT {b*h**2/12:.6e})")

    d = 0.1  # 100 mm diameter
    I_circ = circular_I(d)
    print(f"Circular I = {I_circ:.6e} m^4  (NOT J = {math.pi*d**4/32:.6e})")

    P, L, E = 1000.0, 2.0, 200e9
    M_max = P * L / 4.0
    y_max = h / 2.0
    sigma = bending_stress(M_max, y_max, I_rect)
    print(f"Max bending stress = {sigma/1e6:.2f} MPa")

    delta = simply_supported_deflection(P, L, E, I_rect)
    print(f"Max deflection = {delta*1000:.4f} mm")
