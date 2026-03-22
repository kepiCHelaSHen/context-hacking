"""Enzyme Inhibition — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_enzyme_inhibition_constants import *


def competitive(vmax, km, s, i, ki):
    """Competitive inhibition: inhibitor competes with substrate for active site.

    v = Vmax * [S] / (Km * (1 + [I]/Ki) + [S])
    Apparent Km increases; Vmax unchanged.
    """
    if s < 0:
        raise ValueError("Substrate concentration must be non-negative")
    if ki <= 0:
        raise ValueError("Ki must be positive")
    return vmax * s / (km * (1.0 + i / ki) + s)


def uncompetitive(vmax, km, s, i, ki):
    """Uncompetitive inhibition: inhibitor binds ES complex only.

    v = Vmax * [S] / (Km + [S] * (1 + [I]/Ki))
    Apparent Km DECREASES; apparent Vmax DECREASES.
    """
    if s < 0:
        raise ValueError("Substrate concentration must be non-negative")
    if ki <= 0:
        raise ValueError("Ki must be positive")
    return vmax * s / (km + s * (1.0 + i / ki))


def noncompetitive(vmax, km, s, i, ki):
    """Noncompetitive inhibition: inhibitor binds free enzyme and ES equally.

    v = Vmax * [S] / ((Km + [S]) * (1 + [I]/Ki))
    Km unchanged; Vmax decreases.
    """
    if s < 0:
        raise ValueError("Substrate concentration must be non-negative")
    if ki <= 0:
        raise ValueError("Ki must be positive")
    return vmax * s / ((km + s) * (1.0 + i / ki))


def apparent_km_competitive(km, i, ki):
    """Apparent Km under competitive inhibition: Km * (1 + [I]/Ki).

    Always >= Km (increases with inhibitor).
    """
    return km * (1.0 + i / ki)


def apparent_km_uncompetitive(km, i, ki):
    """Apparent Km under uncompetitive inhibition: Km / (1 + [I]/Ki).

    Always <= Km (DECREASES with inhibitor — this is the key distinction!).
    """
    return km / (1.0 + i / ki)


def apparent_vmax_uncompetitive(vmax, i, ki):
    """Apparent Vmax under uncompetitive inhibition: Vmax / (1 + [I]/Ki).

    Both Km and Vmax decrease by the same factor, preserving slope in L-B plot.
    """
    return vmax / (1.0 + i / ki)


if __name__ == "__main__":
    print(f"Parameters: Vmax={VMAX}, Km={KM}, Ki={KI}, [I]={I}")
    print(f"Alpha = 1 + [I]/Ki = {ALPHA}")
    print()
    for s in [5, 10, 20]:
        v_u = VMAX * s / (KM + s)
        v_c = competitive(VMAX, KM, s, I, KI)
        v_uc = uncompetitive(VMAX, KM, s, I, KI)
        v_nc = noncompetitive(VMAX, KM, s, I, KI)
        print(f"  [S]={s:4.0f}  uninhibited={v_u:.3f}  competitive={v_c:.3f}"
              f"  uncompetitive={v_uc:.3f}  noncompetitive={v_nc:.3f}")
    print()
    print(f"Competitive:    Km_app={apparent_km_competitive(KM, I, KI):.1f} (Vmax unchanged)")
    print(f"Uncompetitive:  Km_app={apparent_km_uncompetitive(KM, I, KI):.1f}"
          f"  Vmax_app={apparent_vmax_uncompetitive(VMAX, I, KI):.1f}")
