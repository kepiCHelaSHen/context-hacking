"""cat-stat-mann-whitney — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_mann_whitney_constants import *
IMPL = Path(__file__).parent.parent / "stat_mann_whitney.py"


def _i():
    if not IMPL.exists():
        pytest.skip("not yet written")
    import importlib.util
    s = importlib.util.spec_from_file_location("m", IMPL)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


class TestPriorErrors:
    """Guards against the documented LLM errors."""

    def test_u1_plus_u2_equals_n1n2(self):
        """U1 + U2 must always equal n1*n2 (catches u_formula_wrong)."""
        m = _i()
        u1, u2, u = m.mann_whitney_u(GROUP_A, GROUP_B)
        assert abs((u1 + u2) - N1 * N2) < 1e-9

    def test_u_is_min(self):
        """U must be min(U1, U2), not just U1 or U2 (catches u_not_min)."""
        m = _i()
        u1, u2, u = m.mann_whitney_u(GROUP_A, GROUP_B)
        assert u == min(u1, u2)

    def test_ranks_start_at_1(self):
        """Ranks must be 1-based, not 0-based (catches ranks_from_1)."""
        m = _i()
        ranks = m.rank_combined(GROUP_A, GROUP_B)
        assert min(ranks.values()) >= 1

    def test_u_check_identity(self):
        """u_check must confirm the identity."""
        m = _i()
        u1, u2, _ = m.mann_whitney_u(GROUP_A, GROUP_B)
        assert m.u_check(u1, u2, N1, N2)


class TestCorrectness:
    """Verify computed values against frozen constants."""

    def test_R1(self):
        m = _i()
        ranks = m.rank_combined(GROUP_A, GROUP_B)
        r1 = sum(ranks[v] for v in GROUP_A)
        assert abs(r1 - R1) < 1e-9

    def test_R2(self):
        m = _i()
        ranks = m.rank_combined(GROUP_A, GROUP_B)
        r2 = sum(ranks[v] for v in GROUP_B)
        assert abs(r2 - R2) < 1e-9

    def test_U1(self):
        m = _i()
        u1, _, _ = m.mann_whitney_u(GROUP_A, GROUP_B)
        assert abs(u1 - U1) < 1e-9

    def test_U2(self):
        m = _i()
        _, u2, _ = m.mann_whitney_u(GROUP_A, GROUP_B)
        assert abs(u2 - U2) < 1e-9

    def test_U_stat(self):
        m = _i()
        _, _, u = m.mann_whitney_u(GROUP_A, GROUP_B)
        assert abs(u - U_STAT) < 1e-9
