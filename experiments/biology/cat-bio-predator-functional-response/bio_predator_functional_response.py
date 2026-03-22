"""Holling's Functional Response — Type I, II, III curves — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_predator_functional_response_constants import *


def type_I(a, N, N_max=None):
    """Type I functional response: f(N) = a*N (linear, capped at N_max if given).

    Predator consumption increases linearly with prey density, up to a maximum.
    """
    if N < 0:
        raise ValueError("Prey density N must be non-negative")
    result = a * N
    if N_max is not None and result > N_max:
        return N_max
    return result


def type_II(a, h, N):
    """Type II functional response: f(N) = a*N / (1 + a*h*N).

    Hyperbolic (decelerating) — consumption rises quickly then saturates.
    Handling time limits the maximum consumption rate to 1/h.
    """
    if N < 0:
        raise ValueError("Prey density N must be non-negative")
    return a * N / (1 + a * h * N)


def type_III(a, h, N):
    """Type III functional response: f(N) = a*N² / (1 + a*h*N²).

    SIGMOIDAL — accelerating at low N (quadratic), then saturating at high N.
    KEY: Uses N² (not N), giving the characteristic sigmoid shape.
    At low N: f ≈ a*N² (accelerating, concave up)
    At high N: f ≈ 1/h (saturating, same as Type II)
    """
    if N < 0:
        raise ValueError("Prey density N must be non-negative")
    N_sq = N * N
    return a * N_sq / (1 + a * h * N_sq)


def max_consumption_rate(h):
    """Maximum consumption rate = 1/h (shared by Type II and Type III).

    As prey density → ∞, both Type II and Type III approach this limit.
    """
    if h <= 0:
        raise ValueError("Handling time h must be positive")
    return 1.0 / h


if __name__ == "__main__":
    print(f"Attack rate a={A}, Handling time h={H}, Max rate 1/h={MAX_RATE}")
    print()
    print("Type I (linear):")
    for n in [1, 5, 10, 20]:
        print(f"  N={n:4d}  f(N) = {type_I(A, n):.4f}")
    print()
    print("Type II (hyperbolic, decelerating):")
    for n in [1, 3, 10, 50, 100]:
        print(f"  N={n:4d}  f(N) = {type_II(A, H, n):.4f}")
    print()
    print("Type III (sigmoidal, accelerating then decelerating):")
    for n in [1, 3, 10, 50, 100]:
        print(f"  N={n:4d}  f(N) = {type_III(A, H, n):.4f}")
    print()
    print(f"Max consumption rate = 1/h = {max_consumption_rate(H):.4f}")
