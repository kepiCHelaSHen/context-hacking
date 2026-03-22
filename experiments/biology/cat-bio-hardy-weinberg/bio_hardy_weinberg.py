"""Hardy-Weinberg Equilibrium — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_hardy_weinberg_constants import *


def genotype_frequencies(p):
    """Return (freq_AA, freq_Aa, freq_aa) given allele frequency p."""
    q = 1 - p
    return (p ** 2, 2 * p * q, q ** 2)


def allele_freq_from_genotypes(n_AA, n_Aa, n_aa):
    """Back-calculate allele frequencies (p, q) from genotype counts."""
    total = n_AA + n_Aa + n_aa
    p = (2 * n_AA + n_Aa) / (2 * total)
    q = 1 - p
    return (p, q)


def hw_expected(p, n):
    """Return expected genotype counts (AA, Aa, aa) given p and total n."""
    aa_f, ab_f, bb_f = genotype_frequencies(p)
    return (aa_f * n, ab_f * n, bb_f * n)


def is_equilibrium(observed, expected, threshold=0.05):
    """Chi-squared goodness-of-fit test; return True if population is in HW equilibrium."""
    chi2 = sum((o - e) ** 2 / e for o, e in zip(observed, expected) if e > 0)
    # df = number of genotype classes - 1 - number of estimated parameters
    # For 3 classes with p estimated from data: df = 3 - 1 - 1 = 1
    # chi2 critical value at alpha=0.05, df=1 is 3.841
    return chi2 < 3.841


if __name__ == "__main__":
    freqs = genotype_frequencies(P)
    print(f"p={P}, q={Q}")
    print(f"AA={freqs[0]:.4f}, Aa={freqs[1]:.4f}, aa={freqs[2]:.4f}")
    print(f"Sum={sum(freqs):.4f}")
    p_back, q_back = allele_freq_from_genotypes(36, 48, 16)
    print(f"Back-calculated: p={p_back:.4f}, q={q_back:.4f}")
