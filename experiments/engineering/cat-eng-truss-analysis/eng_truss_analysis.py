"""Truss Analysis — Method of Joints — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_truss_analysis_constants import *


def support_reactions_symmetric(P):
    """Support reactions for symmetric truss with vertical apex load.

    Returns (R_left, R_right) where each reaction = P/2 (upward).
    """
    return (P / 2.0, P / 2.0)


def diagonal_force_equilateral(P, angle_deg=60.0):
    """Force in diagonal member of equilateral triangle truss under apex load P.

    Sign convention: NEGATIVE = COMPRESSION.
    F_diag = -P / (2 * sin(angle))

    The diagonal members are in COMPRESSION because they push inward
    against the joints to resist the applied load.
    """
    angle_rad = math.radians(angle_deg)
    return -P / (2.0 * math.sin(angle_rad))


def horizontal_force_equilateral(P, angle_deg=60.0):
    """Force in horizontal (base) member of equilateral triangle truss under apex load P.

    Sign convention: POSITIVE = TENSION.
    F_horiz = P / (2 * tan(angle))

    The horizontal member is in TENSION because it pulls outward
    on the base joints to prevent them from spreading apart.
    """
    angle_rad = math.radians(angle_deg)
    return P / (2.0 * math.tan(angle_rad))


def is_tension(force):
    """Return True if force indicates tension (positive by convention)."""
    return force > 0.0


def is_compression(force):
    """Return True if force indicates compression (negative by convention)."""
    return force < 0.0


if __name__ == "__main__":
    P = 10.0  # kN
    R_l, R_r = support_reactions_symmetric(P)
    print(f"Support reactions: R_left = {R_l:.4f} kN, R_right = {R_r:.4f} kN")

    F_d = diagonal_force_equilateral(P)
    F_h = horizontal_force_equilateral(P)
    print(f"Diagonal force:   {F_d:.4f} kN  ({'compression' if is_compression(F_d) else 'tension'})")
    print(f"Horizontal force: {F_h:.4f} kN  ({'tension' if is_tension(F_h) else 'compression'})")

    # Verify equilibrium at left support joint
    sin60 = math.sin(math.radians(60.0))
    cos60 = math.cos(math.radians(60.0))
    Fy_check = R_l + F_d * sin60
    Fx_check = F_h + F_d * cos60
    print(f"\nEquilibrium check at left joint:")
    print(f"  Sum Fy = {Fy_check:.10f} (should be 0)")
    print(f"  Sum Fx = {Fx_check:.10f} (should be 0)")
