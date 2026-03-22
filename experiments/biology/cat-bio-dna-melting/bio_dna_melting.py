"""DNA Melting Temperature — CHP Biology Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_dna_melting_constants import *


def base_counts(seq):
    """Return dict of base counts {A: n, T: n, G: n, C: n} for a DNA sequence."""
    seq = seq.upper()
    counts = {"A": 0, "T": 0, "G": 0, "C": 0}
    for base in seq:
        if base not in counts:
            raise ValueError(f"Invalid DNA base: {base}")
        counts[base] += 1
    return counts


def gc_content(seq):
    """Return GC fraction (0.0–1.0) for a DNA sequence."""
    counts = base_counts(seq)
    total = sum(counts.values())
    if total == 0:
        raise ValueError("Empty sequence")
    return (counts["G"] + counts["C"]) / total


def wallace_tm(seq):
    """Compute Tm using the Wallace rule: Tm = 2*(A+T) + 4*(G+C).

    Valid only for short oligonucleotides (<14 bp).
    NOTE: This method counts bases only — sequence ORDER is ignored entirely.
    Two sequences with the same composition but different order get the SAME Tm,
    which is incorrect for real thermodynamics (see nearest-neighbor method).
    """
    counts = base_counts(seq)
    at = counts["A"] + counts["T"]
    gc = counts["G"] + counts["C"]
    return 2 * at + 4 * gc


def nn_pairs(seq):
    """Return list of nearest-neighbor dinucleotide steps for a DNA sequence.

    For a sequence of length N, there are N-1 overlapping dinucleotide steps.
    These stacking pairs are the basis of the nearest-neighbor Tm method —
    unlike %GC or Wallace, they capture how adjacent bases INTERACT.
    Two sequences with the same base composition but different order will
    produce DIFFERENT nn_pairs, leading to different Tm values.
    """
    seq = seq.upper()
    if len(seq) < 2:
        raise ValueError("Sequence must be at least 2 bases long")
    return [seq[i:i+2] for i in range(len(seq) - 1)]


if __name__ == "__main__":
    for label, seq in [("SEQ1 (clustered)", SEQ1), ("SEQ2 (alternating)", SEQ2)]:
        counts = base_counts(seq)
        gc = gc_content(seq)
        w_tm = wallace_tm(seq)
        pairs = nn_pairs(seq)
        print(f"{label}: {seq}")
        print(f"  Base counts: {counts}")
        print(f"  GC content:  {gc:.2%}")
        print(f"  Wallace Tm:  {w_tm} C")
        print(f"  NN pairs:    {pairs}")
        print()
    print("KEY INSIGHT: Wallace Tm is identical for both sequences,")
    print("but NN pairs are completely different — proving order matters.")
