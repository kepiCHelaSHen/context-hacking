"""Maximum Likelihood Estimation — Frozen Constants. Source: Fisher 1922 / Casella & Berger. DO NOT MODIFY."""
import math

# MLE for Normal distribution:
#   MLE of μ  = x̄ (sample mean)
#   MLE of σ² = (1/n) Σ(xi - x̄)²   — divides by n, NOT n-1
#   This is a BIASED estimator of σ².  The unbiased estimator divides by n-1.
#
# MLE for Exponential(λ):
#   MLE of λ = 1/x̄   (NOT x̄)
#
# Normal log-likelihood at MLE:
#   ℓ(μ,σ²|x) = -(n/2)ln(2π) - (n/2)ln(σ²) - (1/(2σ²)) Σ(xi - x̄)²

# ---------- test data ----------
DATA = (2, 4, 6, 8, 10)
N = 5
XBAR = 6.0                             # sample mean

# sum of squared deviations
_SS = sum((x - XBAR) ** 2 for x in DATA)   # (−4)²+(−2)²+0²+2²+4² = 40

MLE_VAR     = _SS / N          # 40/5 = 8.0   (biased — divides by n)
UNBIASED_VAR = _SS / (N - 1)   # 40/4 = 10.0  (unbiased — divides by n-1)

MLE_SIGMA          = math.sqrt(MLE_VAR)       # √8  ≈ 2.82843
UNBIASED_SIGMA     = math.sqrt(UNBIASED_VAR)  # √10 ≈ 3.16228

MLE_LAMBDA_EXP = 1.0 / XBAR   # 1/6 ≈ 0.16667  (MLE of exponential rate)

# Normal log-likelihood evaluated at MLE (μ=x̄, σ²=MLE_VAR)
LOGLIK_AT_MLE = (
    -(N / 2) * math.log(2 * math.pi)
    - (N / 2) * math.log(MLE_VAR)
    - _SS / (2 * MLE_VAR)
)
# = -(5/2)ln(2π) - (5/2)ln(8) - 40/16
# = -2.5·1.8379 - 2.5·2.0794 - 2.5
# = -4.5948 - 5.1986 - 2.5
# ≈ -12.2934

PRIOR_ERRORS = {
    "mle_var_unbiased": "Uses n-1 in denominator for MLE variance — that gives the unbiased estimator, not the MLE",
    "exp_mle_xbar":     "Claims MLE of exponential λ is x̄ instead of 1/x̄",
    "loglik_sign":      "Wrong sign on log-likelihood (positive instead of negative)",
}
