"""Atmospheric Pressure (Barometric Formula) — CHP Earth Science Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_atmospheric_pressure_constants import R_GAS, T_STD, M_AIR, G_STD, P0, H_SCALE

def scale_height(T, M, g):
    """H = RT / (Mg). Scale height of the atmosphere in metres."""
    return R_GAS * T / (M * g)

def barometric_pressure(P0, h, H):
    """P(h) = P₀ · exp(−h/H). Pressure at altitude h given scale height H."""
    return P0 * math.exp(-h / H)

def altitude_from_pressure(P, P0, H):
    """h = −H · ln(P/P₀). Invert barometric formula to get altitude."""
    return -H * math.log(P / P0)

def pressure_ratio(h, H):
    """P/P₀ = exp(−h/H). Dimensionless pressure ratio."""
    return math.exp(-h / H)

if __name__ == "__main__":
    print(f"Scale height (std atm): {H_SCALE:.2f} m")
    print(f"P(5500 m): {barometric_pressure(P0, 5500, H_SCALE):.1f} Pa")
    print(f"P(Everest, 8848 m): {barometric_pressure(P0, 8848, H_SCALE):.1f} Pa")
    print(f"Altitude for 50000 Pa: {altitude_from_pressure(50000, P0, H_SCALE):.1f} m")
