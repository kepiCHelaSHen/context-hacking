"""Main Sequence Lifetime — CHP Astronomy Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_main_sequence_constants import T_SUN_GYR

def mass_luminosity(M_Msun, alpha=3.5):
    """L/L_sun = (M/M_sun)^alpha. Returns luminosity in solar units."""
    return M_Msun ** alpha

def ms_lifetime(M_Msun, alpha=3.5, t_sun=T_SUN_GYR):
    """Main-sequence lifetime in Gyr.
    t_ms = t_sun * M^(1-alpha).
    More massive → SHORTER life (luminosity grows faster than mass).
    """
    return t_sun * M_Msun ** (1.0 - alpha)

def lifetime_ratio(M1, M2, alpha=3.5):
    """Ratio of MS lifetimes: t1/t2 = (M1/M2)^(1-alpha)."""
    return (M1 / M2) ** (1.0 - alpha)

if __name__ == "__main__":
    print(f"L(10 M_sun): {mass_luminosity(10.0):.1f} L_sun")
    print(f"t_ms(Sun):   {ms_lifetime(1.0):.1f} Gyr")
    print(f"t_ms(10 M_sun): {ms_lifetime(10.0)*1000:.1f} Myr -- dies FAST!")
    print(f"t_ms(0.5 M_sun, a=4): {ms_lifetime(0.5, alpha=4.0):.1f} Gyr -- outlives universe")
    print(f"Ratio 5/1 M_sun: {lifetime_ratio(5.0, 1.0):.5f} (5x mass -> 56x shorter life)")
