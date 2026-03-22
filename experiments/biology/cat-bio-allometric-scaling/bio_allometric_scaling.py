"""Allometric Scaling (Kleiber's Law) — CHP Biology Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_allometric_scaling_constants import *


def metabolic_rate(M, B0=70, exponent=0.75):
    """Metabolic rate B = B0 * M^exponent (kcal/day, M in kg)."""
    return B0 * M ** exponent


def kleiber_exponent():
    """Return the correct Kleiber scaling exponent: 3/4."""
    return 0.75


def rubner_exponent():
    """Return the incorrect Rubner surface-area exponent: 2/3."""
    return 2 / 3


def mass_specific_rate(M, B0=70, exponent=0.75):
    """Mass-specific metabolic rate B/M = B0 * M^(exponent - 1)."""
    return B0 * M ** (exponent - 1)


if __name__ == "__main__":
    for name, mass in [("Mouse", M_MOUSE), ("Human", M_HUMAN), ("Elephant", M_ELEPHANT)]:
        B = metabolic_rate(mass)
        msr = mass_specific_rate(mass)
        print(f"{name:>10} ({mass:>6} kg): B = {B:>10.1f} kcal/day, B/M = {msr:.2f} kcal/day/kg")
    B_wrong = metabolic_rate(M_HUMAN, exponent=rubner_exponent())
    print(f"\nHuman with WRONG 2/3 exponent: {B_wrong:.1f} kcal/day "
          f"(underestimates by {(1 - B_wrong / metabolic_rate(M_HUMAN)) * 100:.0f}%)")
