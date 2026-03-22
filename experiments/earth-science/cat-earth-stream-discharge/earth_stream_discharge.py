"""Stream Discharge (Manning's Equation) — CHP Earth Science Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_stream_discharge_constants import *


def wetted_perimeter_rect(b, d):
    """Wetted perimeter for rectangular channel: P = b + 2d (bottom + BOTH sides)."""
    return b + 2 * d


def hydraulic_radius(A, P):
    """Hydraulic radius: R = A / P (cross-section area / wetted perimeter)."""
    return A / P


def manning_velocity(n, R, S):
    """Manning's equation: v = (1/n) * R^(2/3) * S^(1/2). Returns m/s."""
    return (1 / n) * R**(2/3) * S**0.5


def discharge(v, A):
    """Discharge: Q = v * A. Returns m^3/s."""
    return v * A


if __name__ == "__main__":
    A = B_CHANNEL * D_CHANNEL
    P = wetted_perimeter_rect(B_CHANNEL, D_CHANNEL)
    R = hydraulic_radius(A, P)
    v = manning_velocity(N_MANNING, R, S_SLOPE)
    Q = discharge(v, A)
    print(f"Rectangular channel: b={B_CHANNEL}m, d={D_CHANNEL}m")
    print(f"  A = {A:.1f} m^2")
    print(f"  P = {P:.1f} m  (b + 2d, NOT just b!)")
    print(f"  R = A/P = {R:.4f} m  (NOT depth!)")
    print(f"  v = {v:.4f} m/s")
    print(f"  Q = {Q:.4f} m^3/s")
    print(f"\nWRONG (R=depth): v={V_WRONG_DEPTH:.4f}, Q={Q_WRONG_DEPTH:.4f} ({ERROR_PERCENT_DEPTH:.1f}% too high!)")
