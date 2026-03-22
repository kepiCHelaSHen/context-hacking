"""Gravitational Physics — CHP Physics Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_gravity_constants import G_NEWTON, M_SUN, M_EARTH, R_EARTH, R_EARTH_ORBIT

def gravitational_force(m1, m2, r):
    """F = Gm1m2/r²."""
    return G_NEWTON * m1 * m2 / r**2

def surface_gravity(M, R):
    """g = GM/R²."""
    return G_NEWTON * M / R**2

def escape_velocity(M, R):
    """v_esc = √(2GM/R). Note the √2 factor vs orbital."""
    return math.sqrt(2 * G_NEWTON * M / R)

def orbital_velocity(M, r):
    """v_orb = √(GM/r). For circular orbit."""
    return math.sqrt(G_NEWTON * M / r)

def orbital_period(M, a):
    """T = 2π√(a³/(GM)). Kepler's 3rd law."""
    return 2 * math.pi * math.sqrt(a**3 / (G_NEWTON * M))

def gravitational_pe(m1, m2, r):
    """U = -Gm1m2/r (negative — bound state)."""
    return -G_NEWTON * m1 * m2 / r

if __name__ == "__main__":
    print(f"g(Earth surface): {surface_gravity(M_EARTH, R_EARTH):.2f} m/s²")
    print(f"v_esc(Earth): {escape_velocity(M_EARTH, R_EARTH):.0f} m/s")
    print(f"v_orb(Earth around Sun): {orbital_velocity(M_SUN, R_EARTH_ORBIT):.0f} m/s")
    T = orbital_period(M_SUN, R_EARTH_ORBIT)
    print(f"Earth orbital period: {T/86400:.1f} days")
