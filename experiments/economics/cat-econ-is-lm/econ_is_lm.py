"""IS-LM Model — CHP Economics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_is_lm_constants import A, c, t, b, k, h, M_P


def is_curve(Y, A=A, c=c, t=t, b=b):
    """IS curve: r = (A - Y*(1 - c*(1-t))) / b.  Slopes DOWN in (Y,r) space."""
    return (A - Y * (1 - c * (1 - t))) / b


def lm_curve(Y, k=k, h=h, M_P=M_P):
    """LM curve: r = (kY - M/P) / h.  Slopes UP in (Y,r) space."""
    return (k * Y - M_P) / h


def is_slope(c=c, t=t, b=b):
    """Slope of IS curve: -(1 - c*(1-t)) / b.  Always negative."""
    return -(1 - c * (1 - t)) / b


def lm_slope(k=k, h=h):
    """Slope of LM curve: k / h.  Always positive."""
    return k / h


def is_lm_equilibrium(A=A, c=c, t=t, b=b, k=k, h=h, M_P=M_P):
    """Solve IS = LM for equilibrium (Y*, r*).
    Y* = (hA + bM/P) / (h*(1-c(1-t)) + bk)
    r* = (kY* - M/P) / h
    """
    denom = h * (1 - c * (1 - t)) + b * k
    Y_star = (h * A + b * M_P) / denom
    r_star = (k * Y_star - M_P) / h
    return (Y_star, r_star)


if __name__ == "__main__":
    Y_eq, r_eq = is_lm_equilibrium()
    print(f"IS slope: {is_slope():.4f} (negative = downward)")
    print(f"LM slope: {lm_slope():.4f} (positive = upward)")
    print(f"Equilibrium: Y* = {Y_eq:.2f}, r* = {r_eq:.4f}")
