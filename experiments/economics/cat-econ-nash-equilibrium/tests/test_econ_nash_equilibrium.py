"""econ-nash-equilibrium — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_nash_equilibrium_constants import *

IMPL = Path(__file__).parent.parent / "econ_nash_equilibrium.py"


def _i():
    if not IMPL.exists():
        pytest.skip("implementation not yet written")
    import importlib.util
    spec = importlib.util.spec_from_file_location("impl", IMPL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── Prior Error Tests ─────────────────────────────────────────────────

class TestPriorErrors:
    """Each test catches one known LLM prior error."""

    def test_mixed_makes_opponent_indifferent_not_self(self):
        """PRIOR: mixed_makes_self_indifferent — must use opponent's payoffs."""
        mod = _i()
        result = mod.mixed_strategy_2x2(BOS_MATRIX)
        assert result is not None, "BoS should have a mixed NE"
        p, q = result
        # p makes P2 indifferent => uses P2's payoffs (col 1 of tuples)
        # If wrongly using own payoffs: p = (2-0)/(3-0-0+2) = 2/5 (WRONG)
        # Correct: p = (3-0)/(2-0-0+3) = 3/5
        assert abs(p - BOS_MIXED_P) < 1e-9, (
            f"p={p}, expected {BOS_MIXED_P}: P1 mixes to make P2 indifferent (use P2's payoffs)"
        )
        assert abs(q - BOS_MIXED_Q) < 1e-9, (
            f"q={q}, expected {BOS_MIXED_Q}: P2 mixes to make P1 indifferent (use P1's payoffs)"
        )

    def test_dominant_strategy_is_nash(self):
        """PRIOR: dominant_not_nash — dominant strategy implies Nash, verify (D,D) is NE."""
        mod = _i()
        # (D,D) = (1,1) must be a Nash equilibrium in PD
        assert mod.is_nash_pure(PD_MATRIX, (1, 1)), (
            "Defect is dominant for both players, so (D,D) must be Nash"
        )
        # (C,C) = (0,0) must NOT be a Nash equilibrium
        assert not mod.is_nash_pure(PD_MATRIX, (0, 0)), (
            "(C,C) is not Nash: either player can improve by defecting"
        )

    def test_mixed_prob_not_swapped(self):
        """PRIOR: mixed_prob_wrong — p belongs to P1, q belongs to P2."""
        mod = _i()
        result = mod.mixed_strategy_2x2(BOS_MATRIX)
        assert result is not None
        p, q = result
        # If swapped: p=2/5 and q=3/5 — wrong
        # Correct: p=3/5 and q=2/5
        assert p != q, "p and q should differ for BoS"
        assert p > q, f"For BoS, p=3/5 > q=2/5 but got p={p}, q={q}"
        assert abs(p - BOS_MIXED_P) < 1e-9
        assert abs(q - BOS_MIXED_Q) < 1e-9


# ── Correctness Tests ─────────────────────────────────────────────────

class TestCorrectness:
    """Each test verifies result against frozen spec."""

    # -- Pure strategy NE --

    def test_pd_unique_nash_at_defect_defect(self):
        mod = _i()
        assert mod.is_nash_pure(PD_MATRIX, (1, 1))
        # All other cells should NOT be NE
        for pair in [(0, 0), (0, 1), (1, 0)]:
            assert not mod.is_nash_pure(PD_MATRIX, pair), f"{pair} should not be NE in PD"

    def test_bos_two_pure_nash(self):
        mod = _i()
        pure_ne = [pair for pair in [(0,0),(0,1),(1,0),(1,1)]
                   if mod.is_nash_pure(BOS_MATRIX, pair)]
        assert sorted(pure_ne) == sorted(BOS_PURE_NE), (
            f"BoS pure NE: {pure_ne}, expected {BOS_PURE_NE}"
        )

    def test_bos_pure_ne_payoffs(self):
        mod = _i()
        for pair, expected in zip(BOS_PURE_NE, BOS_PURE_NE_PAYOFFS):
            actual = BOS_MATRIX[pair[0]][pair[1]]
            assert actual == expected

    # -- Mixed strategy NE --

    def test_pd_no_mixed_ne(self):
        mod = _i()
        result = mod.mixed_strategy_2x2(PD_MATRIX)
        assert result is None, "PD has dominant strategies, no interior mixed NE"

    def test_bos_mixed_ne_values(self):
        mod = _i()
        result = mod.mixed_strategy_2x2(BOS_MATRIX)
        assert result is not None
        p, q = result
        assert abs(p - BOS_MIXED_P) < 1e-9
        assert abs(q - BOS_MIXED_Q) < 1e-9

    def test_bos_mixed_probabilities_in_unit_interval(self):
        mod = _i()
        result = mod.mixed_strategy_2x2(BOS_MATRIX)
        assert result is not None
        p, q = result
        assert 0 < p < 1, f"p={p} must be in (0,1)"
        assert 0 < q < 1, f"q={q} must be in (0,1)"

    # -- Expected payoffs --

    def test_bos_mixed_expected_payoff_p1(self):
        mod = _i()
        ep1 = mod.expected_payoff(BOS_MATRIX, BOS_MIXED_P, BOS_MIXED_Q, 1)
        assert abs(ep1 - BOS_MIXED_PAYOFF_P1) < 1e-9, (
            f"P1 expected payoff={ep1}, expected {BOS_MIXED_PAYOFF_P1}"
        )

    def test_bos_mixed_expected_payoff_p2(self):
        mod = _i()
        ep2 = mod.expected_payoff(BOS_MATRIX, BOS_MIXED_P, BOS_MIXED_Q, 2)
        assert abs(ep2 - BOS_MIXED_PAYOFF_P2) < 1e-9, (
            f"P2 expected payoff={ep2}, expected {BOS_MIXED_PAYOFF_P2}"
        )

    def test_expected_payoff_at_pure_ne(self):
        """Expected payoff with deterministic strategies should match matrix entry."""
        mod = _i()
        # (Opera, Opera) => p=1, q=1
        ep1 = mod.expected_payoff(BOS_MATRIX, 1.0, 1.0, 1)
        ep2 = mod.expected_payoff(BOS_MATRIX, 1.0, 1.0, 2)
        assert abs(ep1 - 3.0) < 1e-9
        assert abs(ep2 - 2.0) < 1e-9

    def test_expected_payoff_invalid_player_raises(self):
        mod = _i()
        with pytest.raises(ValueError):
            mod.expected_payoff(BOS_MATRIX, 0.5, 0.5, 3)

    def test_p2_indifferent_at_mixed_ne(self):
        """At mixed NE, P2 must be indifferent between Opera and Fight."""
        mod = _i()
        p = BOS_MIXED_P
        # P2 payoff from Opera (col 0): a11_2*p + a21_2*(1-p) = 2*p + 0*(1-p) = 2p
        ev_opera = BOS_MATRIX[0][0][1] * p + BOS_MATRIX[1][0][1] * (1 - p)
        # P2 payoff from Fight (col 1): a12_2*p + a22_2*(1-p) = 0*p + 3*(1-p) = 3-3p
        ev_fight = BOS_MATRIX[0][1][1] * p + BOS_MATRIX[1][1][1] * (1 - p)
        assert abs(ev_opera - ev_fight) < 1e-9, (
            f"P2 not indifferent: Opera EV={ev_opera}, Fight EV={ev_fight}"
        )

    def test_p1_indifferent_at_mixed_ne(self):
        """At mixed NE, P1 must be indifferent between Opera and Fight."""
        mod = _i()
        q = BOS_MIXED_Q
        # P1 payoff from Opera (row 0): a11_1*q + a12_1*(1-q) = 3*q + 0*(1-q) = 3q
        ev_opera = BOS_MATRIX[0][0][0] * q + BOS_MATRIX[0][1][0] * (1 - q)
        # P1 payoff from Fight (row 1): a21_1*q + a22_1*(1-q) = 0*q + 2*(1-q) = 2-2q
        ev_fight = BOS_MATRIX[1][0][0] * q + BOS_MATRIX[1][1][0] * (1 - q)
        assert abs(ev_opera - ev_fight) < 1e-9, (
            f"P1 not indifferent: Opera EV={ev_opera}, Fight EV={ev_fight}"
        )
