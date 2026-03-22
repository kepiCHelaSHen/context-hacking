"""Gompertz Growth Model — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_gompertz_constants import *


def gompertz_N(K, alpha, N0, t):
    """Population size at time t under Gompertz growth.

    N(t) = K * exp(ln(N0/K) * exp(-alpha * t))
    """
    return K * math.exp(math.log(N0 / K) * math.exp(-alpha * t))


def gompertz_dNdt(alpha, K, N):
    """Instantaneous growth rate dN/dt = -alpha * N * ln(N/K).

    Note: uses ln(N/K), NOT (1 - N/K) as in the logistic model.
    """
    if N <= 0:
        return 0.0
    return -alpha * N * math.log(N / K)


def gompertz_inflection(K):
    """Population size at the inflection point: N = K/e.

    This is where growth rate dN/dt is maximal.
    Gompertz inflection is at K/e ≈ 0.3679*K, NOT K/2.
    """
    return K / math.e


if __name__ == "__main__":
    print(f"Gompertz growth: K={K}, alpha={ALPHA}, N0={N0}")
    for t in [0, 10, 20, 30, 40, 50, 60, 80, 100]:
        n = gompertz_N(K, ALPHA, N0, t)
        rate = gompertz_dNdt(ALPHA, K, n)
        print(f"  t={t:3d}  N={n:10.4f}  dN/dt={rate:8.4f}")
    print(f"Inflection at N = K/e = {gompertz_inflection(K):.4f}")
