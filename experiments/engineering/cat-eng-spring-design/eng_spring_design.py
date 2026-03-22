"""Helical Spring — Wahl Correction Factor — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_spring_design_constants import *


def spring_index(D, d):
    """Spring index C = D/d (mean coil diameter / wire diameter). Typical range 4-12."""
    return D / d


def wahl_factor(C):
    """Wahl correction factor: K_W = (4C-1)/(4C-4) + 0.615/C.  Always > 1."""
    return (4 * C - 1) / (4 * C - 4) + 0.615 / C


def basic_shear_stress(F, D, d):
    """Basic (uncorrected) shear stress: tau = 8FD / (pi * d^3). Underestimates!"""
    return 8 * F * D / (math.pi * d**3)


def corrected_shear_stress(F, D, d):
    """Corrected shear stress with Wahl factor: tau = K_W * 8FD / (pi * d^3)."""
    C = spring_index(D, d)
    K_W = wahl_factor(C)
    return K_W * basic_shear_stress(F, D, d)


def spring_rate(G, d, D, N):
    """Spring rate: k = G*d^4 / (8*D^3*N). G=shear modulus, N=active coils."""
    return G * d**4 / (8 * D**3 * N)


if __name__ == "__main__":
    F, D, d = 100.0, 0.030, 0.005
    C = spring_index(D, d)
    K_W = wahl_factor(C)
    tau_b = basic_shear_stress(F, D, d)
    tau_c = corrected_shear_stress(F, D, d)
    print(f"Spring index C = {C:.1f}")
    print(f"Wahl factor K_W = {K_W:.4f}")
    print(f"Basic shear stress    = {tau_b/1e6:.4f} MPa (UNDERESTIMATES!)")
    print(f"Corrected shear stress = {tau_c/1e6:.4f} MPa ({(K_W-1)*100:.1f}% higher)")

    G, N = 79.3e9, 10
    k = spring_rate(G, d, D, N)
    print(f"Spring rate k = {k:.2f} N/m = {k/1e3:.4f} kN/m")
