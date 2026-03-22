"""Lotka-Volterra Competition — Frozen Constants. Source: Lotka 1925, Volterra 1926. DO NOT MODIFY."""

# Lotka-Volterra competition model (two species):
#   dN₁/dt = r₁ N₁ (1 - (N₁ + α₁₂ N₂) / K₁)
#   dN₂/dt = r₂ N₂ (1 - (N₂ + α₂₁ N₁) / K₂)
#
# α₁₂ = competitive effect of species 2 ON species 1 (per-capita)
# α₂₁ = competitive effect of species 1 ON species 2 (per-capita)
#
# Coexistence requires BOTH conditions:
#   K₁ / α₁₂ > K₂   ⟺   α₁₂ < K₁ / K₂
#   K₂ / α₂₁ > K₁   ⟺   α₂₁ < K₂ / K₁
#
# Meaning: each species must be limited more by intraspecific competition
# than by interspecific competition.  Both inequalities must hold.
#
# Coexistence equilibrium (when both conditions met):
#   N₁* = (K₁ - α₁₂ K₂) / (1 - α₁₂ α₂₁)
#   N₂* = (K₂ - α₂₁ K₁) / (1 - α₁₂ α₂₁)

# --- Test parameters (coexistence case) ---
R1 = 0.5
R2 = 0.3
K1 = 1000
K2 = 800
ALPHA12 = 0.5     # effect of species 2 ON species 1
ALPHA21 = 0.6     # effect of species 1 ON species 2

# Coexistence check:
#   K₁/K₂ = 1000/800 = 1.25 > α₁₂ = 0.5  ✓
#   K₂/K₁ = 800/1000 = 0.8  > α₂₁ = 0.6  ✓
COEXISTENCE_EXPECTED = True

# Equilibrium values:
#   N₁* = (1000 - 0.5*800) / (1 - 0.5*0.6) = 600 / 0.7 = 857.142857...
#   N₂* = (800 - 0.6*1000) / (1 - 0.5*0.6) = 200 / 0.7 = 285.714285...
DENOM = 1 - ALPHA12 * ALPHA21                     # 0.7
N1_STAR = (K1 - ALPHA12 * K2) / DENOM             # 857.142857...
N2_STAR = (K2 - ALPHA21 * K1) / DENOM             # 285.714285...

assert abs(DENOM - 0.7) < 1e-12, f"Denominator wrong: {DENOM}"
assert abs(N1_STAR - 600 / 0.7) < 1e-6, f"N1* wrong: {N1_STAR}"
assert abs(N2_STAR - 200 / 0.7) < 1e-6, f"N2* wrong: {N2_STAR}"

# Growth rates at initial condition N1=100, N2=50
#   dN1/dt = 0.5 * 100 * (1 - (100 + 0.5*50)/1000)
#          = 50 * (1 - 125/1000) = 50 * 0.875 = 43.75
#   dN2/dt = 0.3 * 50 * (1 - (50 + 0.6*100)/800)
#          = 15 * (1 - 110/800) = 15 * 0.8625 = 12.9375
DN1DT_AT_100_50 = R1 * 100 * (1 - (100 + ALPHA12 * 50) / K1)
DN2DT_AT_100_50 = R2 * 50 * (1 - (50 + ALPHA21 * 100) / K2)
assert abs(DN1DT_AT_100_50 - 43.75) < 1e-10, f"dN1/dt wrong: {DN1DT_AT_100_50}"
assert abs(DN2DT_AT_100_50 - 12.9375) < 1e-10, f"dN2/dt wrong: {DN2DT_AT_100_50}"

# --- Non-coexistence parameters ---
ALPHA12_NO = 1.5   # α₁₂ = 1.5 > K₁/K₂ = 1.25  ✗
ALPHA21_NO = 1.2   # α₂₁ = 1.2 > K₂/K₁ = 0.8   ✗
COEXISTENCE_NO_EXPECTED = False

PRIOR_ERRORS = {
    "wrong_coexistence_direction": "Reverses the inequality (e.g. α₁₂ > K₁/K₂ instead of <)",
    "only_one_condition":          "Checks only one species' condition instead of requiring both",
    "alpha_interpretation":        "Confuses α₁₂ (effect of sp 2 ON sp 1) with effect of sp 1 ON sp 2",
}
