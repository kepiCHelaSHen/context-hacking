"""Heat Transfer — CHP Physics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_heat_transfer_constants import STEFAN_BOLTZMANN, K_COPPER

def conduction(k, A, T1, T2, L): return k * A * (T1 - T2) / L
def radiation(epsilon, A, T_surface, T_surr):
    """q = εσA(T⁴ - T_surr⁴). T in KELVIN."""
    return epsilon * STEFAN_BOLTZMANN * A * (T_surface**4 - T_surr**4)
def convection(h, A, T_surface, T_fluid): return h * A * (T_surface - T_fluid)

if __name__ == "__main__":
    q_rad = radiation(1.0, 1.0, 500, 300)
    print(f"Radiation 500K→300K: {q_rad:.1f} W (uses T⁴, NOT T)")
    q_cond = conduction(K_COPPER, 0.01, 400, 300, 0.1)
    print(f"Copper conduction: {q_cond:.1f} W")
