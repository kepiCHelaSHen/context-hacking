"""
Frozen reference constants for Shannon Diversity Index experiment.

Shannon-Wiener Diversity Index (ecology convention):
  H' = -SUM(p_i * ln(p_i))          <-- NATURAL LOG (ecology standard)

Information theory variant:
  H  = -SUM(p_i * log2(p_i))        <-- log base 2 (bits)

These give DIFFERENT numerical values.  LLMs frequently confuse the two.

Maximum diversity:  H'_max = ln(S)   where S = number of species
Evenness (Pielou):  J = H' / H'_max = H' / ln(S),  range [0, 1]

PRIOR_ERRORS
------------
- "log2_not_ln"     : uses log2 instead of ln for the ecology index
- "hmax_wrong_base" : computes H'_max with one base but H' with another
- "evenness_gt_1"   : evenness J > 1, caused by mismatched log bases
"""

import math

# ---------------------------------------------------------------------------
# Reference community: 5 species
# ---------------------------------------------------------------------------
SPECIES_COUNTS = [20, 15, 10, 30, 25]
TOTAL_N = 100
PROPORTIONS = [0.20, 0.15, 0.10, 0.30, 0.25]
NUM_SPECIES = 5

# ---------------------------------------------------------------------------
# Correct values (natural log)
# ---------------------------------------------------------------------------
SHANNON_LN = 1.5444795210968603       # H' = -SUM(p_i * ln(p_i))
HMAX_LN = 1.6094379124341003          # ln(S) = ln(5)
EVENNESS_J = 0.9596390821693783       # J = H' / H'_max

# ---------------------------------------------------------------------------
# Wrong-base values (log2) -- for comparison / error detection
# ---------------------------------------------------------------------------
SHANNON_LOG2 = 2.2282129458410016     # -SUM(p_i * log2(p_i))
LN2 = math.log(2)                     # 0.6931471805599453

# Relationship:  H'_log2 = H'_ln / ln(2)
# So if someone accidentally uses log2, the number is ~1.44x larger.

# ---------------------------------------------------------------------------
# Equal-abundance reference (J must equal 1.0)
# ---------------------------------------------------------------------------
EQUAL_COUNTS = [20, 20, 20, 20, 20]
EQUAL_H = 1.6094379124341005          # == ln(5), as expected
EQUAL_J = 1.0

# ---------------------------------------------------------------------------
# Tolerances
# ---------------------------------------------------------------------------
RTOL = 1e-9
ATOL = 1e-12
