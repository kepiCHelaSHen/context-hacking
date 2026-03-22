"""Photoelectric Effect — CHP Physics Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_photoelectric_constants import H_PLANCK, C_LIGHT, E_CHARGE, WORK_FUNCTION, EV_TO_J

def photon_energy_wavelength(wavelength_m):
    """E = hc/λ."""
    return H_PLANCK * C_LIGHT / wavelength_m

def photon_energy_frequency(frequency_Hz):
    """E = hf."""
    return H_PLANCK * frequency_Hz

def ke_max(wavelength_m, material):
    """KE_max = hc/λ - φ. Returns in Joules. Negative means no emission."""
    phi_J = WORK_FUNCTION[material] * EV_TO_J
    return H_PLANCK * C_LIGHT / wavelength_m - phi_J

def threshold_wavelength(material):
    """λ_0 = hc/φ."""
    phi_J = WORK_FUNCTION[material] * EV_TO_J
    return H_PLANCK * C_LIGHT / phi_J

def threshold_frequency(material):
    """f_0 = φ/h."""
    phi_J = WORK_FUNCTION[material] * EV_TO_J
    return phi_J / H_PLANCK

def stopping_potential(wavelength_m, material):
    """V_stop = KE_max / e."""
    ke = ke_max(wavelength_m, material)
    return max(ke / E_CHARGE, 0.0)

if __name__ == "__main__":
    ke = ke_max(400e-9, "Na")
    print(f"Na at 400nm: KE_max = {ke/EV_TO_J:.3f} eV")
    lam0 = threshold_wavelength("Na")
    print(f"Na threshold: {lam0*1e9:.1f} nm")
    print(f"Intensity increases # electrons, NOT their KE")
