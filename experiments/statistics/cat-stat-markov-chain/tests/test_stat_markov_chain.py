"""cat-stat-markov-chain — Steady-State & Transition Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_markov_chain_constants import *
IMPL = Path(__file__).parent.parent / "stat_markov_chain.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_rows_sum_to_one_not_columns(self):
        """Transition matrix rows must sum to 1 (not columns).

        The 'rows_not_summing' error constructs a matrix whose columns
        sum to 1 instead.  Our matrix P has row sums = 1, but for this
        specific P the column sums differ from 1.
        """
        m = _i()
        # Rows must sum to 1
        assert m.rows_sum_to_one(TRANS_MATRIX) is True
        # Columns should NOT all sum to 1 for this particular P
        col_sums = [sum(TRANS_MATRIX[i][j] for i in range(2)) for j in range(2)]
        for cs in col_sums:
            # At least one column sum must differ from 1
            pass
        # Column 0: 0.8+0.4=1.2, Column 1: 0.2+0.6=0.8 — neither is 1
        assert abs(col_sums[0] - 1.0) > 0.1
        assert abs(col_sums[1] - 1.0) > 0.1

    def test_steady_state_satisfies_pi_P_equals_pi(self):
        """Steady state must satisfy πP = π (LEFT eigenvector convention).

        The 'steady_wrong_direction' error solves Pπ = π instead.
        For non-symmetric P, Pπ = π gives a different vector.
        """
        m = _i()
        pi = m.steady_state_2x2(TRANS_MATRIX)
        # Verify πP = π:  [π₀, π₁] × P = [π₀, π₁]
        # (πP)ⱼ = Σᵢ πᵢ · P[i][j]
        for j in range(2):
            pi_P_j = sum(pi[i] * TRANS_MATRIX[i][j] for i in range(2))
            assert abs(pi_P_j - pi[j]) < 1e-12, (
                f"πP[{j}] = {pi_P_j} != π[{j}] = {pi[j]}"
            )

    def test_steady_state_is_normalized(self):
        """Steady state must sum to 1 — the 'forgets_normalization' error.

        An eigenvector found without normalization might have Σπᵢ ≠ 1.
        """
        m = _i()
        pi = m.steady_state_2x2(TRANS_MATRIX)
        assert abs(sum(pi) - 1.0) < 1e-12, (
            f"Σπᵢ = {sum(pi)}, expected 1.0"
        )


class TestCorrectness:
    def test_steady_state_values(self):
        """Steady state must match frozen constants [2/3, 1/3]."""
        m = _i()
        pi = m.steady_state_2x2(TRANS_MATRIX)
        for i in range(2):
            assert abs(pi[i] - STEADY_STATE[i]) < 1e-10, (
                f"π[{i}] = {pi[i]}, expected {STEADY_STATE[i]}"
            )

    def test_p_squared_values(self):
        """P² must match frozen P_SQUARED matrix."""
        m = _i()
        P2 = m.n_step_matrix(TRANS_MATRIX, 2)
        for i in range(2):
            for j in range(2):
                assert abs(P2[i][j] - P_SQUARED[i][j]) < 1e-10, (
                    f"P²[{i}][{j}] = {P2[i][j]}, expected {P_SQUARED[i][j]}"
                )

    def test_p_squared_rows_sum_to_one(self):
        """P² must also be a valid stochastic matrix (rows sum to 1)."""
        m = _i()
        P2 = m.n_step_matrix(TRANS_MATRIX, 2)
        assert m.rows_sum_to_one(P2)

    def test_rows_sum_to_one_rejects_bad_matrix(self):
        """rows_sum_to_one must reject a matrix with bad row sums."""
        m = _i()
        bad_P = [[0.5, 0.3], [0.4, 0.6]]  # row 0 sums to 0.8
        assert m.rows_sum_to_one(bad_P) is False

    def test_identity_is_p_to_zero(self):
        """P^0 should be the identity matrix."""
        m = _i()
        I = m.n_step_matrix(TRANS_MATRIX, 0)
        for i in range(2):
            for j in range(2):
                expected = 1.0 if i == j else 0.0
                assert abs(I[i][j] - expected) < 1e-12

    def test_mat_mult_associativity(self):
        """(P·P)·P should equal P·(P·P) — matrix multiplication is associative."""
        m = _i()
        PP = m.mat_mult(TRANS_MATRIX, TRANS_MATRIX)
        left = m.mat_mult(PP, TRANS_MATRIX)        # (P·P)·P = P³
        right = m.mat_mult(TRANS_MATRIX, PP)        # P·(P·P) = P³
        for i in range(2):
            for j in range(2):
                assert abs(left[i][j] - right[i][j]) < 1e-12
