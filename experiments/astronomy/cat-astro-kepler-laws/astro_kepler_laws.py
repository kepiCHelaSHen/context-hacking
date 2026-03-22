"""Kepler's Third Law — CHP Astronomy Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_kepler_laws_constants import G_NEWTON, M_SUN, AU_METERS, YR_SECONDS


def kepler_constant(M, G=G_NEWTON):
    """Kepler constant k = 4pi^2/(GM).  Units: s^2/m^3.
    KEY: This depends on the central mass M — it is NOT universal."""
    return 4 * math.pi**2 / (G * M)


def orbital_period(a, M, G=G_NEWTON):
    """Orbital period T = 2pi * sqrt(a^3 / (GM)).
    a : semi-major axis in metres
    M : central mass in kg
    Returns T in seconds."""
    return 2 * math.pi * math.sqrt(a**3 / (G * M))


def semi_major_axis(T, M, G=G_NEWTON):
    """Semi-major axis from period: a = (GM T^2 / (4pi^2))^(1/3).
    T : orbital period in seconds
    M : central mass in kg
    Returns a in metres."""
    return (G * M * T**2 / (4 * math.pi**2))**(1 / 3)


def kepler_ratio_solar():
    """T^2/a^3 in solar-system natural units (yr^2/AU^3).
    Returns 1.0 — but ONLY valid when orbiting the Sun."""
    return 1.0


if __name__ == "__main__":
    from astro_kepler_laws_constants import (
        KEPLER_CONSTANT_SUN, A_EARTH, T_EARTH_DAYS,
        M_DOUBLE_SUN, T_DOUBLE_AT_1AU_DAYS
    )
    # Earth around Sun
    k_sun = kepler_constant(M_SUN)
    T_earth = orbital_period(A_EARTH, M_SUN)
    print(f"Kepler constant (Sun): {k_sun:.4e} s²/m³")
    print(f"Earth period: {T_earth / 86400:.2f} days")

    # Planet at 1 AU around a 2*M_sun star
    k_double = kepler_constant(M_DOUBLE_SUN)
    T_double = orbital_period(A_EARTH, M_DOUBLE_SUN)
    print(f"Kepler constant (2M_sun): {k_double:.4e} s²/m³  (half of Sun's)")
    print(f"Period at 1 AU, 2M_sun star: {T_double / 86400:.2f} days  (< 365)")

    # Round-trip: recover a from T
    a_recovered = semi_major_axis(T_earth, M_SUN)
    print(f"Recovered a (Earth): {a_recovered:.4e} m  (expect {A_EARTH:.4e})")
