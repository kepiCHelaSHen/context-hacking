"""Angular Momentum — CHP Physics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_angular_momentum_constants import *

def angular_momentum_rotation(I, omega): return I * omega
def angular_momentum_particle(m, v, r, theta_deg=90): return m * v * r * math.sin(math.radians(theta_deg))
def conservation_omega(I1, omega1, I2): return I1 * omega1 / I2
def rotational_ke(I, omega): return 0.5 * I * omega**2

if __name__ == "__main__":
    omega2 = conservation_omega(I1_SKATER, OMEGA1_SKATER, I2_SKATER)
    print(f"Skater: ω1={OMEGA1_SKATER}, ω2={omega2} rad/s (L conserved, KE NOT)")
    print(f"KE1={rotational_ke(I1_SKATER,OMEGA1_SKATER):.1f}J KE2={rotational_ke(I2_SKATER,omega2):.1f}J")
