"""Signal Filtering (LP/HP) — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_signal_filtering_constants import *


def cutoff_frequency(R, C):
    """Return cutoff frequency f_c = 1/(2*pi*R*C) in Hz.

    Same formula for both LP and HP first-order RC filters.
    The 2*pi is CRITICAL — omitting it gives angular frequency, not Hz.
    """
    return 1.0 / (2.0 * math.pi * R * C)


def lp_gain(f, fc):
    """Return LP magnitude gain |H_LP(f)| = 1/sqrt(1 + (f/fc)^2).

    LP takes output across C.  At f=fc: gain = 1/sqrt(2) = -3 dB.
    """
    return 1.0 / math.sqrt(1.0 + (f / fc) ** 2)


def hp_gain(f, fc):
    """Return HP magnitude gain |H_HP(f)| = (f/fc)/sqrt(1 + (f/fc)^2).

    HP takes output across R.  At f=fc: gain = 1/sqrt(2) = -3 dB.
    """
    return (f / fc) / math.sqrt(1.0 + (f / fc) ** 2)


def gain_to_db(gain):
    """Convert linear gain to decibels: dB = 20*log10(gain)."""
    return 20.0 * math.log10(gain)


def design_rc(fc, R):
    """Given a target cutoff frequency fc (Hz) and resistance R (Ohm),
    return the required capacitance C (Farad).

    C = 1/(2*pi*fc*R).
    """
    return 1.0 / (2.0 * math.pi * fc * R)


if __name__ == "__main__":
    R, C = 10_000.0, 10e-9  # 10 kOhm, 10 nF
    fc = cutoff_frequency(R, C)
    print(f"f_c = {fc:.4f} Hz  (NOT {1/(R*C):.0f} Hz — 2*pi matters!)")
    print(f"LP gain @ f_c  = {lp_gain(fc, fc):.6f} = {gain_to_db(lp_gain(fc, fc)):.4f} dB")
    print(f"HP gain @ f_c  = {hp_gain(fc, fc):.6f} = {gain_to_db(hp_gain(fc, fc)):.4f} dB")
    print(f"LP gain @ 10*fc = {lp_gain(10*fc, fc):.6f} = {gain_to_db(lp_gain(10*fc, fc)):.4f} dB")
    print(f"HP gain @ 0.1*fc = {hp_gain(0.1*fc, fc):.6f} = {gain_to_db(hp_gain(0.1*fc, fc)):.4f} dB")
    C_needed = design_rc(1000.0, 10_000.0)
    print(f"Design: fc=1000 Hz, R=10 kOhm => C = {C_needed*1e9:.4f} nF")
