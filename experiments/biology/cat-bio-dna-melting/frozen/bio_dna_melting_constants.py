"""DNA Melting Temperature — Frozen Constants. Source: SantaLucia (1998) nearest-neighbor thermodynamics. DO NOT MODIFY."""

# ---------------------------------------------------------------------------
# Methods overview
# ---------------------------------------------------------------------------
# Wallace rule (short oligos <14 bp):  Tm = 2*(A+T) + 4*(G+C)
#   - Counts bases only; ignores sequence order entirely.
#
# Marmur-Doty / %GC (approximate):  Tm = 64.9 + 41*(G+C-16.4)/(A+T+G+C)
#   - Still %GC-based; ignores stacking interactions.
#
# Nearest-Neighbor (accurate):  Tm = (DeltaH / (DeltaS + R*ln(Ct/4))) - 273.15
#   - DeltaH, DeltaS = sums of dinucleotide stacking parameters
#   - R = 1.987 cal/(mol*K), Ct = total strand concentration (M)
#   - Accounts for stacking interactions: base ORDER matters.
# ---------------------------------------------------------------------------

# Gas constant (cal / (mol*K))
R_CAL = 1.987

# Default total strand concentration for Tm calculation (M)
DEFAULT_CT = 0.0001  # 100 uM, a common oligo working concentration

# ---------------------------------------------------------------------------
# Test sequences — same base composition, different order
# ---------------------------------------------------------------------------
SEQ1 = "AATTGGCC"   # clustered: AA-AT-TT-TG-GG-GC-CC
SEQ2 = "AGCTCGAT"   # alternating: AG-GC-CT-TC-CG-GA-AT

# Both are 8 bp, 50% GC (A:2 T:2 G:2 C:2)
SEQ1_LENGTH = 8
SEQ2_LENGTH = 8
SEQ1_GC = 0.50
SEQ2_GC = 0.50

# Wallace Tm for both (identical — Wallace ignores order)
# Tm = 2*(2+2) + 4*(2+2) = 8 + 16 = 24
WALLACE_TM_1 = 24  # degrees C
WALLACE_TM_2 = 24  # degrees C — same!

# Nearest-neighbor dinucleotide pairs (stacking steps)
NN_PAIRS_SEQ1 = ("AA", "AT", "TT", "TG", "GG", "GC", "CC")  # 7 steps
NN_PAIRS_SEQ2 = ("AG", "GC", "CT", "TC", "CG", "GA", "AT")   # 7 steps — all different!

# Simple validation sequence
TEST_SEQ = "ATCGATCG"   # 8 bp, 50% GC
TEST_WALLACE_TM = 24     # 2*(4) + 4*(4) = 8+16 = 24

# ---------------------------------------------------------------------------
# Known LLM error patterns
# ---------------------------------------------------------------------------
PRIOR_ERRORS = {
    "gc_method_accurate":  "Claims %GC method is sufficient for Tm prediction — ignores stacking interactions",
    "order_irrelevant":    "Claims base ORDER does not matter for Tm — nearest-neighbor method proves otherwise",
    "wallace_for_long":    "Uses Wallace rule (2AT + 4GC) for long sequences >14 bp where it is invalid",
}
