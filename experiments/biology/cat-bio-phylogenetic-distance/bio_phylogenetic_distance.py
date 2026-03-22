"""Jukes-Cantor Phylogenetic Distance — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_phylogenetic_distance_constants import *


def count_differences(seq1, seq2):
    """Count the number of nucleotide differences between two aligned sequences."""
    if len(seq1) != len(seq2):
        raise ValueError("Sequences must be the same length")
    return sum(1 for a, b in zip(seq1, seq2) if a != b)


def raw_distance(seq1, seq2):
    """Compute raw (uncorrected) distance p = differences / alignment length."""
    n = len(seq1)
    if n == 0:
        raise ValueError("Sequences must not be empty")
    return count_differences(seq1, seq2) / n


def jukes_cantor(p):
    """Apply the Jukes-Cantor correction: d = -(3/4)*ln(1 - (4/3)*p).

    Args:
        p: raw proportion of differing sites (0 <= p < 0.75)

    Returns:
        Corrected evolutionary distance d.

    Raises:
        ValueError if p >= 0.75 (saturation — correction undefined).
    """
    if p < 0:
        raise ValueError("Raw distance p must be non-negative")
    if p >= P_SATURATION:
        raise ValueError(f"Raw distance p={p} >= {P_SATURATION}: sequences are saturated, JC undefined")
    if p == 0:
        return 0.0
    return -(3 / 4) * math.log(1 - (4 / 3) * p)


def is_saturated(p, threshold=0.70):
    """Check whether raw distance p is approaching saturation.

    Returns True if p >= threshold (default 0.70), meaning the JC correction
    is becoming unreliable and the sequences may be too divergent for
    meaningful distance estimation.
    """
    return p >= threshold


if __name__ == "__main__":
    p = raw_distance(SEQ1, SEQ2)
    d = jukes_cantor(p)
    print(f"Sequences: {SEQ1} vs {SEQ2}")
    print(f"Differences: {count_differences(SEQ1, SEQ2)}")
    print(f"Raw distance (p):  {p:.4f}")
    print(f"JC distance  (d):  {d:.4f}")
    print(f"Correction factor: {d/p:.2f}x")
    print(f"Saturated: {is_saturated(p)}")
