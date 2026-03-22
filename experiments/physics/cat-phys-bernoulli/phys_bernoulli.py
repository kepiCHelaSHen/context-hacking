"""Bernoulli's Equation — CHP Physics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from phys_bernoulli_constants import RHO_WATER, G

def continuity_v2(v1, A1, A2): return v1 * A1 / A2
def bernoulli_pressure_drop(rho, v1, v2): return 0.5 * rho * (v2**2 - v1**2)
def torricelli(h): return math.sqrt(2 * G * h)
def bernoulli_full(P1, rho, v1, h1, v2, h2):
    """P2 = P1 + ½ρ(v1²-v2²) + ρg(h1-h2)."""
    return P1 + 0.5*rho*(v1**2-v2**2) + rho*G*(h1-h2)

if __name__ == "__main__":
    v2 = continuity_v2(2.0, 0.01, 0.005)
    dp = bernoulli_pressure_drop(RHO_WATER, 2.0, v2)
    print(f"Pipe narrows: v2={v2:.1f} m/s, ΔP={dp:.1f} Pa")
    print(f"Torricelli (1m head): {torricelli(1.0):.3f} m/s")
