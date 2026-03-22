"""Faraday's Law — CHP Physics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_faraday_induction_constants import *

def faraday_emf(N, dPhi_dt): return -N * dPhi_dt
def flux(B, A, theta_deg=0): return B * A * math.cos(math.radians(theta_deg))
def motional_emf(B, L, v): return B * L * v
def emf_changing_B(N, A, B1, B2, dt): return -N * A * (B2 - B1) / dt

if __name__ == "__main__":
    emf = emf_changing_B(N_COIL, A_COIL, B_INITIAL, B_FINAL, DT)
    print(f"Coil EMF: {emf:.1f} V (Lenz's law: MINUS sign)")
    emf_m = motional_emf(B_ROD, L_ROD, V_ROD)
    print(f"Motional EMF: {emf_m:.1f} V")
