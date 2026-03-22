"""cat-bio-pharmacokinetics-2c — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_pharmacokinetics_2c_constants import *
IMPL = Path(__file__).parent.parent / "bio_pharmacokinetics_2c.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_alpha_greater_than_beta(self):
        """Distribution (alpha) must be faster than elimination (beta)."""
        assert ALPHA > BETA, \
            f"alpha={ALPHA} must be > beta={BETA} (distribution faster than elimination)"

    def test_terminal_half_life_uses_beta_not_alpha(self):
        """The #1 LLM error: using alpha for terminal t½ instead of beta."""
        m = _i()
        t_half = m.terminal_half_life(BETA)
        assert math.isclose(t_half, TERMINAL_HALF_LIFE, rel_tol=1e-9), \
            f"Terminal t½ should be ln(2)/beta={TERMINAL_HALF_LIFE:.4f}, got {t_half:.4f}"
        assert not math.isclose(t_half, WRONG_TERMINAL_HALF_LIFE, rel_tol=0.01), \
            f"Got ln(2)/alpha={WRONG_TERMINAL_HALF_LIFE:.4f} — must use beta, not alpha!"

    def test_biexponential_not_single_exponential(self):
        """Single-exponential approximation gives wrong C(1)."""
        m = _i()
        c_biexp = m.two_compartment_C(A_COEFF, ALPHA, B_COEFF, BETA, 1.0)
        assert math.isclose(c_biexp, C_AT_1, rel_tol=1e-6), \
            f"Biexponential C(1)={C_AT_1:.4f}, got {c_biexp:.4f}"
        assert not math.isclose(c_biexp, C_AT_1_SINGLE_EXP, rel_tol=0.05), \
            f"C(1) matches single-exp approx {C_AT_1_SINGLE_EXP:.4f} — must use biexponential!"

    def test_alpha_beta_roles_not_swapped(self):
        """If alpha/beta are swapped, C(1) would be wrong."""
        m = _i()
        # Correct: A*exp(-alpha*t) + B*exp(-beta*t)
        correct = m.two_compartment_C(A_COEFF, ALPHA, B_COEFF, BETA, 1.0)
        # Swapped: A*exp(-beta*t) + B*exp(-alpha*t) — different result
        swapped = m.two_compartment_C(A_COEFF, BETA, B_COEFF, ALPHA, 1.0)
        assert math.isclose(correct, C_AT_1, rel_tol=1e-9), \
            f"C(1) should be {C_AT_1:.4f}, got {correct:.4f}"
        assert not math.isclose(correct, swapped, rel_tol=0.01), \
            "Swapping alpha/beta gives different result — roles must not be confused"


class TestCorrectness:
    def test_C_at_0_equals_A_plus_B(self):
        m = _i()
        c0 = m.two_compartment_C(A_COEFF, ALPHA, B_COEFF, BETA, 0)
        assert math.isclose(c0, C_AT_0, rel_tol=1e-9), \
            f"C(0) should be A+B={C_AT_0}, got {c0}"

    def test_C_at_1(self):
        m = _i()
        c1 = m.two_compartment_C(A_COEFF, ALPHA, B_COEFF, BETA, 1.0)
        assert math.isclose(c1, C_AT_1, rel_tol=1e-6), \
            f"C(1) should be {C_AT_1:.4f}, got {c1:.4f}"

    def test_C_at_5(self):
        m = _i()
        c5 = m.two_compartment_C(A_COEFF, ALPHA, B_COEFF, BETA, 5.0)
        assert math.isclose(c5, C_AT_5, rel_tol=1e-6), \
            f"C(5) should be {C_AT_5:.4f}, got {c5:.4f}"

    def test_terminal_half_life_value(self):
        m = _i()
        t_half = m.terminal_half_life(BETA)
        assert math.isclose(t_half, 3.465735902799726, rel_tol=1e-9), \
            f"Terminal t½ should be 3.4657, got {t_half:.4f}"

    def test_distribution_half_life_value(self):
        m = _i()
        t_half_dist = m.distribution_half_life(ALPHA)
        assert math.isclose(t_half_dist, 0.34657359027997264, rel_tol=1e-9), \
            f"Distribution t½ should be 0.3466, got {t_half_dist:.4f}"

    def test_distribution_phase_early(self):
        """At t=0.5, the distribution term is still significant."""
        m = _i()
        assert m.is_distribution_phase(A_COEFF, ALPHA, B_COEFF, BETA, 0.5), \
            "At t=0.5, system should still be in distribution phase"

    def test_elimination_phase_late(self):
        """At t=5, the distribution term is negligible — terminal phase only."""
        m = _i()
        assert not m.is_distribution_phase(A_COEFF, ALPHA, B_COEFF, BETA, 5.0), \
            "At t=5, distribution term should be negligible (terminal phase)"
