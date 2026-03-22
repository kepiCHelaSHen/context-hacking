"""CMB Temperature — 2.725 K, Wien Peak Wavelength — CHP Astronomy Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_cmb_temperature_constants import *


def cmb_temperature():
    """Return the CMB temperature from COBE/FIRAS measurement.

    Returns
    -------
    float — T_CMB in Kelvin (2.7255 K, NOT 3 K)
    """
    return 2.7255


def cmb_peak_wavelength(T=2.7255, b=2.898e-3):
    """Wien's displacement law (wavelength form): lambda_max = b / T.

    Parameters
    ----------
    T : float — temperature in Kelvin (default: T_CMB = 2.7255 K)
    b : float — Wien's displacement constant in m*K (default: 2.898e-3)

    Returns
    -------
    float — peak wavelength in meters
    """
    if T <= 0:
        raise ValueError("Temperature must be positive")
    return b / T


def cmb_peak_frequency(lambda_m):
    """Convert peak wavelength to frequency: nu = c / lambda.

    Note: this gives c/lambda_max, which differs from the Wien frequency
    peak (nu_max = b_nu * T).  For the true frequency peak, use
    wien_frequency_peak().

    Parameters
    ----------
    lambda_m : float — wavelength in meters (must be > 0)

    Returns
    -------
    float — frequency in Hz
    """
    if lambda_m <= 0:
        raise ValueError("Wavelength must be positive")
    return C_LIGHT / lambda_m


def wien_frequency_peak(T=2.7255, b_nu=5.879e10):
    """Wien's displacement law (frequency form): nu_max = b_nu * T.

    Parameters
    ----------
    T : float — temperature in Kelvin (default: T_CMB = 2.7255 K)
    b_nu : float — Wien frequency constant in Hz/K (default: 5.879e10)

    Returns
    -------
    float — peak frequency in Hz
    """
    if T <= 0:
        raise ValueError("Temperature must be positive")
    return b_nu * T


def temperature_at_redshift(T_now, z):
    """CMB temperature at a given redshift: T(z) = T_now * (1 + z).

    Parameters
    ----------
    T_now : float — present-day CMB temperature in Kelvin
    z : float — cosmological redshift (must be >= 0)

    Returns
    -------
    float — temperature at redshift z in Kelvin
    """
    if z < 0:
        raise ValueError("Redshift must be non-negative")
    return T_now * (1 + z)


if __name__ == "__main__":
    T = cmb_temperature()
    lam = cmb_peak_wavelength(T)
    nu_lam = cmb_peak_frequency(lam)
    nu_wien = wien_frequency_peak(T)
    T_ls = temperature_at_redshift(T, Z_LAST_SCATTERING)

    print(f"CMB temperature:         {T} K")
    print(f"Wien peak wavelength:    {lam*1e3:.4f} mm  ({lam:.6e} m)")
    print(f"c / lambda_max:          {nu_lam/1e9:.2f} GHz")
    print(f"Wien frequency peak:     {nu_wien/1e9:.2f} GHz")
    print(f"T at last scattering:    {T_ls:.1f} K  (z={Z_LAST_SCATTERING})")
    print(f"\nCommon error (3K) peak:  {2.898e-3/3.0*1e3:.4f} mm  (off by {abs(3.0-T)/T*100:.1f}%)")
