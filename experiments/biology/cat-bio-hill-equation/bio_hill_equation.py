"""Hill Equation — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_hill_equation_constants import *


def hill_equation(L, Kd, n):
    """Return fractional saturation θ = L^n / (Kd^n + L^n)."""
    if L < 0:
        raise ValueError("Ligand concentration must be non-negative")
    if Kd <= 0:
        raise ValueError("Kd must be positive")
    Ln = L ** n
    Kdn = Kd ** n
    return Ln / (Kdn + Ln)


def is_cooperative(n):
    """Classify cooperativity from Hill coefficient n.

    Returns 'positive', 'negative', or 'none'.
    """
    if math.isclose(n, 1.0, rel_tol=1e-9):
        return "none"
    elif n > 1.0:
        return "positive"
    else:
        return "negative"


def half_saturation(Kd):
    """Return the ligand concentration at which θ = 0.5.

    For the Hill equation, θ = 0.5 when [L] = Kd, regardless of n.
    """
    return Kd


if __name__ == "__main__":
    print(f"Kd={KD}, n={N_HILL} (hemoglobin-like)")
    for L in [5.0, 10.0, 20.0]:
        theta = hill_equation(L, KD, N_HILL)
        print(f"  theta({L:.0f}) = {theta:.6f}")
    print(f"Cooperativity (n={N_HILL}): {is_cooperative(N_HILL)}")
    print(f"Cooperativity (n=1.0):   {is_cooperative(1.0)}")
    print(f"Cooperativity (n=0.5):   {is_cooperative(0.5)}")
    print(f"Half-saturation [L] = {half_saturation(KD)}")
