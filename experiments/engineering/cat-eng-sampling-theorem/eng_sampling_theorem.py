"""Nyquist-Shannon Sampling Theorem — CHP Engineering Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_sampling_theorem_constants import *


def nyquist_rate(f_max):
    """Return minimum sampling rate f_s = 2 * f_max to avoid aliasing.

    KEY: The Nyquist rate is 2x the max frequency, NOT 1x.
    Example: f_max = 20 kHz => f_s_min = 40 kHz.
    """
    return 2.0 * f_max


def nyquist_frequency(f_s):
    """Return the Nyquist frequency f_N = f_s / 2.

    This is the maximum frequency that can be faithfully represented
    at sampling rate f_s. NOT the same as the Nyquist rate.
    """
    return f_s / 2.0


def is_aliased(f_signal, f_s):
    """Return True if f_signal > f_s/2 (above Nyquist frequency), causing aliasing."""
    return f_signal > f_s / 2.0


def alias_frequency(f_signal, f_s):
    """Return the aliased frequency when sampling f_signal at rate f_s.

    Formula: alias = |f_signal - k * f_s| for integer k nearest to f_signal/f_s.
    If f_signal <= f_s/2, the signal is not aliased; return f_signal unchanged.
    """
    if f_signal <= f_s / 2.0:
        return float(f_signal)
    k = round(f_signal / f_s)
    return abs(f_signal - k * f_s)


if __name__ == "__main__":
    f_max = 20000  # 20 kHz
    fs_min = nyquist_rate(f_max)
    print(f"f_max = {f_max} Hz")
    print(f"Nyquist rate = {fs_min} Hz (NOT {f_max} Hz — 2x matters!)")
    print(f"CD sample rate = {CD_SAMPLE_RATE} Hz")
    print(f"CD Nyquist freq = {nyquist_frequency(CD_SAMPLE_RATE)} Hz")
    print()
    # Aliasing demo
    f_sig, fs = 25000, 30000
    print(f"Signal {f_sig} Hz sampled at {fs} Hz:")
    print(f"  Aliased? {is_aliased(f_sig, fs)}")
    print(f"  Alias freq = {alias_frequency(f_sig, fs)} Hz")
