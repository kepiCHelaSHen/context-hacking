"""Feedback Stability (Routh-Hurwitz) — CHP Engineering Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from eng_feedback_stability_constants import STABLE_COEFFS, UNSTABLE_COEFFS


def routh_array_3rd(coeffs):
    """Build Routh array for a 3rd-order polynomial and return the first column.

    Parameters
    ----------
    coeffs : list of 4 numbers [a3, a2, a1, a0]
        Coefficients of a3*s³ + a2*s² + a1*s + a0 in descending power order.

    Returns
    -------
    list : First column of the Routh array [row3, row2, row1, row0].

    Routh array layout:
        Row 3:  a3,  a1
        Row 2:  a2,  a0
        Row 1:  (a2*a1 - a3*a0) / a2,  0
        Row 0:  a0
    """
    a3, a2, a1, a0 = coeffs
    row1_entry = (a2 * a1 - a3 * a0) / a2
    return [a3, a2, row1_entry, a0]


def count_sign_changes(column):
    """Count the number of sign changes in a sequence of real numbers.

    Parameters
    ----------
    column : list of numbers
        The first column of a Routh array.

    Returns
    -------
    int : Number of sign changes (each change = one RHP pole).
    """
    changes = 0
    for i in range(1, len(column)):
        if column[i - 1] * column[i] < 0:
            changes += 1
    return changes


def is_stable_routh(coeffs):
    """Determine stability via the full Routh-Hurwitz criterion.

    Parameters
    ----------
    coeffs : list of 4 numbers [a3, a2, a1, a0]

    Returns
    -------
    bool : True if stable (zero sign changes in first column), False otherwise.
    """
    first_col = routh_array_3rd(coeffs)
    return count_sign_changes(first_col) == 0


def necessary_condition(coeffs):
    """Check the necessary (but NOT sufficient) condition for stability.

    A polynomial can only be stable if ALL its coefficients are positive.
    However, this does NOT guarantee stability — the full Routh test is needed.

    Parameters
    ----------
    coeffs : list of numbers
        Polynomial coefficients in descending power order.

    Returns
    -------
    bool : True if all coefficients are positive.
    """
    return all(c > 0 for c in coeffs)


if __name__ == "__main__":
    # Stable example
    fc = routh_array_3rd(STABLE_COEFFS)
    sc = count_sign_changes(fc)
    print(f"Stable poly {STABLE_COEFFS}:")
    print(f"  First column: {fc}")
    print(f"  Sign changes: {sc} -> stable={is_stable_routh(STABLE_COEFFS)}")

    # Unstable example
    fc2 = routh_array_3rd(UNSTABLE_COEFFS)
    sc2 = count_sign_changes(fc2)
    print(f"\nUnstable poly {UNSTABLE_COEFFS}:")
    print(f"  First column: {fc2}")
    print(f"  Sign changes: {sc2} -> stable={is_stable_routh(UNSTABLE_COEFFS)}")
    print(f"  Necessary condition (all coeffs > 0): {necessary_condition(UNSTABLE_COEFFS)}")
    print(f"  ^^^ This passes, but the system is UNSTABLE -- necessary != sufficient!")
