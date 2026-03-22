"""Stress-Strain — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_stress_strain_constants import *


def engineering_stress(F, A0):
    """Return engineering stress sigma_eng = F / A0 in Pa."""
    return F / A0


def engineering_strain(dL, L0):
    """Return engineering strain eps_eng = dL / L0 (dimensionless)."""
    return dL / L0


def true_stress(sigma_eng, eps_eng):
    """Return true stress sigma_true = sigma_eng * (1 + eps_eng) in Pa.

    Valid for uniform deformation (before necking).
    True stress > engineering stress because the actual area decreases under tension.
    """
    return sigma_eng * (1.0 + eps_eng)


def true_strain(eps_eng):
    """Return true strain eps_true = ln(1 + eps_eng).

    NOT equal to engineering strain!  True strain is the integral of
    infinitesimal strain increments: eps_true = integral(dL/L) = ln(L/L0).
    """
    return math.log(1.0 + eps_eng)


def youngs_modulus(sigma, epsilon):
    """Return Young's modulus E = sigma / epsilon in Pa.

    Only valid in the linear elastic region!
    """
    return sigma / epsilon


if __name__ == "__main__":
    F, A0 = 50000.0, 1e-4     # 50 kN, 100 mm^2
    dL, L0 = 0.5e-3, 0.1      # 0.5 mm, 100 mm

    sig_e = engineering_stress(F, A0)
    eps_e = engineering_strain(dL, L0)
    sig_t = true_stress(sig_e, eps_e)
    eps_t = true_strain(eps_e)
    E = youngs_modulus(sig_e, eps_e)

    print(f"Engineering stress = {sig_e/1e6:.1f} MPa")
    print(f"Engineering strain = {eps_e:.6f}")
    print(f"True stress        = {sig_t/1e6:.1f} MPa  (NOT {sig_e/1e6:.1f} MPa!)")
    print(f"True strain        = {eps_t:.6f}  (NOT {eps_e:.6f}!)")
    print(f"Young's modulus    = {E/1e9:.1f} GPa")
