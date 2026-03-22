"""Codon Table — CHP Biology Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_codon_table_constants import *


def translate(mrna_seq):
    """Translate an mRNA sequence into a single-letter amino acid string.

    Reads from the first codon to the first stop codon (or end of sequence).
    Stop codons are NOT included in the output. Non-triplet trailing bases
    are ignored.
    """
    protein = []
    for i in range(0, len(mrna_seq) - 2, 3):
        codon = mrna_seq[i:i+3].upper()
        aa = CODON_TABLE.get(codon)
        if aa is None:
            raise ValueError(f"Unknown codon: {codon}")
        if aa == "*":
            break
        protein.append(aa)
    return "".join(protein)


def is_start_codon(codon):
    """Return True only for AUG — the sole standard eukaryotic start codon."""
    return codon.upper() == START_CODON


def is_stop_codon(codon):
    """Return True for UAA, UAG, UGA — the 3 standard stop codons."""
    return codon.upper() in STOP_CODONS


def codon_to_aa(codon):
    """Return single-letter amino acid code for a codon, or '*' for stop."""
    codon = codon.upper()
    aa = CODON_TABLE.get(codon)
    if aa is None:
        raise ValueError(f"Unknown codon: {codon}")
    return aa


def count_sense_codons():
    """Return 61 — the number of sense (non-stop) codons in the standard code."""
    return sum(1 for aa in CODON_TABLE.values() if aa != "*")


if __name__ == "__main__":
    print(f"Translate '{TEST_MRNA}' -> '{translate(TEST_MRNA)}'")
    print(f"Start codon AUG? {is_start_codon('AUG')}")
    print(f"Stop codons: {sorted(STOP_CODONS)} (count={len(STOP_CODONS)})")
    print(f"Sense codons: {count_sense_codons()}")
    print(f"UGA is stop? {is_stop_codon('UGA')}  UGG->aa? {codon_to_aa('UGG')}")
