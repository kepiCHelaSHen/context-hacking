"""Spectral Type from Temperature (Wien's Law) — CHP Astronomy Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_stefan_boltzmann_stars_constants import *


def wien_peak(T, b=2.898e-3):
    """Wien's displacement law: lambda_max = b / T.

    Parameters
    ----------
    T : float — effective temperature in Kelvin (must be > 0)
    b : float — Wien's displacement constant in m*K (default: 2.898e-3)

    Returns
    -------
    float — peak wavelength in meters
    """
    if T <= 0:
        raise ValueError("Temperature must be positive")
    return b / T


def spectral_type(T):
    """Return Harvard spectral class for a given effective temperature.

    Parameters
    ----------
    T : float — temperature in Kelvin

    Returns
    -------
    str — one of "O", "B", "A", "F", "G", "K", "M"

    Raises
    ------
    ValueError if T is below 2400 K or non-positive.
    """
    if T <= 0:
        raise ValueError("Temperature must be positive")
    if T > 30000:
        return "O"
    if T > 10000:
        return "B"
    if T > 7500:
        return "A"
    if T > 6000:
        return "F"
    if T > 5200:
        return "G"
    if T > 3700:
        return "K"
    if T >= 2400:
        return "M"
    raise ValueError(f"Temperature {T} K is below M-dwarf range (2400 K)")


def peak_to_nm(lambda_m):
    """Convert wavelength from meters to nanometers.

    Parameters
    ----------
    lambda_m : float — wavelength in meters

    Returns
    -------
    float — wavelength in nanometers
    """
    return lambda_m * 1e9


def temperature_from_peak(lambda_m, b=2.898e-3):
    """Inverse Wien's law: T = b / lambda_max.

    Parameters
    ----------
    lambda_m : float — peak wavelength in meters (must be > 0)
    b : float — Wien's displacement constant in m*K (default: 2.898e-3)

    Returns
    -------
    float — temperature in Kelvin
    """
    if lambda_m <= 0:
        raise ValueError("Wavelength must be positive")
    return b / lambda_m


if __name__ == "__main__":
    for name, T in [("Sun (G2)", T_SUN), ("Sirius (A1)", T_SIRIUS), ("Betelgeuse (M2)", T_BETELGEUSE)]:
        lam = wien_peak(T)
        nm = peak_to_nm(lam)
        stype = spectral_type(T)
        print(f"{name}: T={T} K -> lambda_max={nm:.1f} nm, class {stype}")
    # Round-trip check
    T_back = temperature_from_peak(wien_peak(T_SUN))
    print(f"\nRound-trip Sun: {T_SUN} K -> {peak_to_nm(wien_peak(T_SUN)):.1f} nm -> {T_back:.1f} K")
