"""Bohr Model of Hydrogen — CHP Physics Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_bohr_model_constants import R_INF, RY_EV, A0

def energy_level(n):
    """E_n = -13.606/n² eV. NEGATIVE for bound states."""
    return -RY_EV / n**2

def transition_wavelength(n_upper, n_lower):
    """1/λ = R_inf · (1/n_lower² - 1/n_upper²). Returns wavelength in meters."""
    inv_lambda = R_INF * (1.0/n_lower**2 - 1.0/n_upper**2)
    return 1.0 / inv_lambda

def transition_energy(n_upper, n_lower):
    """ΔE = E_upper - E_lower (positive for emission when n_upper > n_lower)."""
    return energy_level(n_lower) - energy_level(n_upper)

def orbital_radius(n):
    """r_n = n²·a₀."""
    return n**2 * A0

def series_limit(n_lower):
    """Series limit wavelength: 1/λ = R_inf/n_lower²."""
    return n_lower**2 / R_INF

if __name__ == "__main__":
    print(f"E1 = {energy_level(1):.3f} eV (ground state, NEGATIVE)")
    print(f"E2 = {energy_level(2):.3f} eV")
    print(f"Hα (3→2): λ = {transition_wavelength(3,2)*1e9:.1f} nm (red)")
    print(f"Lyman α (2→1): λ = {transition_wavelength(2,1)*1e9:.1f} nm (UV)")
    print(f"Bohr radius: {A0*1e10:.4f} Å")
