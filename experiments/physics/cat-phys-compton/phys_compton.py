"""Compton Scattering — CHP Physics Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_compton_constants import COMPTON_WAVELENGTH

def compton_shift(theta_deg):
    """Δλ = λ_C · (1 - cos θ). NOT λ_C · cos θ."""
    return COMPTON_WAVELENGTH * (1 - math.cos(math.radians(theta_deg)))

def scattered_wavelength(lambda_incident, theta_deg):
    """λ' = λ + Δλ."""
    return lambda_incident + compton_shift(theta_deg)

def max_shift():
    """Maximum shift at θ=180°: Δλ = 2λ_C."""
    return 2 * COMPTON_WAVELENGTH

if __name__ == "__main__":
    print(f"Compton wavelength: {COMPTON_WAVELENGTH:.4e} m")
    print(f"Shift at 90°: {compton_shift(90):.4e} m (= λ_C)")
    print(f"Shift at 180°: {compton_shift(180):.4e} m (= 2λ_C)")
    print(f"Shift at 0°: {compton_shift(0):.4e} m (= 0, forward)")
