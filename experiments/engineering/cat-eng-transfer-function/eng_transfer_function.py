"""Transfer Function — CHP Engineering Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_transfer_function_constants import NUM_COEFFS, DEN_COEFFS


def dc_gain(num_coeffs, den_coeffs):
    """H(0) = N(0)/D(0). Evaluate polynomial at s=0 → last coefficient."""
    n0 = num_coeffs[-1]
    d0 = den_coeffs[-1]
    if d0 == 0:
        return float('inf')
    return n0 / d0


def is_stable(poles):
    """BIBO stable iff ALL poles have Re(s) < 0."""
    return all(
        (p.real if isinstance(p, complex) else p) < 0
        for p in poles
    )


def find_roots_quadratic(a, b, c):
    """Roots of as² + bs + c via quadratic formula. Returns list of 2 roots."""
    disc = b**2 - 4*a*c
    if disc >= 0:
        sqrt_d = math.sqrt(disc)
        return [(-b + sqrt_d) / (2*a), (-b - sqrt_d) / (2*a)]
    else:
        sqrt_d = math.sqrt(-disc)
        return [complex(-b / (2*a), sqrt_d / (2*a)),
                complex(-b / (2*a), -sqrt_d / (2*a))]


def pole_zero_from_factored(zeros, poles, s):
    """Evaluate H(s) = K * prod(s - z_i) / prod(s - p_i) with K=1."""
    num = 1.0
    for z in zeros:
        num *= (s - z)
    den = 1.0
    for p in poles:
        den *= (s - p)
    if den == 0:
        return float('inf')
    return num / den


if __name__ == "__main__":
    gain = dc_gain(NUM_COEFFS, DEN_COEFFS)
    print(f"DC gain H(0) = {gain:.4f}")
    poles = find_roots_quadratic(1.0, 4.0, 3.0)
    print(f"Poles: {poles} -> stable={is_stable(poles)}")
    print(f"H(0) from factored: {pole_zero_from_factored([-2.0], [-1.0, -3.0], 0):.4f}")
