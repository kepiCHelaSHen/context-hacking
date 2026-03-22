"""Bode Plot — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_bode_plot_constants import *


def first_order_gain_db(omega, omega_0):
    """Gain of H(s)=1/(1+s/ω₀) in dB: 20·log₁₀(1/√(1+(ω/ω₀)²)).

    At the pole frequency (ω = ω₀) this is −3.01 dB, NOT 0 dB or some
    linear value.  The dB conversion is mandatory.
    """
    return 20.0 * math.log10(1.0 / math.sqrt(1.0 + (omega / omega_0) ** 2))


def first_order_phase(omega, omega_0):
    """Phase of H(s)=1/(1+s/ω₀) in degrees: −arctan(ω/ω₀).

    CRITICAL: at ω = ω₀ this returns −45°, NOT −90°.
    Phase approaches −90° only asymptotically as ω → ∞.
    """
    return -math.degrees(math.atan(omega / omega_0))


def db_to_linear(db):
    """Convert decibels to linear magnitude: 10^(dB/20)."""
    return 10.0 ** (db / 20.0)


def linear_to_db(linear):
    """Convert linear magnitude to decibels: 20·log₁₀(linear).

    Input must be positive.
    """
    if linear <= 0:
        raise ValueError("linear magnitude must be positive")
    return 20.0 * math.log10(linear)


if __name__ == "__main__":
    w0 = OMEGA_0  # 100 rad/s
    print(f"First-order LP: H(s) = 1/(1 + s/{w0})")
    print()
    for label, w in [("0.1·ω₀", 0.1 * w0), ("ω₀", w0), ("10·ω₀", 10.0 * w0)]:
        g = first_order_gain_db(w, w0)
        p = first_order_phase(w, w0)
        print(f"  ω = {label:>6s} ({w:>7.1f} rad/s):  gain = {g:+.4f} dB,  phase = {p:+.4f}°")
    print()
    print(f"  dB → linear:  −3.01 dB = {db_to_linear(-3.01):.6f}")
    print(f"  linear → dB:  0.5      = {linear_to_db(0.5):.4f} dB")
