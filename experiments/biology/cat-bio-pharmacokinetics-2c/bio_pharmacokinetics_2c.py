"""Two-Compartment Pharmacokinetics — CHP Biology Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_pharmacokinetics_2c_constants import *


def two_compartment_C(A, alpha, B, beta, t):
    """Return concentration at time t: C(t) = A*e^(-alpha*t) + B*e^(-beta*t)."""
    return A * math.exp(-alpha * t) + B * math.exp(-beta * t)


def terminal_half_life(beta):
    """Return terminal (elimination) half-life: t½ = ln(2)/beta."""
    return math.log(2) / beta


def distribution_half_life(alpha):
    """Return distribution half-life: t½_dist = ln(2)/alpha."""
    return math.log(2) / alpha


def is_distribution_phase(A, alpha, B, beta, t, threshold=0.1):
    """Return True if the distribution term still contributes > threshold fraction of total.

    When the fast (alpha) exponential is negligible relative to total concentration,
    the system is in the terminal elimination phase.
    """
    dist_term = A * math.exp(-alpha * t)
    total = two_compartment_C(A, alpha, B, beta, t)
    if total <= 0:
        return False
    return (dist_term / total) > threshold


if __name__ == "__main__":
    print(f"A={A_COEFF}, B={B_COEFF}, alpha={ALPHA} /hr, beta={BETA} /hr")
    print(f"C(0) = {two_compartment_C(A_COEFF, ALPHA, B_COEFF, BETA, 0):.2f} mg/L")
    print(f"C(1) = {two_compartment_C(A_COEFF, ALPHA, B_COEFF, BETA, 1):.4f} mg/L")
    print(f"C(5) = {two_compartment_C(A_COEFF, ALPHA, B_COEFF, BETA, 5):.4f} mg/L")
    t_half = terminal_half_life(BETA)
    t_half_dist = distribution_half_life(ALPHA)
    print(f"Terminal t1/2 = ln(2)/beta = {t_half:.4f} hr")
    print(f"Distribution t1/2 = ln(2)/alpha = {t_half_dist:.4f} hr")
    print(f"WRONG terminal t1/2 = ln(2)/alpha = {t_half_dist:.4f} hr (10x too short!)")
    print(f"Distribution phase at t=0.5? {is_distribution_phase(A_COEFF, ALPHA, B_COEFF, BETA, 0.5)}")
    print(f"Distribution phase at t=5.0? {is_distribution_phase(A_COEFF, ALPHA, B_COEFF, BETA, 5.0)}")
