"""Hemoglobin O2 Saturation Curve — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_oxygen_dissociation_constants import *


def o2_saturation(pO2, P50, n):
    """Return fractional O2 saturation Y = pO2^n / (P50^n + pO2^n).

    Parameters
    ----------
    pO2 : float  — partial pressure of O2 (mmHg), >= 0
    P50 : float  — partial pressure at 50 % saturation (mmHg), > 0
    n   : float  — Hill coefficient (cooperativity)

    Returns
    -------
    float — Y in [0, 1]
    """
    if pO2 < 0:
        raise ValueError("pO2 must be non-negative")
    if P50 <= 0:
        raise ValueError("P50 must be positive")
    pO2_n = pO2 ** n
    P50_n = P50 ** n
    return pO2_n / (P50_n + pO2_n)


def p50_at_ph(pH):
    """Return approximate P50 (mmHg) for a given blood pH.

    Uses a simple linear Bohr-effect model:
        P50 = 26.6 + (7.4 - pH) * 17

    Lower pH -> right shift -> higher P50 (less O2 affinity).
    Higher pH -> left shift -> lower P50 (more O2 affinity).
    """
    return P50_NORMAL + (7.4 - pH) * BOHR_SLOPE


def bohr_shift_direction(pH):
    """Return the direction of the O2-dissociation curve shift for a given pH.

    Returns
    -------
    str — "right" if pH < 7.4 (lower affinity),
          "left"  if pH > 7.4 (higher affinity),
          "none"  if pH == 7.4.
    """
    if math.isclose(pH, 7.4, abs_tol=1e-9):
        return "none"
    elif pH < 7.4:
        return "right"
    else:
        return "left"


if __name__ == "__main__":
    print(f"P50 = {P50_NORMAL} mmHg (pH 7.4), Hill n = {N_HILL}")
    for pO2 in [26.6, 40.0, 100.0]:
        Y = o2_saturation(pO2, P50_NORMAL, N_HILL)
        print(f"  Y({pO2:.1f}) = {Y:.6f}")
    for pH in [7.2, 7.4, 7.6]:
        p50 = p50_at_ph(pH)
        direction = bohr_shift_direction(pH)
        print(f"  pH {pH}: P50 = {p50:.1f} mmHg, shift = {direction}")
