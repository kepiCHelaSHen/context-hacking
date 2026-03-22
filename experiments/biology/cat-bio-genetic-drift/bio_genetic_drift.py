"""Wright-Fisher Genetic Drift — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_genetic_drift_constants import *


def fixation_probability(p0):
    """Fixation probability of a neutral allele with initial frequency p0.

    For neutral alleles under pure drift, P(fixation) = p0.
    NOT 1/(2N) — that is only for a new single-copy mutation where p0 = 1/(2N).
    """
    return p0


def heterozygosity(p):
    """Expected heterozygosity for allele frequency p: H = 2*p*(1-p)."""
    return 2 * p * (1 - p)


def het_after_t(H0, N, t):
    """Heterozygosity after t generations of drift in a population of N diploids.

    H(t) = H0 * (1 - 1/(2N))^t
    """
    return H0 * (1 - 1 / (2 * N)) ** t


def drift_variance(p, N):
    """Variance in allele-frequency change per generation under Wright-Fisher drift.

    Var(delta_p) = p*(1-p) / (2*N)
    """
    return p * (1 - p) / (2 * N)


if __name__ == "__main__":
    print(f"N={N} diploids, 2N={TWO_N} gene copies, p0={P0}")
    print(f"P(fixation)  = {fixation_probability(P0)}")
    print(f"P(loss)      = {1 - fixation_probability(P0)}")
    print(f"H0           = {heterozygosity(P0):.4f}")
    print(f"H({T_TEST})       = {het_after_t(H0, N, T_TEST):.4f}")
    print(f"Var(delta_p) = {drift_variance(P0, N):.4f}")
