"""Phillips Curve — CHP Economics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_phillips_curve_constants import BETA, U_N, PI_E

def short_run_phillips(pi_e, beta, u, u_n):
    """Short-run Phillips curve: π = πᵉ - β(u - uₙ)."""
    return pi_e - beta * (u - u_n)

def is_long_run(u, u_n, tol=0.01):
    """Check if economy is at long-run equilibrium (u ≈ uₙ)."""
    return abs(u - u_n) <= tol

def long_run_inflation(pi_e):
    """Long-run inflation: π = πᵉ (NO tradeoff — vertical curve!)."""
    return pi_e

def nairu():
    """Return NAIRU (natural rate of unemployment)."""
    return U_N

if __name__ == "__main__":
    for u in [3.0, 5.0, 7.0]:
        pi = short_run_phillips(PI_E, BETA, u, U_N)
        lr = is_long_run(u, U_N)
        tag = " <- NAIRU (long-run equilibrium)" if lr else ""
        print(f"u={u:.0f}%: pi={pi:.1f}%{tag}")
    print(f"\nLong-run inflation (pi_e={PI_E}%): {long_run_inflation(PI_E):.1f}%")
    print(f"NAIRU: {nairu():.1f}%")
    print("\nKEY: Long-run Phillips curve is VERTICAL at u_n -- NO permanent tradeoff!")
