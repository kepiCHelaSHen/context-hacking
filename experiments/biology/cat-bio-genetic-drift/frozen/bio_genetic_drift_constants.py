"""Wright-Fisher Genetic Drift — Frozen Constants. Source: Wright 1931, Fisher 1930. DO NOT MODIFY."""
import math

# Wright-Fisher model: 2N gene copies, binomial sampling each generation
# KEY INSIGHT: Fixation probability of neutral allele = p0 (initial frequency)
#   NOT 1/(2N)! That's only for a NEW single-copy mutation where p0 = 1/(2N).
# Heterozygosity decays: H(t) = H0 * (1 - 1/(2N))^t
# Variance in allele frequency per generation: p(1-p)/(2N)

# Test parameters: N=50 diploid individuals, p0=0.3
N = 50
TWO_N = 2 * N               # 100 gene copies
P0 = 0.3                    # initial allele frequency
Q0 = 1 - P0                 # 0.7

# Fixation probability (neutral allele): P(fix) = p0
P_FIX = P0                  # 0.3
P_LOSS = Q0                 # 0.7
WRONG_P_FIX = 1 / TWO_N    # 0.01 — the common LLM mistake

# Heterozygosity
H0 = 2 * P0 * Q0            # 0.42
T_TEST = 100                 # generations
DECAY_FACTOR = (1 - 1 / TWO_N) ** T_TEST   # 0.99^100 ≈ 0.3660
H_AFTER_T = H0 * DECAY_FACTOR               # ≈ 0.1537

# Variance in allele-frequency change per generation
VARIANCE = P0 * Q0 / TWO_N  # 0.0021

# Sanity checks
assert math.isclose(P_FIX, P0), "Fixation prob must equal initial frequency for neutral allele"
assert P_FIX != WRONG_P_FIX, "P(fix)=p0, NOT 1/(2N) for general initial frequency"
assert math.isclose(H0, 0.42, rel_tol=1e-9), "H0 = 2*p*q = 0.42"
assert H_AFTER_T < H0, "Heterozygosity must decay under drift"
assert math.isclose(VARIANCE, 0.0021, rel_tol=1e-9), "Variance = p*q/(2N)"

PRIOR_ERRORS = {
    "fixation_1_over_2N":   "Uses 1/(2N) as fixation prob for general p0 — only true for NEW single-copy mutation",
    "drift_only_small_pop": "Claims drift is negligible in large populations — wrong, just slower",
    "het_no_decay":         "Forgets that heterozygosity decays under drift: H(t) = H0*(1-1/(2N))^t",
}
