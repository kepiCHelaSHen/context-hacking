"""Markowitz Portfolio Theory — CHP Economics Sprint.
Portfolio risk and return with proper covariance handling.
All constants from frozen spec.
"""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_portfolio_constants import *


def portfolio_return(weights, returns):
    """E(Rp) = sum(wi * E(Ri)). Weighted sum of expected returns."""
    return sum(w * r for w, r in zip(weights, returns))


def covariance(s1, s2, rho):
    """sigma12 = rho * sigma1 * sigma2. NOT just rho, NOT just s1*s2."""
    return rho * s1 * s2


def portfolio_variance_2asset(w1, w2, s1, s2, rho):
    """sigma_p^2 = w1^2*s1^2 + w2^2*s2^2 + 2*w1*w2*sigma12.
    INCLUDES the cross-covariance term. Without it, variance is WRONG."""
    cov12 = covariance(s1, s2, rho)
    return w1**2 * s1**2 + w2**2 * s2**2 + 2 * w1 * w2 * cov12


def portfolio_std(variance):
    """sigma_p = sqrt(variance). Standard deviation of portfolio."""
    return math.sqrt(variance)


def diversification_benefit(s1, s2, sp, w1, w2):
    """Benefit = weighted_avg_std - portfolio_std.
    Positive when rho < 1 (diversification reduces risk)."""
    weighted_avg = w1 * s1 + w2 * s2
    return weighted_avg - sp


if __name__ == "__main__":
    print("=== Markowitz Portfolio Theory ===\n")

    er_p = portfolio_return([W1, W2], [ER1, ER2])
    print(f"E(Rp) = {er_p:.4f} ({er_p*100:.2f}%)")

    cov12 = covariance(S1, S2, RHO)
    print(f"Covariance(1,2) = {cov12:.6f}")

    var_p = portfolio_variance_2asset(W1, W2, S1, S2, RHO)
    std_p = portfolio_std(var_p)
    print(f"Portfolio variance = {var_p:.6f}")
    print(f"Portfolio std dev  = {std_p:.5f} ({std_p*100:.2f}%)")

    # Show what happens WITHOUT covariance
    var_wrong = W1**2 * S1**2 + W2**2 * S2**2
    std_wrong = math.sqrt(var_wrong)
    print(f"\nWITHOUT covariance: std = {std_wrong:.5f} ({std_wrong*100:.2f}%) -- WRONG!")

    div_b = diversification_benefit(S1, S2, std_p, W1, W2)
    print(f"\nDiversification benefit = {div_b:.5f} ({div_b*100:.2f}%)")
