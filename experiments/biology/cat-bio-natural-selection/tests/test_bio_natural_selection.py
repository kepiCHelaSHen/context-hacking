"""cat-bio-natural-selection -- Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_natural_selection_constants import *

IMPL = Path(__file__).parent.parent / "bio_natural_selection.py"


def _i():
    if not IMPL.exists():
        pytest.skip("not yet written")
    import importlib.util
    s = importlib.util.spec_from_file_location("m", IMPL)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


class TestPriorErrors:
    """Guard against known LLM mistakes."""

    def test_additive_ne_multiplicative(self):
        """Additive and multiplicative heterozygote fitness differ when s is large."""
        m = _i()
        wAA, wAa, waa = m.fitness_values(S, H)
        wAa_mult = m.multiplicative_heterozygote(wAA, waa)
        # They must NOT be equal for s = 0.4
        assert abs(wAa - wAa_mult) > 0.01, (
            "additive_equals_multiplicative: additive and multiplicative models "
            "should differ for large s"
        )

    def test_delta_p_includes_wbar_denominator(self):
        """Delta-p must divide by w-bar; without it the value is too large."""
        m = _i()
        wAA, wAa, waa = m.fitness_values(S, H)
        dp = m.delta_p(P_TEST, wAA, wAa, waa)
        # Numerator alone (without w-bar) = 0.042; correct answer ~ 0.05833
        # If someone forgets w-bar, dp = 0.042 which is < 0.05
        numerator_only = (P_TEST * Q_TEST
                          * (P_TEST * (wAA - wAa) + Q_TEST * (wAa - waa)))
        assert abs(dp - numerator_only) > 0.01, (
            "delta_p_no_wbar: delta-p should differ from raw numerator "
            "(must divide by w-bar)"
        )

    def test_h_matters(self):
        """Dominance coefficient h must affect heterozygote fitness."""
        m = _i()
        _, wAa_h0, _ = m.fitness_values(S, 0.0)
        _, wAa_h05, _ = m.fitness_values(S, 0.5)
        _, wAa_h1, _ = m.fitness_values(S, 1.0)
        assert wAa_h0 > wAa_h05 > wAa_h1, (
            "h_ignored: changing h must change heterozygote fitness"
        )


class TestCorrectness:
    """Verify numerical accuracy against frozen constants."""

    def test_fitness_values(self):
        m = _i()
        wAA, wAa, waa = m.fitness_values(S, H)
        assert abs(wAA - W_AA) < 1e-9
        assert abs(wAa - W_Aa) < 1e-9
        assert abs(waa - W_aa) < 1e-9

    def test_mean_fitness(self):
        m = _i()
        w_bar = m.mean_fitness(P_TEST, W_AA, W_Aa, W_aa)
        assert abs(w_bar - W_BAR) < 1e-9

    def test_delta_p(self):
        m = _i()
        dp = m.delta_p(P_TEST, W_AA, W_Aa, W_aa)
        assert abs(dp - DELTA_P) < 1e-9

    def test_multiplicative_heterozygote(self):
        m = _i()
        wAa_mult = m.multiplicative_heterozygote(W_AA, W_aa)
        assert abs(wAa_mult - W_Aa_MULT) < 1e-6

    def test_multiplicative_ne_additive_at_large_s(self):
        """Explicit numeric check: 0.8 != 0.7746."""
        m = _i()
        wAa_mult = m.multiplicative_heterozygote(W_AA, W_aa)
        assert abs(W_Aa - wAa_mult) > 0.025
