"""
Earthquake Magnitude — CHP Earth Science Sprint
Moment magnitude (Mw), energy-magnitude relation, amplitude/energy scaling.
Modern seismology uses Mw (not ML) for large earthquakes.
All constants from frozen spec.
"""
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_richter_scale_constants import (
    MW_COEFF, MW_OFFSET_NM, ENERGY_SLOPE, ENERGY_OFFSET,
)


def moment_magnitude(M0_Nm):
    """Moment magnitude: Mw = (2/3) * (log10(M0) - 9.1), M0 in N·m.
    NOT the Richter local magnitude (ML), which saturates above ~7."""
    return MW_COEFF * (math.log10(M0_Nm) - MW_OFFSET_NM)


def energy_from_magnitude(Mw):
    """Seismic energy in joules: log10(E) = 1.5*Mw + 4.8.
    Gutenberg-Richter energy-magnitude relation."""
    return 10.0 ** (ENERGY_SLOPE * Mw + ENERGY_OFFSET)


def energy_ratio(dM):
    """Energy ratio for a magnitude difference dM.
    +1 magnitude = 10^1.5 = ~31.623x energy. NOT 10x."""
    return 10.0 ** (ENERGY_SLOPE * dM)


def amplitude_ratio(dM):
    """Amplitude ratio for a magnitude difference dM.
    +1 magnitude = 10x amplitude (this IS 10x, unlike energy)."""
    return 10.0 ** dM


def seismic_moment_from_Mw(Mw):
    """Inverse: M0 (N·m) from Mw.  M0 = 10^(1.5*Mw + 9.1)."""
    return 10.0 ** (Mw / MW_COEFF + MW_OFFSET_NM)


if __name__ == "__main__":
    print("=== Earthquake Magnitude ===\n")

    # Reference: M0 = 1e20 N·m
    M0_test = 1e20
    Mw_test = moment_magnitude(M0_test)
    print(f"M0 = {M0_test:.0e} N·m  ->  Mw = {Mw_test:.4f}")
    print(f"  Expected: (2/3)*(20 - 9.1) = (2/3)*10.9 = 7.2667\n")

    # Energy from that magnitude
    E = energy_from_magnitude(Mw_test)
    print(f"Energy at Mw={Mw_test:.3f}: {E:.3e} J")
    print(f"  log10(E) = {math.log10(E):.4f} (should = 1.5*{Mw_test:.3f} + 4.8 = {1.5*Mw_test + 4.8:.4f})\n")

    # Energy ratio for +1 magnitude
    ratio_1 = energy_ratio(1.0)
    print(f"Energy ratio for +1 magnitude: {ratio_1:.3f}")
    print(f"  This is 10^1.5, NOT 10. Common LLM error: claiming 10x.\n")

    # Amplitude ratio for +1 magnitude
    amp_1 = amplitude_ratio(1.0)
    print(f"Amplitude ratio for +1 magnitude: {amp_1:.1f}")
    print(f"  This IS 10x (amplitude, not energy).\n")

    # Round-trip test
    M0_back = seismic_moment_from_Mw(Mw_test)
    print(f"Round-trip: Mw={Mw_test:.4f} -> M0={M0_back:.3e} N·m (original: {M0_test:.0e})")
