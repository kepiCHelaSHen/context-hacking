"""Simpson's Diversity Index — CHP Biology Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_simpson_diversity_constants import *


def simpson_D(counts):
    """Compute Simpson's D = sum(p_i^2). This is DOMINANCE, not diversity.
    Higher D means the community is MORE dominated (LESS diverse)."""
    total = sum(counts)
    return sum((c / total) ** 2 for c in counts)


def simpson_diversity(counts):
    """Compute Gini-Simpson diversity = 1 - D. Higher = more diverse."""
    return 1 - simpson_D(counts)


def simpson_reciprocal(counts):
    """Compute Simpson's reciprocal = 1/D. Higher = more diverse. Range [1, S]."""
    d = simpson_D(counts)
    return 1 / d


def effective_species(reciprocal):
    """The reciprocal index IS the effective number of equally-common species."""
    return reciprocal


if __name__ == "__main__":
    d = simpson_D(COUNTS)
    div = simpson_diversity(COUNTS)
    rec = simpson_reciprocal(COUNTS)
    print(f"Counts: {COUNTS}, N={N}")
    print(f"Simpson's D (dominance):    {d:.6f}")
    print(f"Gini-Simpson (1-D):         {div:.6f}")
    print(f"Simpson's Reciprocal (1/D): {rec:.6f}")
    print(f"Effective species:          {effective_species(rec):.2f}")
