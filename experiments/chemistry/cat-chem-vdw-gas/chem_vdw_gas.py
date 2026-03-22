"""
Van der Waals Real Gas — CHP Chemistry Sprint
Ideal vs VdW pressure, compression factor, critical constants.
All constants from frozen spec.
"""
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from chem_vdw_gas_constants import R_ATM, VDW


def ideal_gas_P(n, V_L, T_K):
    """Ideal gas law: P = nRT/V."""
    return n * R_ATM * T_K / V_L


def vdw_P(n, V_L, T_K, gas):
    """Van der Waals: P = nRT/(V-nb) - n^2*a/V^2. CRITICAL: n**2 in attraction term."""
    a = VDW[gas]["a"]
    b = VDW[gas]["b"]
    return n * R_ATM * T_K / (V_L - n * b) - n**2 * a / V_L**2


def compression_factor(P, V, n, T):
    """Z = PV/(nRT). Z=1 for ideal gas."""
    return P * V / (n * R_ATM * T)


def critical_temperature(gas):
    """Tc = 8a/(27Rb). NOT a/(Rb)."""
    a = VDW[gas]["a"]
    b = VDW[gas]["b"]
    return 8.0 * a / (27.0 * R_ATM * b)


def critical_pressure(gas):
    """Pc = a/(27b^2). NOT a/b^2."""
    a = VDW[gas]["a"]
    b = VDW[gas]["b"]
    return a / (27.0 * b**2)


if __name__ == "__main__":
    print("=== Van der Waals Real Gas ===\n")

    P_ideal = ideal_gas_P(1, 0.5, 500)
    P_vdw = vdw_P(1, 0.5, 500, "CO2")
    print(f"CO2 at 1 mol, 0.5L, 500K:")
    print(f"  Ideal: {P_ideal:.2f} atm")
    print(f"  VdW:   {P_vdw:.2f} atm")
    print(f"  Deviation: {abs(P_ideal-P_vdw)/P_ideal*100:.1f}%\n")

    Tc = critical_temperature("CO2")
    Pc = critical_pressure("CO2")
    print(f"CO2 critical constants:")
    print(f"  Tc = {Tc:.1f} K (literature: 304.2 K)")
    print(f"  Pc = {Pc:.1f} atm")
