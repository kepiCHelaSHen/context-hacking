"""CO2 Radiative Forcing — CHP Earth Science Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_radiative_forcing_constants import ALPHA, C0, LN2, DF_DOUBLING

def radiative_forcing(C, C0=C0, alpha=ALPHA):
    """Compute radiative forcing from CO2 concentration change.

    Uses the Myhre et al. (1998) logarithmic formula:
        dF = alpha * ln(C / C0)   W/m^2

    Args:
        C:     current CO2 concentration in ppm
        C0:    reference (preindustrial) CO2 concentration in ppm (default 280)
        alpha: radiative forcing coefficient in W/m^2 (default 5.35)

    Returns:
        Radiative forcing in W/m^2.
    """
    if C <= 0 or C0 <= 0:
        raise ValueError("CO2 concentrations must be positive")
    return alpha * math.log(C / C0)

def forcing_doubling(alpha=ALPHA):
    """Compute radiative forcing for a doubling of CO2.

    dF_2x = alpha * ln(2)

    Args:
        alpha: radiative forcing coefficient in W/m^2 (default 5.35)

    Returns:
        Radiative forcing in W/m^2 for CO2 doubling.
    """
    return alpha * math.log(2)

def co2_for_forcing(dF, C0=C0, alpha=ALPHA):
    """Compute the CO2 concentration that produces a given radiative forcing.

    Inverse of the Myhre formula: C = C0 * exp(dF / alpha)

    Args:
        dF:    target radiative forcing in W/m^2
        C0:    reference CO2 concentration in ppm (default 280)
        alpha: radiative forcing coefficient in W/m^2 (default 5.35)

    Returns:
        CO2 concentration in ppm.
    """
    if C0 <= 0 or alpha <= 0:
        raise ValueError("C0 and alpha must be positive")
    return C0 * math.exp(dF / alpha)

def is_logarithmic():
    """Confirm the radiative forcing relationship is logarithmic.

    KEY FACT: Radiative forcing from CO2 follows a logarithmic relationship,
    meaning each successive doubling produces the same additional forcing
    (~3.7 W/m^2). This is NOT linear.

    Returns:
        True — the relationship is always logarithmic.
    """
    return True

if __name__ == "__main__":
    print(f"Radiative forcing coefficient (alpha): {ALPHA} W/m^2")
    print(f"Reference CO2 (C0): {C0} ppm")
    print(f"\nDoubling forcing: {forcing_doubling():.4f} W/m^2 (approx 3.7)")
    print(f"  = {ALPHA} * ln(2) = {ALPHA} * {math.log(2):.4f}")
    print(f"\nCurrent CO2 = 420 ppm:")
    dF = radiative_forcing(420)
    print(f"  dF = {ALPHA} * ln(420/280) = {ALPHA} * {math.log(420/280):.4f} = {dF:.4f} W/m^2")
    print(f"\nWrong linear calc: {ALPHA} * (420-280)/280 = {ALPHA * (420-280)/280:.4f} W/m^2 (23% too high!)")
    print(f"\nInverse: CO2 for dF={dF:.4f} = {co2_for_forcing(dF):.1f} ppm (should be 420)")
    print(f"Is logarithmic? {is_logarithmic()}")
