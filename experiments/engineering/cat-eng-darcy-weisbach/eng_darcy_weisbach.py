"""Darcy-Weisbach Pipe Friction — CHP Engineering Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_darcy_weisbach_constants import *


def darcy_friction_laminar(Re):
    """Darcy friction factor for laminar flow: f_D = 64/Re."""
    return 64.0 / Re


def fanning_friction_laminar(Re):
    """Fanning friction factor for laminar flow: f_F = 16/Re = f_D/4."""
    return 16.0 / Re


def head_loss_darcy(f_D, L, D, v, g=9.81):
    """Head loss via Darcy-Weisbach: h_f = f_D * (L/D) * (v^2 / (2*g)).

    IMPORTANT: f_D must be the DARCY friction factor, not Fanning!
    """
    return f_D * (L / D) * (v**2 / (2.0 * g))


def darcy_to_fanning(f_D):
    """Convert Darcy friction factor to Fanning: f_F = f_D / 4."""
    return f_D / 4.0


if __name__ == "__main__":
    Re = 1000.0
    L, D, v, g = 10.0, 0.05, 1.0, 9.81

    f_D = darcy_friction_laminar(Re)
    f_F = fanning_friction_laminar(Re)
    print(f"Re = {Re}")
    print(f"Darcy   f_D = 64/Re = {f_D}")
    print(f"Fanning f_F = 16/Re = {f_F}  (4x smaller!)")
    print(f"f_D / f_F = {f_D / f_F}")
    print()

    hf = head_loss_darcy(f_D, L, D, v, g)
    print(f"Head loss (correct, Darcy f):  h_f = {hf:.6f} m")

    hf_wrong = head_loss_darcy(f_F, L, D, v, g)
    print(f"Head loss (WRONG, Fanning f):  h_f = {hf_wrong:.6f} m  (4x too small!)")
    print(f"Ratio correct/wrong = {hf / hf_wrong:.1f}")
