"""Maximum Likelihood Estimation — CHP Statistics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_mle_constants import *


def mle_mean(data):
    """MLE of μ for Normal distribution = sample mean."""
    return sum(data) / len(data)


def mle_variance(data):
    """MLE of σ² for Normal distribution = (1/n) Σ(xi - x̄)².
    NOTE: divides by n (biased), NOT n-1."""
    n = len(data)
    mu = mle_mean(data)
    return sum((x - mu) ** 2 for x in data) / n


def unbiased_variance(data):
    """Unbiased estimator of σ² = (1/(n-1)) Σ(xi - x̄)²."""
    n = len(data)
    mu = mle_mean(data)
    return sum((x - mu) ** 2 for x in data) / (n - 1)


def mle_exp_lambda(data):
    """MLE of λ for Exponential(λ) distribution = 1/x̄."""
    return 1.0 / mle_mean(data)


def normal_loglikelihood(data, mu, sigma_sq):
    """Log-likelihood for Normal(μ, σ²) given data.
    ℓ = -(n/2)ln(2π) - (n/2)ln(σ²) - (1/(2σ²)) Σ(xi - μ)²
    """
    n = len(data)
    ss = sum((x - mu) ** 2 for x in data)
    return -(n / 2) * math.log(2 * math.pi) - (n / 2) * math.log(sigma_sq) - ss / (2 * sigma_sq)


if __name__ == "__main__":
    data = list(DATA)
    mu = mle_mean(data)
    var_mle = mle_variance(data)
    var_ub = unbiased_variance(data)
    lam = mle_exp_lambda(data)
    ll = normal_loglikelihood(data, mu, var_mle)
    print(f"Data: {data}")
    print(f"MLE mu = {mu}")
    print(f"MLE var = {var_mle} (biased, /n)  vs  unbiased s2 = {var_ub} (/n-1)")
    print(f"MLE sigma = {math.sqrt(var_mle):.5f}  vs  s = {math.sqrt(var_ub):.5f}")
    print(f"Exp MLE lambda = {lam:.5f}")
    print(f"Normal log-likelihood at MLE = {ll:.4f}")
