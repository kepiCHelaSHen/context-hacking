"""Lotka-Volterra Competition — CHP Biology Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_competition_constants import *


def dN1_dt(r1, N1, N2, K1, alpha12):
    """Growth rate of species 1.

    dN₁/dt = r₁ N₁ (1 - (N₁ + α₁₂ N₂) / K₁)
    α₁₂ is the competitive effect of species 2 ON species 1.
    """
    return r1 * N1 * (1 - (N1 + alpha12 * N2) / K1)


def dN2_dt(r2, N2, N1, K2, alpha21):
    """Growth rate of species 2.

    dN₂/dt = r₂ N₂ (1 - (N₂ + α₂₁ N₁) / K₂)
    α₂₁ is the competitive effect of species 1 ON species 2.
    """
    return r2 * N2 * (1 - (N2 + alpha21 * N1) / K2)


def can_coexist(K1, K2, alpha12, alpha21):
    """Check whether stable coexistence is possible.

    Coexistence requires BOTH conditions:
        α₁₂ < K₁/K₂   (species 1 not overwhelmed by species 2)
        α₂₁ < K₂/K₁   (species 2 not overwhelmed by species 1)

    Both inequalities must hold — each species' intraspecific competition
    must exceed the interspecific competition it experiences.
    """
    return alpha12 < K1 / K2 and alpha21 < K2 / K1


def equilibrium(K1, K2, alpha12, alpha21):
    """Coexistence equilibrium population sizes (N₁*, N₂*).

    N₁* = (K₁ - α₁₂ K₂) / (1 - α₁₂ α₂₁)
    N₂* = (K₂ - α₂₁ K₁) / (1 - α₁₂ α₂₁)

    Only valid when can_coexist() is True.
    Raises ValueError if coexistence conditions are not met.
    """
    if not can_coexist(K1, K2, alpha12, alpha21):
        raise ValueError("Coexistence conditions not met — equilibrium undefined")
    denom = 1 - alpha12 * alpha21
    n1_star = (K1 - alpha12 * K2) / denom
    n2_star = (K2 - alpha21 * K1) / denom
    return (n1_star, n2_star)


if __name__ == "__main__":
    print(f"r1={R1}, r2={R2}, K1={K1}, K2={K2}")
    print(f"α₁₂={ALPHA12}, α₂₁={ALPHA21}")
    print(f"Coexistence: {can_coexist(K1, K2, ALPHA12, ALPHA21)}")
    n1s, n2s = equilibrium(K1, K2, ALPHA12, ALPHA21)
    print(f"Equilibrium: N1*={n1s:.4f}, N2*={n2s:.4f}")
    print(f"dN1/dt at (100,50): {dN1_dt(R1, 100, 50, K1, ALPHA12):.4f}")
    print(f"dN2/dt at (100,50): {dN2_dt(R2, 50, 100, K2, ALPHA21):.4f}")
