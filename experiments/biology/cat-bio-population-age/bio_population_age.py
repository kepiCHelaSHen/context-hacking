"""Leslie Matrix — Stable Age Distribution — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_population_age_constants import *


def leslie_multiply(L, n):
    """Matrix-vector product L × n for a Leslie matrix."""
    size = len(n)
    return [sum(L[i][j] * n[j] for j in range(size)) for i in range(size)]


def project(L, n0, steps):
    """Project population forward, returning list of population vectors [n0, n1, ..., n_steps]."""
    history = [list(n0)]
    n = list(n0)
    for _ in range(steps):
        n = leslie_multiply(L, n)
        history.append(n)
    return history


def growth_rate_numerical(L, n0, steps=100):
    """Estimate asymptotic growth rate λ from ratio of total population at large t."""
    n = list(n0)
    for _ in range(steps):
        n_new = leslie_multiply(L, n)
        n = n_new
    # One more step to compute ratio
    n_next = leslie_multiply(L, n)
    total_now = sum(n)
    total_next = sum(n_next)
    if total_now == 0:
        return 0.0
    return total_next / total_now


def is_growing(lam):
    """Return True if population is growing (λ > 1)."""
    return lam > 1.0


if __name__ == "__main__":
    print("Leslie Matrix — Population Age Structure")
    print(f"L = {LESLIE_MATRIX}")
    print(f"n0 = {N0}")

    # One-step projection
    n1 = leslie_multiply(LESLIE_MATRIX, N0)
    print(f"n1 = L × n0 = {n1}")

    # Multi-step projection
    history = project(LESLIE_MATRIX, N0, 20)
    for t, n in enumerate(history[:6]):
        total = sum(n)
        print(f"  t={t}: n={[f'{x:.1f}' for x in n]}, total={total:.1f}")

    # Growth rate
    lam = growth_rate_numerical(LESLIE_MATRIX, N0, steps=200)
    r = math.log(lam)
    print(f"\nEstimated λ = {lam:.10f}")
    print(f"Intrinsic rate r = ln(λ) = {r:.10f}")
    print(f"Population is {'growing' if is_growing(lam) else 'declining or stable'}")
    print(f"\nNOTE: λ ({lam:.4f}) ≠ r ({r:.4f}) — they are different quantities!")
