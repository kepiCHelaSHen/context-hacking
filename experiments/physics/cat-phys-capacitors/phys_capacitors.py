"""Capacitors — CHP Physics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_capacitors_constants import EPSILON_0, KAPPA

def parallel_plate_C(A, d, kappa=1.0): return kappa * EPSILON_0 * A / d
def series_capacitance(*caps): return 1.0 / sum(1.0/c for c in caps)
def parallel_capacitance(*caps): return sum(caps)
def energy(C, V): return 0.5 * C * V**2
def charge(C, V): return C * V

if __name__ == "__main__":
    Cs = series_capacitance(10e-6, 20e-6, 30e-6)
    Cp = parallel_capacitance(10e-6, 20e-6, 30e-6)
    print(f"Series: {Cs*1e6:.3f} μF (LESS than smallest)")
    print(f"Parallel: {Cp*1e6:.0f} μF (sum — opposite of resistors!)")
    print(f"Energy (100μF, 12V): {energy(100e-6, 12)*1000:.1f} mJ")
