"""Diffraction — CHP Physics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_diffraction_constants import LAMBDA_HENE

def single_slit_minima(a, wavelength, m): return math.asin(m * wavelength / a)
def double_slit_maxima(d, wavelength, m): return math.asin(m * wavelength / d)
def rayleigh_criterion(wavelength, D): return 1.22 * wavelength / D
def central_max_width(wavelength, a, L): return 2 * L * wavelength / a

if __name__ == "__main__":
    theta = single_slit_minima(1e-4, LAMBDA_HENE, 1)
    print(f"Single slit 1st min: {math.degrees(theta):.4f}°")
    print(f"Rayleigh (1cm aperture): {rayleigh_criterion(LAMBDA_HENE, 0.01)*1e6:.1f} μrad")
