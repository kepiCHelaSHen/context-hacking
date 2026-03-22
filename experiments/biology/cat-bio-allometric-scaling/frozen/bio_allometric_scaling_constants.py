"""Allometric Scaling (Kleiber's Law) — Frozen Constants. Source: Kleiber 1932, West-Brown-Enquist 1997. DO NOT MODIFY."""
# Kleiber's Law: B = B0 * M^(3/4) where B=metabolic rate (kcal/day), M=body mass (kg)
# KEY: exponent is 3/4 = 0.75 (Kleiber 1932), NOT 2/3 (Rubner surface-area law)
# 2/3 comes from surface-area scaling (Rubner 1883) — wrong for whole-organism metabolism
# 3/4 is Kleiber's empirical finding, later supported by West-Brown-Enquist fractal theory
KLEIBER_EXPONENT = 0.75          # 3/4 — the CORRECT scaling exponent
RUBNER_EXPONENT = 2 / 3          # ~0.6667 — surface-area law, WRONG for metabolism
B0_MAMMAL = 70                   # kcal/day normalization constant (M in kg)

# Test organisms
M_MOUSE = 0.025                  # kg
M_HUMAN = 70                     # kg
M_ELEPHANT = 5000                # kg

# Correct metabolic rates with Kleiber exponent 3/4
B_MOUSE = B0_MAMMAL * M_MOUSE ** KLEIBER_EXPONENT       # ≈ 4.401 kcal/day
B_HUMAN = B0_MAMMAL * M_HUMAN ** KLEIBER_EXPONENT       # ≈ 1694.0 kcal/day
B_ELEPHANT = B0_MAMMAL * M_ELEPHANT ** KLEIBER_EXPONENT  # ≈ 41622 kcal/day

# WRONG result using Rubner 2/3 exponent
B_HUMAN_WRONG = B0_MAMMAL * M_HUMAN ** RUBNER_EXPONENT  # ≈ 1188.9 kcal/day (~30% under)

PRIOR_ERRORS = {
    "exponent_two_thirds":  "Uses 2/3 exponent instead of 3/4 (Rubner surface law, not Kleiber)",
    "surface_area_law":     "Cites Rubner's surface-area law as correct for metabolic scaling",
    "b0_wrong_units":       "Uses B0 from a different unit system (e.g. watts) without conversion",
}
