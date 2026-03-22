"""Markov Chains — CHP Statistics Sprint.  All constants from frozen spec."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_markov_chain_constants import *


def mat_mult(A, B):
    """Multiply two 2×2 matrices (nested lists).

    C[i][j] = Σ_k A[i][k] · B[k][j]
    """
    n = len(A)
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


def mat_vec(P, v):
    """Matrix-vector product Pv for square matrix P and vector v.

    result[i] = Σ_j P[i][j] · v[j]
    """
    n = len(P)
    result = [0.0] * n
    for i in range(n):
        for j in range(n):
            result[i] += P[i][j] * v[j]
    return result


def n_step_matrix(P, n):
    """Compute P^n via repeated matrix multiplication.

    Parameters
    ----------
    P : list[list[float]]   — transition matrix
    n : int                  — number of steps (n >= 1)
    """
    result = [[1.0 if i == j else 0.0 for j in range(len(P))]
              for i in range(len(P))]  # identity matrix
    for _ in range(n):
        result = mat_mult(result, P)
    return result


def steady_state_2x2(P):
    """Solve πP = π with Σπᵢ = 1 analytically for a 2-state chain.

    For the 2×2 transition matrix:
        P = [[a, b],
             [c, d]]
    where a + b = 1 and c + d = 1,

    πP = π gives:
        π₀·a + π₁·c = π₀   →   π₁·c = π₀·(1 − a) = π₀·b
        → π₀/π₁ = c/b

    With π₀ + π₁ = 1:
        π₀ = c / (b + c)
        π₁ = b / (b + c)
    """
    b = P[0][1]   # P(0→1)
    c = P[1][0]   # P(1→0)
    denom = b + c
    if denom == 0:
        raise ValueError("Absorbing chain: b + c = 0, no unique steady state")
    return [c / denom, b / denom]


def rows_sum_to_one(P):
    """Check that every row of P sums to 1 (within tolerance)."""
    tol = 1e-10
    for row in P:
        if abs(sum(row) - 1.0) > tol:
            return False
    return True


if __name__ == "__main__":
    print("Markov Chains — Sunny/Rainy Demo\n")
    print(f"  P = {TRANS_MATRIX}")
    print(f"  Rows sum to 1? {rows_sum_to_one(TRANS_MATRIX)}")

    pi = steady_state_2x2(TRANS_MATRIX)
    print(f"\n  Steady state pi = [{pi[0]:.10f}, {pi[1]:.10f}]")
    print(f"  Expected        = [{STEADY_STATE[0]:.10f}, {STEADY_STATE[1]:.10f}]")

    P2 = n_step_matrix(TRANS_MATRIX, 2)
    print(f"\n  P^2 = {P2}")
    print(f"  Expected P^2 = {P_SQUARED}")
