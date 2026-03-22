"""Mohr's Circle — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_mohr_circle_constants import *


def mohr_center(sx, sy):
    """Return the center of Mohr's circle: C = (σ_x + σ_y) / 2."""
    return (sx + sy) / 2.0


def mohr_radius(sx, sy, txy):
    """Return the radius of Mohr's circle: R = √(((σ_x - σ_y)/2)² + τ_xy²)."""
    return math.sqrt(((sx - sy) / 2.0) ** 2 + txy ** 2)


def principal_stresses(sx, sy, txy):
    """Return (σ₁, σ₂) where σ₁ = C+R (max) and σ₂ = C-R (min)."""
    c = mohr_center(sx, sy)
    r = mohr_radius(sx, sy, txy)
    return (c + r, c - r)


def max_shear(sx, sy, txy):
    """Return maximum shear stress: τ_max = R."""
    return mohr_radius(sx, sy, txy)


def principal_angle_deg(sx, sy, txy):
    """Return principal angle θ_p in degrees: (1/2) * arctan(2*τ_xy / (σ_x - σ_y))."""
    return math.degrees(0.5 * math.atan2(2.0 * txy, sx - sy))


if __name__ == "__main__":
    sx, sy, txy = 80.0, 40.0, 30.0
    c = mohr_center(sx, sy)
    r = mohr_radius(sx, sy, txy)
    s1, s2 = principal_stresses(sx, sy, txy)
    ts = max_shear(sx, sy, txy)
    theta = principal_angle_deg(sx, sy, txy)
    print(f"Center   C     = {c:.3f} MPa")
    print(f"Radius   R     = {r:.3f} MPa")
    print(f"sigma_1        = {s1:.3f} MPa")
    print(f"sigma_2        = {s2:.3f} MPa")
    print(f"tau_max        = {ts:.3f} MPa")
    print(f"theta_p        = {theta:.3f} deg")
