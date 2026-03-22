"""Solow Growth Model — CHP Economics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_solow_model_constants import *


def steady_state_k(s, n, delta, alpha):
    """Compute steady-state capital per worker.

    k* = (s / (n + delta))^(1/(1-alpha))

    KEY: denominator is (n + delta), NOT just delta.
    Population growth dilutes capital per worker.
    """
    return (s / (n + delta)) ** (1 / (1 - alpha))


def steady_state_y(k_star, alpha):
    """Compute steady-state output per worker: y* = k*^alpha."""
    return k_star ** alpha


def golden_rule_k(alpha, n, delta):
    """Compute golden-rule capital per worker.

    Maximises steady-state consumption: MPK = n + delta
    => k_gold = (alpha / (n + delta))^(1/(1-alpha))
    """
    return (alpha / (n + delta)) ** (1 / (1 - alpha))


def break_even_investment(n, delta, k):
    """Break-even investment: (n + delta) * k.

    The amount of investment needed just to keep k constant,
    replacing depreciated capital AND equipping new workers.
    """
    return (n + delta) * k


def actual_investment(s, k, alpha):
    """Actual investment per worker: s * f(k) = s * k^alpha."""
    return s * k ** alpha


if __name__ == "__main__":
    # Steady-state computation
    k_s = steady_state_k(S_TEST, N_TEST, DELTA_TEST, ALPHA_TEST)
    y_s = steady_state_y(k_s, ALPHA_TEST)
    print(f"Parameters: s={S_TEST}, alpha={ALPHA_TEST:.4f}, n={N_TEST}, delta={DELTA_TEST}")
    print(f"n + delta = {N_TEST + DELTA_TEST}")
    print(f"k* = {k_s:.6f}")
    print(f"y* = {y_s:.6f}")

    # Show the error from ignoring population growth
    k_wrong = steady_state_k(S_TEST, 0, DELTA_TEST, ALPHA_TEST)
    print(f"\nWRONG k* (only delta): {k_wrong:.6f}")
    print(f"Error: {(k_wrong - k_s) / k_s * 100:.1f}% too high!")

    # Golden rule
    k_g = golden_rule_k(ALPHA_TEST, N_TEST, DELTA_TEST)
    print(f"\nGolden rule k = {k_g:.6f}")
    print(f"MPK at golden rule = {ALPHA_TEST * k_g ** (ALPHA_TEST - 1):.6f} (should be {N_TEST + DELTA_TEST})")

    # Transition dynamics
    print(f"\nAt k={K_LOW}: actual inv = {actual_investment(S_TEST, K_LOW, ALPHA_TEST):.4f}, "
          f"break-even inv = {break_even_investment(N_TEST, DELTA_TEST, K_LOW):.4f}, "
          f"k_dot > 0 (accumulating)")
    print(f"At k={K_HIGH}: actual inv = {actual_investment(S_TEST, K_HIGH, ALPHA_TEST):.4f}, "
          f"break-even inv = {break_even_investment(N_TEST, DELTA_TEST, K_HIGH):.4f}, "
          f"k_dot < 0 (decumulating)")
