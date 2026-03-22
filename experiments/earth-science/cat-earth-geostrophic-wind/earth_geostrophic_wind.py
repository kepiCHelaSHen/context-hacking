"""Geostrophic Wind — CHP Earth Science Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_geostrophic_wind_constants import *

def pressure_gradient(dP, dx): return dP / dx
def geostrophic_speed(dP_dx, rho, f): return abs(1.0 / (rho * f) * dP_dx)
def wind_direction_nh(): return "low to left"
def wind_direction_sh(): return "low to right"

if __name__ == "__main__":
    grad = pressure_gradient(DP_TEST, DX_TEST)
    vg = geostrophic_speed(grad, RHO_AIR, F_TEST)
    print(f"phi={PHI_TEST} deg N  f={F_TEST:.6e} 1/s")
    print(f"dP/dx={grad:.4e} Pa/m  ->  v_g={vg:.2f} m/s")
    print(f"NH direction: low pressure to the {wind_direction_nh()} of the wind")
    print(f"SH direction: low pressure to the {wind_direction_sh()} of the wind")
