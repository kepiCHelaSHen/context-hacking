"""
Nash Equilibrium — 2×2 Game Solutions — CHP Economics Sprint
Pure and mixed strategy Nash equilibria for 2×2 normal-form games.
All constants from frozen spec.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_nash_equilibrium_constants import (
    PD_MATRIX, BOS_MATRIX,
    BOS_MIXED_P, BOS_MIXED_Q,
    BOS_MIXED_PAYOFF_P1, BOS_MIXED_PAYOFF_P2,
)


def is_nash_pure(payoff_matrix, strategy_pair):
    """
    Check whether a strategy pair is a pure-strategy Nash equilibrium.

    Parameters
    ----------
    payoff_matrix : list[list[tuple]]
        2×2 matrix where payoff_matrix[i][j] = (P1_payoff, P2_payoff).
    strategy_pair : tuple[int, int]
        (row, col) indices of the strategy profile to check.

    Returns
    -------
    bool
        True if neither player can improve by unilateral deviation.
    """
    r, c = strategy_pair
    p1_payoff = payoff_matrix[r][c][0]
    p2_payoff = payoff_matrix[r][c][1]

    # Check P1: can P1 improve by switching row?
    for alt_r in range(2):
        if alt_r != r and payoff_matrix[alt_r][c][0] > p1_payoff:
            return False

    # Check P2: can P2 improve by switching column?
    for alt_c in range(2):
        if alt_c != c and payoff_matrix[r][alt_c][1] > p2_payoff:
            return False

    return True


def mixed_strategy_2x2(payoff_matrix):
    """
    Compute mixed strategy Nash equilibrium for a 2×2 game.

    KEY: Player 1's mixing probability p makes Player 2 INDIFFERENT.
         Player 2's mixing probability q makes Player 1 INDIFFERENT.

    Parameters
    ----------
    payoff_matrix : list[list[tuple]]
        2×2 matrix where payoff_matrix[i][j] = (P1_payoff, P2_payoff).

    Returns
    -------
    (p, q) : tuple[float, float] or None
        p = prob P1 plays row 0, q = prob P2 plays col 0.
        Returns None if no interior mixed NE exists (denominator is zero).
    """
    a11_1, a11_2 = payoff_matrix[0][0]
    a12_1, a12_2 = payoff_matrix[0][1]
    a21_1, a21_2 = payoff_matrix[1][0]
    a22_1, a22_2 = payoff_matrix[1][1]

    # p makes P2 indifferent (uses P2's payoffs):
    #   P2 col0 EV: a11_2*p + a21_2*(1-p)
    #   P2 col1 EV: a12_2*p + a22_2*(1-p)
    #   Set equal => p = (a22_2 - a21_2) / (a11_2 - a12_2 - a21_2 + a22_2)
    denom_p = a11_2 - a12_2 - a21_2 + a22_2
    if denom_p == 0:
        return None

    p = (a22_2 - a21_2) / denom_p

    # q makes P1 indifferent (uses P1's payoffs):
    #   P1 row0 EV: a11_1*q + a12_1*(1-q)
    #   P1 row1 EV: a21_1*q + a22_1*(1-q)
    #   Set equal => q = (a22_1 - a12_1) / (a11_1 - a12_1 - a21_1 + a22_1)
    denom_q = a11_1 - a12_1 - a21_1 + a22_1
    if denom_q == 0:
        return None

    q = (a22_1 - a12_1) / denom_q

    # Valid mixed NE requires 0 < p < 1 and 0 < q < 1
    if not (0 < p < 1 and 0 < q < 1):
        return None

    return (p, q)


def expected_payoff(payoff_matrix, p, q, player):
    """
    Compute expected payoff under mixed strategies.

    Parameters
    ----------
    payoff_matrix : list[list[tuple]]
        2×2 matrix where payoff_matrix[i][j] = (P1_payoff, P2_payoff).
    p : float
        Probability Player 1 plays row 0.
    q : float
        Probability Player 2 plays col 0.
    player : int
        1 for Player 1, 2 for Player 2.

    Returns
    -------
    float
        Expected payoff for the specified player.
    """
    if player not in (1, 2):
        raise ValueError(f"player must be 1 or 2, got {player!r}")

    idx = player - 1  # 0 for P1, 1 for P2
    ev = (    p   *     q   * payoff_matrix[0][0][idx]
          +   p   * (1 - q) * payoff_matrix[0][1][idx]
          + (1-p) *     q   * payoff_matrix[1][0][idx]
          + (1-p) * (1 - q) * payoff_matrix[1][1][idx])
    return ev


if __name__ == "__main__":
    print("=== Nash Equilibrium — 2×2 Games ===\n")

    # --- Prisoner's Dilemma ---
    print("--- Prisoner's Dilemma ---")
    print("  C\\C=(-1,-1)  C\\D=(-3,0)")
    print("  D\\C=(0,-3)   D\\D=(-2,-2)")
    for r in range(2):
        for c in range(2):
            label = f"({'CD'[r]},{'CD'[c]})"
            is_ne = is_nash_pure(PD_MATRIX, (r, c))
            print(f"  {label}: NE={is_ne}")
    mixed = mixed_strategy_2x2(PD_MATRIX)
    print(f"  Mixed NE: {mixed}")
    print()

    # --- Battle of the Sexes ---
    print("--- Battle of the Sexes ---")
    print("  O\\O=(3,2)  O\\F=(0,0)")
    print("  F\\O=(0,0)  F\\F=(2,3)")
    for r in range(2):
        for c in range(2):
            label = f"({'OF'[r]},{'OF'[c]})"
            is_ne = is_nash_pure(BOS_MATRIX, (r, c))
            print(f"  {label}: NE={is_ne}")
    result = mixed_strategy_2x2(BOS_MATRIX)
    if result:
        p, q = result
        print(f"  Mixed NE: p={p:.4f} (frozen={BOS_MIXED_P}), q={q:.4f} (frozen={BOS_MIXED_Q})")
        ep1 = expected_payoff(BOS_MATRIX, p, q, 1)
        ep2 = expected_payoff(BOS_MATRIX, p, q, 2)
        print(f"  Expected payoffs: P1={ep1:.4f} (frozen={BOS_MIXED_PAYOFF_P1}), P2={ep2:.4f} (frozen={BOS_MIXED_PAYOFF_P2})")
