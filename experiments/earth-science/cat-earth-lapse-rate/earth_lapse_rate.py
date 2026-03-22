"""Temperature Lapse Rate — CHP Earth Science Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_lapse_rate_constants import G, CP, DALR_CONV, MALR_PER_KM, ENV_LAPSE_PER_KM

def dalr():
    """Return the conventional Dry Adiabatic Lapse Rate in °C/km."""
    return 9.8

def temperature_at_altitude(T_surface, lapse_rate, altitude_km):
    """Compute temperature at a given altitude.

    Args:
        T_surface:    surface temperature in °C
        lapse_rate:   lapse rate in °C/km (positive means cooling with height)
        altitude_km:  altitude in km above surface

    Returns:
        Temperature in °C at the given altitude.
    """
    return T_surface - lapse_rate * altitude_km

def is_stable(env_lapse, dalr_val=None):
    """Determine if the atmosphere is absolutely stable.

    Absolutely stable when environmental lapse rate < DALR.
    (Parcel cools faster than environment, so it sinks back.)

    Args:
        env_lapse: environmental lapse rate in °C/km
        dalr_val:  dry adiabatic lapse rate (default: 9.8 °C/km)

    Returns:
        True if absolutely stable, False otherwise.
    """
    if dalr_val is None:
        dalr_val = dalr()
    return env_lapse < dalr_val

def lifting_condensation_level(T, Td):
    """Approximate Lifting Condensation Level using Espy/Bolton formula.

    Args:
        T:  surface temperature in °C
        Td: surface dewpoint temperature in °C

    Returns:
        Approximate LCL height in km.
    """
    return (T - Td) / 8.0

if __name__ == "__main__":
    print(f"DALR: {dalr()} °C/km")
    print(f"MALR: ~{MALR_PER_KM} °C/km (representative)")
    print(f"Environmental: {ENV_LAPSE_PER_KM} °C/km (average)")
    print(f"\nOrdering: DALR ({dalr()}) > Env ({ENV_LAPSE_PER_KM}) > MALR ({MALR_PER_KM})")
    print(f"\nTest — T_surface=20°C, altitude=3km:")
    print(f"  Dry adiabatic:  {temperature_at_altitude(20, dalr(), 3):.1f} °C")
    print(f"  Moist adiabatic: {temperature_at_altitude(20, MALR_PER_KM, 3):.1f} °C")
    print(f"  Environmental:   {temperature_at_altitude(20, ENV_LAPSE_PER_KM, 3):.1f} °C")
    print(f"\nLCL (T=25°C, Td=17°C): {lifting_condensation_level(25, 17):.2f} km")
    print(f"Stable (env=5.0)? {is_stable(5.0)} — correct, less than DALR")
    print(f"Stable (env=11.0)? {is_stable(11.0)} -- correct, greater than DALR = unstable")
