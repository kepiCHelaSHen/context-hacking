"""Coriolis Parameter — CHP Earth Science Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_coriolis_constants import *


def omega_earth():
    """Return Earth's rotational angular velocity in rad/s."""
    return OMEGA_EARTH


def coriolis_parameter(lat_deg):
    """Coriolis parameter f = 2*Omega*sin(phi). Returns s^-1."""
    return 2 * OMEGA_EARTH * math.sin(math.radians(lat_deg))


def coriolis_acceleration(f, v):
    """Coriolis acceleration magnitude a_c = f * v. Returns m/s^2."""
    return abs(f) * v


def deflection_direction(lat_deg):
    """Deflection direction due to Coriolis: 'right' (NH), 'left' (SH), 'none' (equator)."""
    f = coriolis_parameter(lat_deg)
    if f > 0:
        return "right"
    elif f < 0:
        return "left"
    else:
        return "none"


if __name__ == "__main__":
    print(f"Omega_Earth = {omega_earth():.4e} rad/s")
    for lat in [0, 30, 45, 60, 90]:
        f = coriolis_parameter(lat)
        d = deflection_direction(lat)
        print(f"  lat={lat:3d} deg: f={f:.4e} 1/s, deflection={d}")
    print(f"\nTest: v={TEST_V} m/s at {TEST_LAT} deg N")
    print(f"  f = {coriolis_parameter(TEST_LAT):.4e} 1/s")
    print(f"  a_c = {coriolis_acceleration(coriolis_parameter(TEST_LAT), TEST_V):.4e} m/s^2")
