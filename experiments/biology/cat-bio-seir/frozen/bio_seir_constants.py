"""SEIR Epidemic Model — Frozen Constants. Source: Kermack & McKendrick 1927. DO NOT MODIFY."""
import math

# SEIR compartmental model:
#   S → E → I → R
#   dS/dt = -β * S * I / N
#   dE/dt =  β * S * I / N - σ * E
#   dI/dt =  σ * E - γ * I
#   dR/dt =  γ * I
#
# Parameters:
#   β (beta)  — transmission rate
#   σ (sigma) — 1 / incubation period (E → I transition rate)
#   γ (gamma) — 1 / infectious period (I → R recovery rate)
#   N         — total population (constant)
#
# KEY FACT:
#   R₀ = β / γ  for BOTH SIR and SEIR models.
#   The exposed compartment rate σ affects TIMING (how fast E→I) but NOT R₀.
#   Many LLMs incorrectly write R₀ = βσ / ((σ+γ)γ) or similar formulas
#   that incorporate σ.  This is WRONG.
#
# Herd immunity threshold: 1 - 1/R₀  (same for SIR and SEIR)
#
# Conservation: S + E + I + R = N  always (population is closed)
#
# Test parameters: β=0.5, σ=0.2 (5-day incubation), γ=0.1 (10-day infectious), N=10000
#   R₀ = β / γ = 0.5 / 0.1 = 5.0
#   Herd immunity = 1 - 1/5 = 0.8 (80%)
#   Derivatives at (S=9990, E=5, I=3, R=2, N=10000):
#     dS/dt = -0.5 * 9990 * 3 / 10000 = -1.4985
#     dE/dt =  0.5 * 9990 * 3 / 10000 - 0.2 * 5 = 1.4985 - 1.0 = 0.4985
#     dI/dt =  0.2 * 5 - 0.1 * 3 = 1.0 - 0.3 = 0.7
#     dR/dt =  0.1 * 3 = 0.3
#     Sum of derivatives: -1.4985 + 0.4985 + 0.7 + 0.3 = 0.0  (conservation!)

BETA = 0.5
SIGMA = 0.2
GAMMA = 0.1
N = 10000

# R₀ = β / γ — sigma is NOT included
R0 = BETA / GAMMA  # 5.0

# Herd immunity threshold
HERD_IMMUNITY = 1 - 1 / R0  # 0.8

# Test state: S=9990, E=5, I=3, R=2
TEST_S = 9990
TEST_E = 5
TEST_I = 3
TEST_R = 2

# Precomputed derivatives at test state
DSDT = -BETA * TEST_S * TEST_I / N       # -1.4985
DEDT = BETA * TEST_S * TEST_I / N - SIGMA * TEST_E  # 0.4985
DIDT = SIGMA * TEST_E - GAMMA * TEST_I   # 0.7
DRDT = GAMMA * TEST_I                    # 0.3

# Verify frozen values
assert math.isclose(R0, 5.0, rel_tol=1e-9), f"R0 wrong: {R0}"
assert math.isclose(HERD_IMMUNITY, 0.8, rel_tol=1e-9), f"Herd immunity wrong: {HERD_IMMUNITY}"
assert math.isclose(DSDT, -1.4985, rel_tol=1e-6), f"dS/dt wrong: {DSDT}"
assert math.isclose(DEDT, 0.4985, rel_tol=1e-6), f"dE/dt wrong: {DEDT}"
assert math.isclose(DIDT, 0.7, rel_tol=1e-9), f"dI/dt wrong: {DIDT}"
assert math.isclose(DRDT, 0.3, rel_tol=1e-9), f"dR/dt wrong: {DRDT}"

# Conservation: derivatives must sum to zero
assert math.isclose(DSDT + DEDT + DIDT + DRDT, 0.0, abs_tol=1e-12), (
    f"Derivatives don't sum to 0: {DSDT + DEDT + DIDT + DRDT}"
)

# Conservation: compartments must sum to N
assert TEST_S + TEST_E + TEST_I + TEST_R == N, (
    f"Compartments don't sum to N: {TEST_S + TEST_E + TEST_I + TEST_R}"
)

# R₀ with different σ values — should all give the SAME R₀
for sigma_test in [0.05, 0.1, 0.2, 0.5, 1.0, 5.0]:
    assert math.isclose(BETA / GAMMA, R0, rel_tol=1e-9), (
        f"R0 should not depend on sigma={sigma_test}"
    )

PRIOR_ERRORS = {
    "r0_includes_sigma":    "Incorrectly includes σ in R₀ formula (e.g., R₀=βσ/((σ+γ)γ))",
    "seir_r0_different":    "Claims SEIR R₀ differs from SIR R₀",
    "herd_immunity_wrong":  "Wrong herd immunity threshold formula",
}
