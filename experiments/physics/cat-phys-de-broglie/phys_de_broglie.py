"""de Broglie Wavelength — CHP Physics Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_de_broglie_constants import H_PLANCK, M_ELECTRON, M_PROTON, E_CHARGE, C_LIGHT

def de_broglie_wavelength(mass, velocity):
    """λ = h/(mv) — non-relativistic."""
    return H_PLANCK / (mass * velocity)

def wavelength_from_KE(mass, KE_joules):
    """λ = h/√(2mKE). From KE = ½mv² → p = √(2mKE)."""
    return H_PLANCK / math.sqrt(2 * mass * KE_joules)

def wavelength_from_voltage(mass, charge, voltage):
    """λ = h/√(2m·qV). For charged particle accelerated through V."""
    return H_PLANCK / math.sqrt(2 * mass * charge * voltage)

def is_relativistic(mass, KE_joules):
    """Check if KE > 1% of rest energy."""
    rest_energy = mass * C_LIGHT**2
    return KE_joules > 0.01 * rest_energy

if __name__ == "__main__":
    lam = wavelength_from_voltage(M_ELECTRON, E_CHARGE, 100)
    print(f"Electron at 100V: λ = {lam*1e10:.3f} Å")
    lam_p = wavelength_from_voltage(M_PROTON, E_CHARGE, 100)
    print(f"Proton at 100V: λ = {lam_p*1e10:.5f} Å (much shorter — heavier)")
    print(f"Relativistic at 100eV? {is_relativistic(M_ELECTRON, 100*E_CHARGE)}")
