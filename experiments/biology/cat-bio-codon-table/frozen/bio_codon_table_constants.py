"""Codon Table — Frozen Constants. Source: NCBI Standard Genetic Code (transl_table=1). DO NOT MODIFY."""

# Standard genetic code: 64 codons total
# 61 sense codons (encode amino acids) + 3 stop codons
TOTAL_CODONS = 64
SENSE_CODONS = 61
STOP_CODON_COUNT = 3

# Start codon: AUG is the ONLY standard start codon in eukaryotes (codes for Met)
START_CODON = "AUG"

# Stop codons: exactly 3 — UAA (ochre), UAG (amber), UGA (opal/umber)
STOP_CODONS = frozenset({"UAA", "UAG", "UGA"})

# Full standard genetic code table: codon -> single-letter amino acid
# Organized by first base (U, C, A, G)
CODON_TABLE = {
    # UXX
    "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
    "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
    "UAU": "Y", "UAC": "Y", "UAA": "*", "UAG": "*",
    "UGU": "C", "UGC": "C", "UGA": "*", "UGG": "W",
    # CXX
    "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
    "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    # AXX
    "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
    "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    # GXX
    "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
    "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}

# Key degeneracies (amino acids with multiple codons)
# Leu: 6 codons (UUA, UUG, CUU, CUC, CUA, CUG) — most degenerate along with Ser, Arg
LEU_CODONS = ("UUA", "UUG", "CUU", "CUC", "CUA", "CUG")
# Trp: 1 codon (UGG) — only UGG, NOT UGA
TRP_CODON = "UGG"
# Met: 1 codon (AUG) — also serves as start codon
MET_CODON = "AUG"

# Test sequence: AUG-CUU-UAA → Met-Leu-Stop → "ML"
TEST_MRNA = "AUGCUUUAA"
TEST_PROTEIN = "ML"

# Trap: UGA is a stop codon in the standard code, NOT Trp
# (UGA can code for selenocysteine (Sec/U) via SECIS element, but that is
#  a recoding event, not part of the standard table)

PRIOR_ERRORS = {
    "extra_start_codons": "Claims codons other than AUG can be standard eukaryotic start codons",
    "wrong_stop_count":   "Says 2 or 4 stop codons instead of exactly 3 (UAA, UAG, UGA)",
    "uga_not_stop":       "Forgets UGA is a stop codon, confuses it with Trp or selenocysteine",
}
