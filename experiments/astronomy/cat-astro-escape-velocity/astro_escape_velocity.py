"""Escape Velocity — CHP Astronomy Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_escape_velocity_constants import *

def escape_velocity(M, R, G_const=6.674e-11):
    """v_esc = sqrt(2GM/R). R = distance from CENTER of body."""
    return math.sqrt(2 * G_const * M / R)

def escape_velocity_km_s(M, R):
    """Escape velocity in km/s."""
    return escape_velocity(M, R) / 1000.0

def surface_gravity(M, R, G_const=6.674e-11):
    """g = GM/R²."""
    return G_const * M / R**2

if __name__ == "__main__":
    for name, M, R in [("Earth", M_EARTH, R_EARTH_MEAN), ("Moon", M_MOON, R_MOON),
                        ("Mars", M_MARS, R_MARS), ("Jupiter", M_JUPITER, R_JUPITER)]:
        v = escape_velocity_km_s(M, R)
        g = surface_gravity(M, R)
        print(f"{name}: v_esc={v:.2f} km/s, g={g:.3f} m/s²")
