"""Logistic Growth — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_logistic_growth_constants import *


def logistic_N(r, K, N0, t):
    """Population size N(t) under logistic growth.

    N(t) = K / (1 + ((K - N0) / N0) * exp(-r * t))
    """
    return K / (1 + ((K - N0) / N0) * math.exp(-r * t))


def logistic_dNdt(r, K, N):
    """Instantaneous growth rate dN/dt = r * N * (1 - N/K)."""
    return r * N * (1 - N / K)


def inflection_N(K):
    """Population size at inflection point (where growth rate is maximum).

    Inflection is at N = K/2, NOT at N = K.
    """
    return K / 2


def max_growth_rate(r, K):
    """Maximum possible growth rate, occurring at N = K/2.

    dN/dt_max = r * K / 4
    """
    return r * K / 4


if __name__ == "__main__":
    print(f"r={R}, K={K}, N0={N0}")
    print(f"N(10) = {logistic_N(R, K, N0, 10):.4f}")
    print(f"N(20) = {logistic_N(R, K, N0, 20):.4f}")
    print(f"Inflection at N = {inflection_N(K):.1f}")
    print(f"Max growth rate = {max_growth_rate(R, K):.1f}")
    print(f"dN/dt at N=100: {logistic_dNdt(R, K, 100):.1f}")
    print(f"dN/dt at N=500: {logistic_dNdt(R, K, 500):.1f}")
    print(f"dN/dt at N=900: {logistic_dNdt(R, K, 900):.1f}")
