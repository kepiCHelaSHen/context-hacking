"""Natural Selection — CHP Biology Sprint."""
import sys, math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_natural_selection_constants import *


def fitness_values(s, h):
    """Return (w_AA, w_Aa, w_aa) under standard parameterization."""
    w_AA = 1.0
    w_Aa = 1.0 - h * s
    w_aa = 1.0 - s
    return (w_AA, w_Aa, w_aa)


def mean_fitness(p, w_AA, w_Aa, w_aa):
    """Mean population fitness w-bar = p^2 w_AA + 2pq w_Aa + q^2 w_aa."""
    q = 1.0 - p
    return p**2 * w_AA + 2 * p * q * w_Aa + q**2 * w_aa


def delta_p(p, w_AA, w_Aa, w_aa):
    """Change in allele frequency per generation (includes w-bar denominator)."""
    q = 1.0 - p
    w_bar = mean_fitness(p, w_AA, w_Aa, w_aa)
    return p * q * (p * (w_AA - w_Aa) + q * (w_Aa - w_aa)) / w_bar


def multiplicative_heterozygote(w_AA, w_aa):
    """Multiplicative (geometric-mean) heterozygote fitness: sqrt(w_AA * w_aa)."""
    return math.sqrt(w_AA * w_aa)


if __name__ == "__main__":
    wAA, wAa, waa = fitness_values(S, H)
    print(f"Fitness: w_AA={wAA}, w_Aa={wAa}, w_aa={waa}")
    wAa_mult = multiplicative_heterozygote(wAA, waa)
    print(f"Additive w_Aa={wAa:.4f}  vs  Multiplicative w_Aa={wAa_mult:.4f}")
    print(f"  -> Difference = {abs(wAa - wAa_mult):.4f} (NOT zero for s={S})")
    w_bar = mean_fitness(P_TEST, wAA, wAa, waa)
    dp = delta_p(P_TEST, wAA, wAa, waa)
    print(f"p={P_TEST}: w_bar={w_bar:.4f}, delta_p={dp:.6f}")
