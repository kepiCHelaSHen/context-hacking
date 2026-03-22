"""
Nernst equation implementation for membrane equilibrium potentials.

E_ion = (RT / zF) * ln([ion]_out / [ion]_in)

Returns potential in millivolts (mV).
"""

import math

from frozen.bio_membrane_potential_constants import R, F


def rt_over_f(T=310.15):
    """Return RT/F in volts for a given temperature (Kelvin)."""
    return R * T / F


def nernst(z, ion_out, ion_in, T=310.15):
    """
    Compute the Nernst equilibrium potential for a single ion species.

    Parameters
    ----------
    z : int
        Signed valence of the ion (+1 for K+ and Na+, -1 for Cl-).
    ion_out : float
        Extracellular concentration (mM).
    ion_in : float
        Intracellular concentration (mM).
    T : float
        Temperature in Kelvin (default 310.15 K = 37 C).

    Returns
    -------
    float
        Equilibrium potential in millivolts (mV).

    Raises
    ------
    ValueError
        If z is zero, or if concentrations are non-positive.
    """
    if z == 0:
        raise ValueError("Valence z must be non-zero.")
    if ion_out <= 0 or ion_in <= 0:
        raise ValueError("Ion concentrations must be positive.")

    return (rt_over_f(T) / z) * math.log(ion_out / ion_in) * 1000
