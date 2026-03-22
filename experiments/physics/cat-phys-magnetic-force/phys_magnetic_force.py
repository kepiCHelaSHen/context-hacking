"""Magnetic Force — CHP Physics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_magnetic_force_constants import E_CHARGE, M_PROTON, M_ELECTRON

def lorentz_force(q, v, B, theta_deg=90): return abs(q) * v * B * math.sin(math.radians(theta_deg))
def cyclotron_radius(m, v, q, B): return m * v / (abs(q) * B)
def cyclotron_frequency(q, B, m): return abs(q) * B / (2 * math.pi * m)
def force_on_wire(I, L, B, theta_deg=90): return I * L * B * math.sin(math.radians(theta_deg))

if __name__ == "__main__":
    F = lorentz_force(E_CHARGE, 1e6, 1.0)
    r = cyclotron_radius(M_PROTON, 1e6, E_CHARGE, 1.0)
    f = cyclotron_frequency(E_CHARGE, 1.0, M_PROTON)
    print(f"Proton at 1e6 m/s in 1T: F={F:.4e}N, r={r:.5f}m, f={f:.2e}Hz")
    print(f"Cyclotron freq independent of velocity!")
