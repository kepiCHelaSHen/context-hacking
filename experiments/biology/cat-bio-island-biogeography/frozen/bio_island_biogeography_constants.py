"""Island Biogeography — Frozen Constants. Source: MacArthur & Wilson 1967. DO NOT MODIFY."""

# Species-Area Relationship (MacArthur-Wilson):
#   S = c * A^z
#
# S = number of species
# A = island area (km^2)
# c = taxon/region-specific constant
# z = species-area exponent (KEY parameter)
#
# Canonical z values:
#   Oceanic islands:  z ~ 0.25-0.35, canonical z = 0.30
#   Mainland areas:   z ~ 0.12-0.17, canonical z = 0.15
#
# z is NOT 0.5 or 1.0 — those are common LLM errors.
#   z=0.5 implies S grows as sqrt(A), far too steep
#   z=1.0 implies S is proportional to A (linear), which is wrong
#
# Equilibrium theory: species number on an island is where
# immigration rate (decreases as S rises) = extinction rate (increases as S rises)

# --- Test parameters (oceanic island case) ---
C_TEST = 10          # taxon constant
Z_ISLAND = 0.30      # canonical oceanic island exponent
Z_MAINLAND = 0.15    # canonical mainland exponent
A_TEST = 100          # area in km^2

# S = c * A^z = 10 * 100^0.30 = 10 * 3.981072 = 39.810717
S_AT_100 = C_TEST * A_TEST ** Z_ISLAND

# Doubling area: S(200) = 10 * 200^0.30 = 49.012742
S_AT_200 = C_TEST * 200 ** Z_ISLAND

# 10x area: S(1000) = 10 * 1000^0.30 = 79.432823
S_AT_1000 = C_TEST * 1000 ** Z_ISLAND

# Doubling ratio: when area doubles, species count multiplies by 2^z
#   2^0.30 = 1.231144 → ~23% increase, NOT 100%
DOUBLING_RATIO_ISLAND = 2 ** Z_ISLAND

# Mainland doubling ratio: 2^0.15 = 1.109569 → ~11% increase
DOUBLING_RATIO_MAINLAND = 2 ** Z_MAINLAND

# --- Verification assertions ---
assert abs(S_AT_100 - 39.810717) < 1e-3, f"S(100) wrong: {S_AT_100}"
assert abs(S_AT_200 - 49.012742) < 1e-3, f"S(200) wrong: {S_AT_200}"
assert abs(S_AT_1000 - 79.432823) < 1e-3, f"S(1000) wrong: {S_AT_1000}"
assert abs(DOUBLING_RATIO_ISLAND - 1.231144) < 1e-3, \
    f"Doubling ratio (island) wrong: {DOUBLING_RATIO_ISLAND}"
assert abs(DOUBLING_RATIO_MAINLAND - 1.109569) < 1e-3, \
    f"Doubling ratio (mainland) wrong: {DOUBLING_RATIO_MAINLAND}"

# Doubling area gives ~23% more species, NOT 100%
assert DOUBLING_RATIO_ISLAND < 1.30, \
    "Doubling area must NOT double species count — z is ~0.30, not ~1.0"

# 10x area roughly doubles species (ratio ~1.995)
TENFOLD_RATIO_ISLAND = S_AT_1000 / S_AT_100
assert abs(TENFOLD_RATIO_ISLAND - 1.995262) < 1e-3, \
    f"10x area ratio wrong: {TENFOLD_RATIO_ISLAND}"

PRIOR_ERRORS = {
    "z_too_high":           "Uses z ~ 0.5 or z ~ 1.0 instead of canonical z ~ 0.30 for islands",
    "linear_species_area":  "Assumes S proportional to A (S = c*A) instead of S = c*A^z",
    "z_island_vs_mainland": "Uses mainland z (~0.15) for oceanic islands or island z (~0.30) for mainland",
}
