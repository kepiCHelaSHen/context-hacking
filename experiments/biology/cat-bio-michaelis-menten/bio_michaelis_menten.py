"""Michaelis-Menten Enzyme Kinetics — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_michaelis_menten_constants import *


def michaelis_menten(vmax, km, s):
    """Return reaction velocity v given Vmax, Km, and substrate concentration [S].

    v = Vmax * [S] / (Km + [S])
    """
    if s < 0:
        raise ValueError("Substrate concentration must be non-negative")
    return vmax * s / (km + s)


def at_km(vmax):
    """Return v when [S] = Km.  This is always Vmax/2, NOT Vmax."""
    return vmax / 2


def lineweaver_burk(vmax, km, s):
    """Return 1/v (Lineweaver-Burk transform) for given Vmax, Km, [S].

    1/v = (Km/Vmax)(1/[S]) + 1/Vmax
    """
    if s <= 0:
        raise ValueError("Substrate concentration must be positive for Lineweaver-Burk")
    v = michaelis_menten(vmax, km, s)
    return 1.0 / v


def km_from_lineweaver(slope, y_intercept):
    """Back-calculate Km from Lineweaver-Burk slope and y-intercept.

    slope = Km / Vmax,  y_intercept = 1 / Vmax
    => Km = slope / y_intercept
    """
    if y_intercept == 0:
        raise ValueError("y-intercept cannot be zero")
    return slope / y_intercept


if __name__ == "__main__":
    print(f"Vmax={VMAX} umol/min, Km={KM} mM")
    for s in [KM, 10, 50, 100]:
        v = michaelis_menten(VMAX, KM, s)
        print(f"  [S]={s:6.1f} mM -> v={v:.3f} umol/min")
    print(f"  v at [S]=Km: {at_km(VMAX):.3f} (= Vmax/2 = {VMAX/2})")
    print(f"Lineweaver-Burk: slope={LB_SLOPE}, y-int={LB_Y_INTERCEPT}, x-int={LB_X_INTERCEPT}")
    km_back = km_from_lineweaver(LB_SLOPE, LB_Y_INTERCEPT)
    print(f"  Back-calculated Km = {km_back:.3f} mM (expected {KM})")
