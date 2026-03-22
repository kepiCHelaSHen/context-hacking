"""Single-Layer Atmosphere Model — Frozen Constants. Source: Pierrehumbert, Principles of Planetary Climate, Ch 3. DO NOT MODIFY."""
import math

# Stefan-Boltzmann constant
SIGMA = 5.67e-8  # W/(m^2 K^4)

# Solar constant and Earth albedo
S_SOLAR = 1361    # W/m^2  (TSI at 1 AU)
ALPHA = 0.30      # Bond albedo (dimensionless)

# Absorbed solar flux averaged over sphere: S*(1-alpha)/4
F_ABSORBED = S_SOLAR * (1 - ALPHA) / 4  # = 238.175 W/m^2

# Bare-earth equilibrium temperature (no atmosphere): sigma*T^4 = F_absorbed
T_BARE = (F_ABSORBED / SIGMA) ** 0.25  # ≈ 254.58 K  (-18.6°C)

# Single-layer atmosphere model with emissivity = 1 (complete absorption)
# T_surface = T_bare * 2^(1/4)
FACTOR_1LAYER = 2 ** 0.25  # = 1.18921...
T_SURFACE_1LAYER = T_BARE * FACTOR_1LAYER  # ≈ 302.75 K  (29.6°C)  — OVERESTIMATES

# Observed values
T_SURFACE_OBSERVED = 288.0  # K  (15°C)
GREENHOUSE_EFFECT_OBSERVED = T_SURFACE_OBSERVED - T_BARE  # ≈ 33.4 K

# KEY INSIGHT: Real atmosphere has ε < 1 (partial absorption/emission)
# Single-layer ε=1 model OVERESTIMATES the greenhouse warming (303K vs 288K)
# The ε=1 assumption is the most common LLM error in this topic

# Test scenario: Stefan-Boltzmann flux at 288K
TEST_T = 288.0
TEST_EPSILON = 0.78  # realistic effective atmospheric emissivity
TEST_FLUX_FULL = SIGMA * TEST_T ** 4             # ≈ 390.08 W/m^2 (ε=1)
TEST_FLUX_PARTIAL = TEST_EPSILON * SIGMA * TEST_T ** 4  # ≈ 304.26 W/m^2

PRIOR_ERRORS = {
    "emissivity_always_1": "Assumes ε=1 for atmosphere (real atmosphere has ε<1, partial absorption)",
    "no_albedo":           "Forgets albedo α in energy balance — uses S/4 instead of S*(1-α)/4",
    "bare_earth_too_warm": "Gets T_bare wrong, often confuses bare-earth 255K with observed 288K",
}
