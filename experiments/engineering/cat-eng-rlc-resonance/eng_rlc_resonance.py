"""RLC Resonance — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_rlc_resonance_constants import *


def resonance_freq_rad(L, C):
    """Return angular resonance frequency omega0 = 1/sqrt(L*C) in rad/s."""
    return 1.0 / math.sqrt(L * C)


def resonance_freq_hz(L, C):
    """Return resonance frequency f0 = 1/(2*pi*sqrt(L*C)) in Hz."""
    return 1.0 / (2.0 * math.pi * math.sqrt(L * C))


def q_factor_series(R, L, C):
    """Return Q factor for series RLC: Q = (1/R)*sqrt(L/C).  NOT R*sqrt(C/L)!"""
    return (1.0 / R) * math.sqrt(L / C)


def bandwidth(f0, Q):
    """Return bandwidth BW = f0/Q in Hz.  NOT f0*Q!"""
    return f0 / Q


def impedance_at_resonance(R):
    """At resonance the reactive parts cancel — impedance is purely resistive: Z = R."""
    return R


if __name__ == "__main__":
    L, C, R = 10e-3, 100e-6, 10.0
    w0 = resonance_freq_rad(L, C)
    f0 = resonance_freq_hz(L, C)
    Q = q_factor_series(R, L, C)
    BW = bandwidth(f0, Q)
    Z = impedance_at_resonance(R)
    print(f"omega0 = {w0:.2f} rad/s")
    print(f"f0     = {f0:.2f} Hz  (NOT {w0:.2f} Hz — 2*pi matters!)")
    print(f"Q      = {Q:.4f}")
    print(f"BW     = {BW:.2f} Hz")
    print(f"Z(res) = {Z:.1f} Ohm (purely resistive)")
