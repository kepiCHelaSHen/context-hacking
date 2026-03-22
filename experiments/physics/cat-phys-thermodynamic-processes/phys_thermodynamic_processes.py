"""Thermodynamic Processes — CHP Physics Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_thermodynamic_processes_constants import R, GAMMA_MONO, GAMMA_DI

def isothermal_work(n, T, V1, V2):
    """W = nRT·ln(V2/V1). Positive when gas expands."""
    return n * R * T * math.log(V2 / V1)

def adiabatic_final_T(T1, V1, V2, gamma):
    """T2 = T1·(V1/V2)^(γ-1)."""
    return T1 * (V1 / V2) ** (gamma - 1)

def adiabatic_work(n, T1, T2, gamma):
    """W = nCv(T1-T2) = nR(T1-T2)/(γ-1)."""
    return n * R * (T1 - T2) / (gamma - 1)

def isobaric_work(n, T1, T2):
    """W = nRΔT = P·ΔV."""
    return n * R * (T2 - T1)

def isochoric_work():
    """W = 0 (constant volume)."""
    return 0.0

def cv_from_gamma(gamma):
    """Cv = R/(γ-1)."""
    return R / (gamma - 1)

def cp_from_gamma(gamma):
    """Cp = γR/(γ-1) = Cv + R."""
    return gamma * R / (gamma - 1)

if __name__ == "__main__":
    W = isothermal_work(1.0, 300, 0.001, 0.002)
    print(f"Isothermal expansion 1L->2L at 300K: W = {W:.1f} J")
    T2 = adiabatic_final_T(300, 0.001, 0.002, GAMMA_DI)
    print(f"Adiabatic expansion (diatomic): T2 = {T2:.1f} K")
