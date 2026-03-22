"""Viscosity & Stokes Drag — CHP Physics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_viscosity_constants import MU_WATER, RHO_WATER, G

def stokes_drag(mu, r, v): return 6 * math.pi * mu * r * v
def terminal_velocity(r, rho_sphere, rho_fluid, mu):
    return 2 * r**2 * (rho_sphere - rho_fluid) * G / (9 * mu)
def reynolds_number(rho, v, d, mu): return rho * v * d / mu

if __name__ == "__main__":
    vt = terminal_velocity(0.001, 7800, RHO_WATER, MU_WATER)
    Re = reynolds_number(RHO_WATER, vt, 0.002, MU_WATER)
    print(f"Steel sphere r=1mm in water: v_t={vt:.2f} m/s, Re={Re:.0f}")
    print(f"Re >> 1 → Stokes drag INVALID for this case")
