"""
Mohs Hardness Scale — Frozen Constants
Source: Friedrich Mohs (1822), Tabor (1954) Vickers indentation data, Broz et al. (2006)
DO NOT MODIFY.
"""

# --- Mohs Scale (ordinal, 1-10) ---
# Each mineral can scratch all minerals below it, and is scratched by all above.
# The scale is ORDINAL (rank order), NOT linear in absolute hardness.
MOHS_SCALE = {
    "talc":       1,
    "gypsum":     2,
    "calcite":    3,
    "fluorite":   4,
    "apatite":    5,
    "orthoclase": 6,
    "quartz":     7,
    "topaz":      8,
    "corundum":   9,
    "diamond":   10,
}

# --- Approximate Vickers Hardness (absolute, kg/mm²) ---
# These show the scale is profoundly NON-LINEAR.
# The gap from 9 (corundum) to 10 (diamond) is ~1100 Vickers,
# while the gap from 1 (talc) to 2 (gypsum) is only ~2 Vickers.
VICKERS_APPROX = {
    1:    1,       # talc
    2:    3,       # gypsum
    3:    9,       # calcite
    4:   21,       # fluorite
    5:   48,       # apatite
    6:   72,       # orthoclase
    7:  100,       # quartz
    8:  200,       # topaz
    9:  400,       # corundum
    10: 1500,      # diamond
}

# --- Common reference hardness values ---
FINGERNAIL_HARDNESS = 2.5
GLASS_HARDNESS = 5.5
STEEL_FILE_HARDNESS = 6.5

# --- Key non-linearity facts ---
# Vickers gap 9->10: 1500 - 400 = 1100
# Vickers gap 1->2:    3 - 1   = 2
# Ratio of diamond to talc in Vickers: 1500 / 1 = 1500x (NOT 10x!)
VICKERS_GAP_9_TO_10 = VICKERS_APPROX[10] - VICKERS_APPROX[9]   # 1100
VICKERS_GAP_1_TO_2  = VICKERS_APPROX[2]  - VICKERS_APPROX[1]   # 2
VICKERS_RATIO_DIAMOND_TALC = VICKERS_APPROX[10] / VICKERS_APPROX[1]  # 1500.0

PRIOR_ERRORS = {
    "mohs_linear":       "Claims equal hardness intervals between Mohs numbers — scale is ordinal, not linear",
    "diamond_10x_talc":  "Claims diamond is 10x harder than talc — actual Vickers ratio is ~1500x",
    "wrong_mineral_order": "Misorders common minerals on the Mohs scale (e.g., swaps quartz and feldspar)",
}
