"""Central Limit Theorem — Frozen Constants. Source: Lindeberg-Lévy. DO NOT MODIFY."""
import math

# ── CLT Statement ────────────────────────────────────────────────────
# For iid random variables X₁, X₂, …, Xₙ with FINITE mean μ and
# FINITE variance σ², the sampling distribution of x̄ approaches
# N(μ, σ²/n) as n → ∞.  (Lindeberg-Lévy CLT)

# ── KEY requirement: finite mean AND finite variance ─────────────────
# Cauchy distribution violates BOTH:
#   - No finite mean  (integral diverges)
#   - No finite variance  (no mean ⇒ variance undefined)
# The mean of n Cauchy r.v.s is STILL Cauchy (NOT normal).
# This is the most famous counterexample to naive CLT claims.
CAUCHY_HAS_MEAN = False
CAUCHY_HAS_VARIANCE = False
CLT_APPLIES_CAUCHY = False  # CLT does NOT apply to Cauchy

# ── Test scenario: X ~ Uniform(0, 1) ────────────────────────────────
# μ = (a+b)/2 = 0.5
# σ² = (b−a)²/12 = 1/12
# σ = 1/√12 ≈ 0.28868
MU_UNIFORM = 0.5
VAR_UNIFORM = 1.0 / 12.0                            # 0.08333333...
SIGMA_UNIFORM = math.sqrt(VAR_UNIFORM)               # 0.28867513...

# Standard error of the mean: SE = σ / √n
SE_30 = SIGMA_UNIFORM / math.sqrt(30)                # 0.05270462...
SE_100 = SIGMA_UNIFORM / math.sqrt(100)              # 0.02886751...

# ── Prior errors (LLM misconceptions) ───────────────────────────────
PRIOR_ERRORS = {
    "clt_all_distributions":
        "Claims CLT applies to ALL distributions including Cauchy — "
        "WRONG: Cauchy has no finite mean or variance, so CLT does not apply",
    "se_sigma_not_over_sqrt_n":
        "Uses σ as the standard error instead of σ/√n — "
        "misses the √n denominator that shrinks spread with sample size",
    "finite_mean_sufficient":
        "Thinks only a finite mean is required for CLT — "
        "WRONG: both finite mean AND finite variance are necessary",
}
