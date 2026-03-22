"""Stellar Luminosity (Stefan-Boltzmann) — CHP Astronomy Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_stellar_luminosity_constants import *

def luminosity(R_m, T_K, sigma=5.670e-8):
    """L = 4*pi*R^2 * sigma * T^4.  R in meters, T in Kelvin, returns watts."""
    return 4 * math.pi * R_m**2 * sigma * T_K**4

def luminosity_solar(R_Rsun, T_K, T_sun=5778):
    """L/L_sun = (R/R_sun)^2 * (T/T_sun)^4.  Returns luminosity in solar units."""
    return R_Rsun**2 * (T_K / T_sun)**4

def solar_luminosity():
    """Return solar luminosity in watts (IAU 2015 nominal)."""
    return 3.828e26

def solar_radius():
    """Return solar radius in meters (IAU 2015 nominal)."""
    return 6.957e8

if __name__ == "__main__":
    L = luminosity(R_SUN, T_SUN)
    print(f"Sun: L = {L:.3e} W (expected {L_SUN:.3e} W)")
    L_sir = luminosity(R_SIRIUS_M, T_SIRIUS)
    print(f"Sirius A: L = {L_sir:.3e} W = {L_sir/L_SUN:.1f} L_sun")
    L_sir_solar = luminosity_solar(R_SIRIUS_RSUN, T_SIRIUS)
    print(f"Sirius A (solar units): {L_sir_solar:.1f} L_sun")
