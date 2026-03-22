"""Thermal Expansion — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_thermal_expansion_constants import *

def linear_expansion(alpha, L0, dT):
    """dL = alpha * L0 * dT"""
    return alpha * L0 * dT

def volumetric_expansion(alpha, V0, dT):
    """dV = 3*alpha * V0 * dT  (beta = 3*alpha for isotropic materials)"""
    return 3 * alpha * V0 * dT

def area_expansion(alpha, A0, dT):
    """dA = 2*alpha * A0 * dT  (gamma = 2*alpha for isotropic materials)"""
    return 2 * alpha * A0 * dT

def volumetric_coefficient(alpha):
    """beta = 3 * alpha for isotropic materials"""
    return 3 * alpha

if __name__ == "__main__":
    dL = linear_expansion(ALPHA_STEEL, L0_STEEL, DT_TEST)
    dV = volumetric_expansion(ALPHA_STEEL, V0_STEEL, DT_TEST)
    dA = area_expansion(ALPHA_STEEL, A0_STEEL, DT_TEST)
    beta = volumetric_coefficient(ALPHA_STEEL)
    print(f"Steel rod L0={L0_STEEL}m, dT={DT_TEST}C:")
    print(f"  Linear:  dL = {dL:.6f} m = {dL*1000:.2f} mm")
    print(f"  Area:    dA = {dA:.6f} m^2  (gamma=2*alpha={2*ALPHA_STEEL:.2e})")
    print(f"  Volume:  dV = {dV:.6f} m^3  (beta=3*alpha={beta:.2e})")
    print(f"  WRONG volume (using alpha): {ALPHA_STEEL * V0_STEEL * DT_TEST:.6f} m^3 (3x too small!)")
