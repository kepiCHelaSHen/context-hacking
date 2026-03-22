"""Kirchhoff's Circuit Laws — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_ohm_kirchhoff_constants import *

def series_resistance(*Rs): return sum(Rs)
def parallel_resistance(*Rs): return 1.0 / sum(1.0/r for r in Rs)
def ohms_law_current(V, R): return V / R
def kvl_check(voltages, tol=1e-9): return abs(sum(voltages)) < tol
def voltage_divider(V, R1, R2): return V * R2 / (R1 + R2)

if __name__ == "__main__":
    I = ohms_law_current(V_SOURCE, series_resistance(R1, R2, R3))
    drops = [V_SOURCE, -I*R1, -I*R2, -I*R3]
    print(f"Series: R_total={series_resistance(R1,R2,R3):.0f} ohm, I={I:.1f} A")
    print(f"KVL loop: {drops} -> sum={sum(drops):.1f} (must be 0)")
    print(f"Parallel (6,3): {parallel_resistance(R_A, R_B):.1f} ohm")
    print(f"Divider (10V, 4/6): {voltage_divider(V_DIV_IN, R_DIV1, R_DIV2):.1f} V")
