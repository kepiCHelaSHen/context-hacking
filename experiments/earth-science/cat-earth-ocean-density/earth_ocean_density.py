"""Ocean Water Density — CHP Earth Science Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_ocean_density_constants import RHO_BASE, SALT_COEFF, TEMP_COEFF, T_MAX_DENSITY, SIGMA_T_OFFSET

def seawater_density(T, S):
    """Compute simplified seawater density near the surface.

    Uses empirical approximation: rho = 1000 + 0.8*S - 0.0065*(T - 4)^2

    Args:
        T: temperature in deg C
        S: salinity in psu (practical salinity units)

    Returns:
        Density in kg/m^3.
    """
    return RHO_BASE + SALT_COEFF * S - TEMP_COEFF * (T - T_MAX_DENSITY)**2

def sigma_t(rho):
    """Convert full density to sigma-t notation.

    sigma_t = rho - 1000

    Args:
        rho: density in kg/m^3

    Returns:
        sigma_t value (dimensionless, but conventionally in kg/m^3 offset).
    """
    return rho - SIGMA_T_OFFSET

def freshwater_max_density_temp():
    """Return the temperature at which freshwater has maximum density.

    Returns:
        4.0 deg C -- the well-known anomaly of water.
    """
    return T_MAX_DENSITY

def density_change_T(T1, T2, S):
    """Compute how density changes when temperature changes from T1 to T2 at fixed salinity.

    Args:
        T1: initial temperature in deg C
        T2: final temperature in deg C
        S:  salinity in psu

    Returns:
        Change in density (rho2 - rho1) in kg/m^3.  Negative means density decreased.
    """
    rho1 = seawater_density(T1, S)
    rho2 = seawater_density(T2, S)
    return rho2 - rho1

if __name__ == "__main__":
    rho = seawater_density(10.0, 35.0)
    print(f"Seawater density (T=10C, S=35 psu): {rho:.3f} kg/m3")
    print(f"  sigma_t = {sigma_t(rho):.3f}")
    rho2 = seawater_density(25.0, 36.0)
    print(f"Seawater density (T=25C, S=36 psu): {rho2:.4f} kg/m3")
    print(f"  sigma_t = {sigma_t(rho2):.4f}")
    print(f"Freshwater max density at: {freshwater_max_density_temp()}C")
    dT = density_change_T(10.0, 20.0, 35.0)
    print(f"Density change T=10->20C, S=35 psu: {dT:.3f} kg/m3 (should be negative)")
