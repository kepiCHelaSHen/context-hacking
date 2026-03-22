"""Goodwin Oscillator (Circadian Rhythm) — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_circadian_constants import *


def hill_repression(Z, K_val, n):
    """Hill repression function: K^n / (K^n + Z^n).

    Returns the fraction of maximal transcription when repressor
    concentration is Z, half-max constant is K_val, and Hill
    coefficient is n.
    """
    if Z < 0:
        raise ValueError("Repressor concentration Z must be non-negative")
    if K_val <= 0:
        raise ValueError("Half-max constant K must be positive")
    if n <= 0:
        raise ValueError("Hill coefficient n must be positive")
    Kn = K_val ** n
    Zn = Z ** n
    return Kn / (Kn + Zn)


def goodwin_derivatives(X, Y, Z, k1, k2, k3, k4, k5, k6, K_val, n):
    """Compute derivatives for the 3-variable Goodwin oscillator.

    dX/dt = k1 * K^n/(K^n + Z^n) - k2 * X   (mRNA)
    dY/dt = k3 * X - k4 * Y                   (protein)
    dZ/dt = k5 * Y - k6 * Z                   (nuclear effector)

    Returns (dX, dY, dZ).
    """
    h = hill_repression(Z, K_val, n)
    dX = k1 * h - k2 * X
    dY = k3 * X - k4 * Y
    dZ = k5 * Y - k6 * Z
    return (dX, dY, dZ)


def min_hill_for_oscillation():
    """Return the minimum integer Hill coefficient for sustained oscillations
    in the basic 3-variable Goodwin model.

    The theoretical threshold is n > 8 (Griffith 1968).
    The smallest integer satisfying this is n = 9.
    """
    return MIN_HILL_INTEGER


def can_oscillate(n):
    """Return True if Hill coefficient n permits sustained oscillations
    in the basic 3-variable Goodwin model.

    Requires n > 8 (strictly). Values n <= 8 give only damped oscillations
    that spiral to a stable fixed point.
    """
    return n > HILL_THRESHOLD


if __name__ == "__main__":
    print(f"Goodwin Oscillator — Circadian Rhythm Model")
    print(f"Parameters: k1={K1}, k2={K2}, k3={K3}, k4={K4}, k5={K5}, k6={K6}, K={K}")
    print()

    # Hill repression examples
    for z_val in [0.0, 0.5, 1.0, 2.0]:
        h = hill_repression(z_val, K, N_OSCILLATION)
        print(f"  h(Z={z_val}, K={K}, n={N_OSCILLATION}) = {h:.6f}")
    print()

    # Derivatives at (1,1,1)
    dX, dY, dZ = goodwin_derivatives(1, 1, 1, K1, K2, K3, K4, K5, K6, K, N_OSCILLATION)
    print(f"  Derivatives at (1,1,1), n={N_OSCILLATION}: dX={dX:.4f}, dY={dY:.4f}, dZ={dZ:.4f}")
    print()

    # Oscillation check
    print(f"  min_hill_for_oscillation() = {min_hill_for_oscillation()}")
    for n_test in [1, 2, 3, 8, 9, 10, 20]:
        print(f"  can_oscillate(n={n_test}) = {can_oscillate(n_test)}")
