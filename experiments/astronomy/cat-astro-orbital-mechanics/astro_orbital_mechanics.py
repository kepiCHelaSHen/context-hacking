"""Hohmann Transfer Orbit — CHP Astronomy Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_orbital_mechanics_constants import MU_SUN, R_EARTH, R_MARS

def transfer_semi_major(r1, r2):
    """Semi-major axis of Hohmann transfer ellipse: a_t = (r1 + r2) / 2.
    r1: radius of inner circular orbit (m)
    r2: radius of outer circular orbit (m)
    """
    return (r1 + r2) / 2

def hohmann_dv1(mu, r1, r2):
    """Departure burn delta-v for Hohmann transfer.
    Accelerate from circular orbit at r1 onto transfer ellipse.
    dv1 = v_t1 - v_c1
    where v_t1 = sqrt(mu*(2/r1 - 1/a_t)), v_c1 = sqrt(mu/r1)
    """
    a_t = transfer_semi_major(r1, r2)
    v_c1 = math.sqrt(mu / r1)
    v_t1 = math.sqrt(mu * (2 / r1 - 1 / a_t))
    return v_t1 - v_c1

def hohmann_dv2(mu, r1, r2):
    """Arrival burn delta-v for Hohmann transfer.
    Accelerate from transfer ellipse to circular orbit at r2.
    dv2 = v_c2 - v_t2
    where v_t2 = sqrt(mu*(2/r2 - 1/a_t)), v_c2 = sqrt(mu/r2)
    """
    a_t = transfer_semi_major(r1, r2)
    v_c2 = math.sqrt(mu / r2)
    v_t2 = math.sqrt(mu * (2 / r2 - 1 / a_t))
    return v_c2 - v_t2

def hohmann_total_dv(mu, r1, r2):
    """Total delta-v for Hohmann transfer: |dv1| + |dv2|.
    TWO burns are required — departure AND arrival.
    Common LLM error: computing only dv1 and forgetting dv2.
    """
    return abs(hohmann_dv1(mu, r1, r2)) + abs(hohmann_dv2(mu, r1, r2))

def transfer_time(mu, a_t):
    """Transfer time = HALF the orbital period of the transfer ellipse.
    T_transfer = pi * sqrt(a_t^3 / mu)
    Common LLM error: using the full period (2*pi) instead of half (pi).
    """
    return math.pi * math.sqrt(a_t**3 / mu)

if __name__ == "__main__":
    a_t = transfer_semi_major(R_EARTH, R_MARS)
    dv1 = hohmann_dv1(MU_SUN, R_EARTH, R_MARS)
    dv2 = hohmann_dv2(MU_SUN, R_EARTH, R_MARS)
    total = hohmann_total_dv(MU_SUN, R_EARTH, R_MARS)
    t = transfer_time(MU_SUN, a_t)
    print(f"Earth-Mars Hohmann Transfer")
    print(f"  Transfer semi-major axis: {a_t:.6e} m")
    print(f"  Departure dv1: {dv1:.2f} m/s ({dv1/1000:.2f} km/s)")
    print(f"  Arrival   dv2: {dv2:.2f} m/s ({dv2/1000:.2f} km/s)")
    print(f"  Total      dv: {total:.2f} m/s ({total/1000:.2f} km/s)")
    print(f"  Transfer time: {t:.0f} s ({t/86400:.1f} days)")
