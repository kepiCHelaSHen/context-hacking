"""
Radioactive Decay — CHP Chemistry Sprint
Decay constants, remaining atoms, activity, C-14 dating, secular equilibrium.
All constants from frozen spec.
"""
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from chem_radioactive_decay_constants import (
    LN2, U238_HALF_LIFE, TH234_HALF_LIFE, RA226_HALF_LIFE,
    C14_HALF_LIFE, C14_LIBBY_WRONG,
)


def decay_constant(half_life):
    """Lambda = ln(2) / t_half."""
    return LN2 / half_life


def n_remaining(N0, half_life, t):
    """N(t) = N0 * exp(-lambda * t)."""
    lam = decay_constant(half_life)
    return N0 * math.exp(-lam * t)


def activity(N, half_life):
    """A = lambda * N."""
    return decay_constant(half_life) * N


def age_from_ratio(ratio, half_life):
    """t = -ln(ratio) * half_life / ln(2)."""
    return -math.log(ratio) * half_life / LN2


def c14_age(fraction_remaining):
    """C-14 age using CORRECT half-life = 5730 years (Godwin), NOT 5568 (Libby)."""
    return age_from_ratio(fraction_remaining, C14_HALF_LIFE)


def secular_eq_ratio(lam1, lam2):
    """At secular equilibrium, N2/N1 = lambda1/lambda2 (NOT N1=N2)."""
    return lam1 / lam2


if __name__ == "__main__":
    print("=== Radioactive Decay ===\n")

    age_half = c14_age(0.5)
    print(f"C-14 age at 50% remaining: {age_half:.0f} years")
    print(f"  Correct half-life: {C14_HALF_LIFE} years (Godwin 1962)")
    print(f"  Wrong (Libby):     {C14_LIBBY_WRONG} years — DO NOT USE\n")

    lam_U238 = decay_constant(U238_HALF_LIFE)
    lam_Th234 = decay_constant(TH234_HALF_LIFE)
    ratio = secular_eq_ratio(lam_U238, lam_Th234)
    print(f"Secular equilibrium U238/Th234:")
    print(f"  N(Th234)/N(U238) = {ratio:.6e}")
    print(f"  Atoms are NOT equal — activities are equal!")
    print(f"  A(U238) = A(Th234) at secular equilibrium")
