"""Single-Layer Atmosphere Model — CHP Earth Science Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_greenhouse_simple_constants import *


def bare_earth_temp(S=1361, alpha=0.30):
    """Bare-earth equilibrium temperature (no atmosphere).
    Energy balance: σT⁴ = S(1-α)/4  →  T = (S(1-α)/(4σ))^(1/4).
    Returns temperature in Kelvin.
    """
    return (S * (1 - alpha) / (4 * SIGMA)) ** 0.25


def greenhouse_1layer_temp(T_bare):
    """Surface temperature under single-layer atmosphere with ε=1.
    T_surface = T_bare * 2^(1/4).
    NOTE: This OVERESTIMATES real greenhouse effect because real ε < 1.
    Returns temperature in Kelvin.
    """
    return T_bare * 2 ** 0.25


def stefan_boltzmann_flux(T, epsilon=1.0):
    """Stefan-Boltzmann radiative flux F = εσT⁴.
    Returns flux in W/m².
    """
    return epsilon * SIGMA * T ** 4


def greenhouse_effect(T_surface, T_bare):
    """Greenhouse effect ΔT = T_surface - T_bare.
    Returns temperature difference in Kelvin.
    """
    return T_surface - T_bare


if __name__ == "__main__":
    Tb = bare_earth_temp()
    T1 = greenhouse_1layer_temp(Tb)
    dT_model = greenhouse_effect(T1, Tb)
    dT_real = greenhouse_effect(T_SURFACE_OBSERVED, Tb)

    print(f"Stefan-Boltzmann constant sigma = {SIGMA} W/(m^2 K^4)")
    print(f"Solar constant S = {S_SOLAR} W/m^2,  albedo alpha = {ALPHA}")
    print(f"Absorbed flux = S(1-alpha)/4 = {F_ABSORBED:.3f} W/m^2")
    print(f"\nBare-earth temperature T_bare = {Tb:.2f} K  ({Tb - 273.15:.1f} C)")
    print(f"Single-layer eps=1 surface temp = {T1:.2f} K  ({T1 - 273.15:.1f} C)  [OVERESTIMATE]")
    print(f"Observed surface temp           = {T_SURFACE_OBSERVED:.0f} K  ({T_SURFACE_OBSERVED - 273.15:.0f} C)")
    print(f"\nGreenhouse effect (eps=1 model) = {dT_model:.2f} K")
    print(f"Greenhouse effect (observed)    = {dT_real:.2f} K")
    print(f"\nFlux at 288K (eps=1):   {stefan_boltzmann_flux(288.0):.2f} W/m^2")
    print(f"Flux at 288K (eps=0.78): {stefan_boltzmann_flux(288.0, 0.78):.2f} W/m^2")
