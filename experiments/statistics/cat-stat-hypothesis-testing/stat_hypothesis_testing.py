"""Hypothesis Testing — CHP Statistics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_hypothesis_testing_constants import *

def z_test_statistic(xbar, mu0, sigma, n):
    """z = (xbar - mu0) / (sigma / sqrt(n))"""
    return (xbar - mu0) / (sigma / math.sqrt(n))

def p_value_two_tailed(z):
    """Two-tailed p-value: 2*(1 - Phi(|z|)) = 1 - erf(|z| / sqrt(2))."""
    return 1.0 - math.erf(abs(z) / math.sqrt(2))

def reject_h0(p_value, alpha):
    """Reject H0 when p-value < alpha."""
    return p_value < alpha

def type_i_error_rate():
    """Type I error rate equals the significance level alpha."""
    return ALPHA_05

def power(beta):
    """Power = 1 - beta (probability of correctly rejecting a false H0)."""
    return 1.0 - beta

if __name__ == "__main__":
    z = z_test_statistic(XBAR, MU_0, SIGMA, N)
    p = p_value_two_tailed(z)
    print(f"z = {z:.4f}, p = {p:.5f}")
    print(f"Reject H0 at alpha=0.05? {reject_h0(p, ALPHA_05)}")
    print(f"Reject H0 at alpha=0.01? {reject_h0(p, ALPHA_01)}")
    print(f"Type I error rate: {type_i_error_rate()}")
    print(f"Power (beta=0.20): {power(0.20):.2f}")
