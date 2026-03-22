"""S-N Curve / Fatigue Life / Miner's Rule — Frozen Constants. Source: Shigley's Mechanical Engineering Design. DO NOT MODIFY."""

# S-N curve: relates stress amplitude S to number of cycles N to failure
# Basquin's law: S = A * N^b  (power law, linear in log-log space)
#
# Endurance limit Se: stress below which infinite life is expected
#   - STEEL: Se ≈ 0.5 * Su  for Su < 1400 MPa  (well-established empirical rule)
#   - ALUMINUM: NO true endurance limit! Fatigue life is always finite.
#     (ASTM defines "fatigue strength at N cycles" for Al, NOT an endurance limit)
#
# Miner's rule (linear damage accumulation):
#   Σ(nᵢ / Nᵢ) = 1  at failure
#   nᵢ = actual cycles at stress level i
#   Nᵢ = cycles to failure at stress level i (from S-N curve)
#
# LLM priors:
#   1. Claims aluminum has an endurance limit (it does NOT)
#   2. Uses Miner's damage sum ≠ 1 for failure criterion
#   3. Uses Se = Su instead of Se ≈ 0.5 * Su

# --- Steel reference ---
SU_STEEL_REF = 800e6          # Ultimate tensile strength 800 MPa
SU_THRESHOLD = 1400e6         # Se ≈ 0.5*Su rule valid for Su < 1400 MPa
SE_STEEL_REF = 0.5 * SU_STEEL_REF  # 400 MPa endurance limit

# WRONG: Se = Su (common LLM error — confuses endurance limit with ultimate strength)
SE_WRONG_EQUALS_SU = SU_STEEL_REF  # 800 MPa — WRONG!

# --- S-N curve test points ---
# At S = 500 MPa, N = 100,000 cycles to failure
S_LEVEL_1 = 500e6             # Pa
N_LIFE_1 = 100_000            # cycles

# At S = 450 MPa, N = 500,000 cycles to failure
S_LEVEL_2 = 450e6             # Pa
N_LIFE_2 = 500_000            # cycles

# --- Miner's rule test ---
# n1 = 50,000 cycles at S = 500 MPa (N1 = 100,000)
# damage_1 = 50,000 / 100,000 = 0.5
N_ACTUAL_1 = 50_000
DAMAGE_1 = N_ACTUAL_1 / N_LIFE_1   # 0.5

# Remaining life at S = 450 MPa: n2 = N2 * (1 - damage_1) = 500,000 * 0.5 = 250,000
N_REMAINING_2 = N_LIFE_2 * (1.0 - DAMAGE_1)  # 250,000

# Total damage at failure = 1.0 (Miner's rule)
MINER_FAILURE_SUM = 1.0

# Materials with/without endurance limits
MATERIALS_WITH_ENDURANCE = {"steel", "titanium"}
MATERIALS_WITHOUT_ENDURANCE = {"aluminum", "copper", "magnesium"}

PRIOR_ERRORS = {
    "al_has_endurance":        "Claims aluminum has an endurance limit — it does NOT; fatigue life is always finite",
    "miner_sum_not_1":         "Uses Miner's damage sum ≠ 1 for failure criterion — sum must equal 1.0",
    "endurance_equals_ultimate": "Uses Se = Su instead of Se ≈ 0.5*Su for steel — endurance limit is roughly half of ultimate strength",
}
