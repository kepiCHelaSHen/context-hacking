"""Planetary Equilibrium Temperature — CHP Astronomy Sprint.

T_eq = (L(1-A) / (16*pi*sigma*d^2))^(1/4)

This is the blackbody equilibrium temperature — what a planet would have with
NO atmosphere.  The greenhouse effect raises the actual surface temperature
above T_eq for any planet with an atmosphere.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_equilibrium_temp_constants import *


def equilibrium_temp(L, d, A, sigma=5.6704e-8):
    """Compute planetary equilibrium temperature.

    Parameters
    ----------
    L : float — stellar luminosity in watts
    d : float — orbital distance in meters (must be > 0)
    A : float — Bond albedo, 0 <= A < 1
    sigma : float — Stefan-Boltzmann constant (default: 5.6704e-8 W m^-2 K^-4)

    Returns
    -------
    float — equilibrium temperature in Kelvin

    Raises
    ------
    ValueError if d <= 0 or A is out of range [0, 1).
    """
    if d <= 0:
        raise ValueError("Orbital distance must be positive")
    if not (0 <= A < 1):
        raise ValueError(f"Albedo must be in [0, 1), got {A}")
    if L <= 0:
        raise ValueError("Luminosity must be positive")
    return (L * (1 - A) / (16 * math.pi * sigma * d**2)) ** 0.25


def greenhouse_effect(T_actual, T_eq):
    """Compute the greenhouse warming delta.

    Parameters
    ----------
    T_actual : float — observed surface temperature in Kelvin
    T_eq : float — computed equilibrium temperature in Kelvin

    Returns
    -------
    float — greenhouse delta (T_actual - T_eq) in Kelvin
            Positive means atmosphere warms the surface (normal).
    """
    return T_actual - T_eq


def is_habitable(T_actual, T_min=273, T_max=373):
    """Check whether a surface temperature falls in the liquid-water habitable range.

    Parameters
    ----------
    T_actual : float — surface temperature in Kelvin
    T_min : float — lower bound (default: 273 K = 0 C)
    T_max : float — upper bound (default: 373 K = 100 C)

    Returns
    -------
    bool — True if T_min <= T_actual <= T_max
    """
    return T_min <= T_actual <= T_max


if __name__ == "__main__":
    planets = [
        ("Earth", L_SUN, D_EARTH, A_EARTH, T_ACTUAL_EARTH),
        ("Venus", L_SUN, D_VENUS, A_VENUS, T_ACTUAL_VENUS),
        ("Mars",  L_SUN, D_MARS,  A_MARS,  T_ACTUAL_MARS),
    ]
    for name, L, d, A, T_act in planets:
        T_eq = equilibrium_temp(L, d, A)
        dT = greenhouse_effect(T_act, T_eq)
        hab = is_habitable(T_act)
        print(f"{name}: T_eq={T_eq:.1f} K, T_actual={T_act} K, "
              f"greenhouse={dT:+.1f} K, habitable={hab}")
