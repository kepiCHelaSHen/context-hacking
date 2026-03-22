"""Jukes-Cantor Phylogenetic Distance — Frozen Constants. Source: Jukes & Cantor 1969. DO NOT MODIFY."""
import math

# Raw distance: p = (number of differences) / (alignment length)
# Jukes-Cantor correction: d = -(3/4)*ln(1 - (4/3)*p)
# KEY: As p approaches 0.75, d -> infinity (saturation). Raw p underestimates true distance!
# For p < ~0.05, d ~ p (correction negligible)
# Maximum raw distance for 4 nucleotides: p_max = 3/4 = 0.75 (random sequences)

# Test sequences
SEQ1 = "ATCGATCG"
SEQ2 = "ATCAATGG"
# ATCGATCG vs ATCAATGG: positions 4 (G->A) and 7 (C->G) differ -> 2 differences in 8 sites

RAW_P = 0.25                    # 2/8 = 0.25
JC_D = 0.3041                   # -(3/4)*ln(1-(4/3)*0.25) = -(3/4)*ln(2/3) = 0.30410
P_SATURATION = 0.75             # Maximum raw distance (random sequences)

# Additional test point: p = 0.3
#   d = -(3/4)*ln(1-0.4) = -(3/4)*ln(0.6) = 0.3831
#   Raw says 0.30, JC says 0.3831 -> 28% underestimation by raw!
JC_D_03 = 0.3831               # JC distance at p=0.3

# Verify constants
_jc_025 = -(3 / 4) * math.log(1 - (4 / 3) * RAW_P)
assert math.isclose(_jc_025, JC_D, rel_tol=1e-3), f"JC at p=0.25: got {_jc_025}, expected {JC_D}"

_jc_030 = -(3 / 4) * math.log(1 - (4 / 3) * 0.3)
assert math.isclose(_jc_030, JC_D_03, rel_tol=1e-3), f"JC at p=0.3: got {_jc_030}, expected {JC_D_03}"

assert JC_D > RAW_P, "JC distance must always exceed raw distance for p > 0"
assert JC_D_03 > 0.3, "JC distance at p=0.3 must exceed raw p=0.3"

PRIOR_ERRORS = {
    "raw_not_corrected":        "Uses raw p instead of Jukes-Cantor corrected d",
    "no_saturation":            "Doesn't recognize correction diverges near p=0.75",
    "wrong_correction_formula": "Wrong constant in Jukes-Cantor formula (e.g., 2/3 instead of 3/4)",
}
