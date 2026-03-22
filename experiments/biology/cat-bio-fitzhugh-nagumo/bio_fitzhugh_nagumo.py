"""FitzHugh-Nagumo Model — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_fitzhugh_nagumo_constants import *


def dv_dt(v, w, I_ext=0):
    """Fast variable derivative: dv/dt = v - v^3/3 - w + I_ext."""
    return v - v**3 / 3 - w + I_ext


def dw_dt(v, w, a=0.7, b=0.8, eps=0.08):
    """Slow variable derivative: dw/dt = eps*(v + a - b*w)."""
    return eps * (v + a - b * w)


def v_nullcline(v, I_ext=0):
    """v-nullcline: w = v - v^3/3 + I_ext (CUBIC)."""
    return v - v**3 / 3 + I_ext


def w_nullcline(v, a=0.7, b=0.8):
    """w-nullcline: w = (v + a) / b (LINEAR)."""
    return (v + a) / b


if __name__ == "__main__":
    print(f"FitzHugh-Nagumo: a={A}, b={B}, eps={EPS}, I_ext={I_EXT}")
    print(f"Fixed point: v={V_FP:.6f}, w={W_FP:.6f}")
    print(f"  dv/dt at FP = {dv_dt(V_FP, W_FP, I_EXT):.8f}")
    print(f"  dw/dt at FP = {dw_dt(V_FP, W_FP, A, B, EPS):.8f}")
    print()
    print("v-nullcline (cubic) at sample points:")
    for v in [-2.0, -1.0, 0.0, 1.0, 2.0]:
        print(f"  v={v:5.1f}  ->  w={v_nullcline(v):.5f}")
    print("w-nullcline (linear) at sample points:")
    for v in [-2.0, -1.0, 0.0, 1.0, 2.0]:
        print(f"  v={v:5.1f}  ->  w={w_nullcline(v):.5f}")
