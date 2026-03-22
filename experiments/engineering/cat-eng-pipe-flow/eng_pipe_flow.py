"""Hagen-Poiseuille Laminar Pipe Flow — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_pipe_flow_constants import RHO_WATER, MU_WATER, RE_CRIT


def hagen_poiseuille_Q(dP, d, mu, L):
    """Volumetric flow rate Q = πΔPd⁴/(128μL). Only valid for laminar flow."""
    return math.pi * dP * d**4 / (128 * mu * L)


def hagen_poiseuille_dP(Q, d, mu, L):
    """Pressure drop ΔP = 128μLQ/(πd⁴). Only valid for laminar flow."""
    return 128 * mu * L * Q / (math.pi * d**4)


def is_laminar(Re):
    """Return True if Reynolds number indicates laminar regime (Re < 2300)."""
    return Re < RE_CRIT


def avg_velocity(Q, d):
    """Average velocity v = Q / A where A = πd²/4."""
    return Q / (math.pi * d**2 / 4)


if __name__ == "__main__":
    mu, L, d, Q = 1e-3, 10.0, 0.02, 1e-5
    v = avg_velocity(Q, d)
    Re = RHO_WATER * v * d / mu
    dP = hagen_poiseuille_dP(Q, d, mu, L)
    print(f"v_avg = {v:.5f} m/s")
    print(f"Re    = {Re:.1f}  -> {'laminar' if is_laminar(Re) else 'TURBULENT'}")
    print(f"dP    = {dP:.2f} Pa")
