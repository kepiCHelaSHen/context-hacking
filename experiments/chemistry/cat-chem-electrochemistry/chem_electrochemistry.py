"""
Electrochemistry — CHP Chemistry Sprint
Cell potential, Nernst equation, equilibrium constants, Gibbs energy.
All constants from frozen spec.
"""
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from chem_electrochemistry_constants import F, R, T298, E0, RT_F_298


def cell_potential(cathode, anode):
    """E0_cell = E0(cathode) - E0(anode). CATHODE minus ANODE."""
    return E0[cathode] - E0[anode]


def nernst(E0_cell, n, Q, T_K=298.15):
    """Nernst equation: E = E0 - (RT/nF)*ln(Q). NOTE THE MINUS SIGN."""
    return E0_cell - (R * T_K / (n * F)) * math.log(Q)


def eq_constant_from_E0(E0_val, n, T_K=298.15):
    """K = exp(n*F*E0/(R*T))."""
    return math.exp(n * F * E0_val / (R * T_K))


def delta_G(E0_val, n):
    """Delta G = -n*F*E0. NOTE THE MINUS SIGN."""
    return -n * F * E0_val


if __name__ == "__main__":
    print("=== Electrochemistry ===\n")

    E_daniell = cell_potential("Cu2+/Cu", "Zn2+/Zn")
    print(f"Daniell cell (Cu/Zn):")
    print(f"  E0 = {E_daniell:.4f} V")
    print(f"  (cathode - anode, NOT anode - cathode)\n")

    E_nernst = nernst(E_daniell, 2, 0.01)
    print(f"Nernst at Q=0.01: E = {E_nernst:.4f} V (> E0 when Q<1)")
    E_nernst2 = nernst(E_daniell, 2, 100)
    print(f"Nernst at Q=100:  E = {E_nernst2:.4f} V (< E0 when Q>1)\n")

    dG = delta_G(E_daniell, 2)
    print(f"Delta G = {dG:.0f} J/mol (negative = spontaneous)")
    print(f"  = {dG/1000:.1f} kJ/mol")
