"""cat-stat-bayes-theorem — Normalization Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_bayes_theorem_constants import *
IMPL = Path(__file__).parent.parent / "stat_bayes_theorem.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_posterior_not_equal_unnormalized(self):
        """Posterior P(D|+) must NOT equal the unnormalized numerator."""
        m = _i()
        full = m.bayes_full(P_DISEASE, SENSITIVITY, FPR)
        unnorm = m.prior_times_likelihood(P_DISEASE, SENSITIVITY)
        # They must differ substantially — the denominator matters
        assert abs(full - unnorm) > 0.05
        # Unnormalized is just 0.0095; posterior is ≈0.0876
        assert abs(unnorm - UNNORMALIZED) < 1e-12
        assert abs(full - POSTERIOR) < 1e-8

    def test_base_rate_matters(self):
        """Posterior P(D|+) must be much less than sensitivity P(+|D).

        Base-rate neglect would give P(D|+) ≈ 0.95 — wildly wrong.
        """
        m = _i()
        full = m.bayes_full(P_DISEASE, SENSITIVITY, FPR)
        # Correct posterior ≈ 0.0876, far below sensitivity 0.95
        assert full < SENSITIVITY * 0.5
        assert full < 0.15


class TestCorrectness:
    def test_total_probability(self):
        """P(+) = P(+|D)·P(D) + P(+|¬D)·P(¬D) must equal frozen P_POS."""
        m = _i()
        p_b = m.total_probability(SENSITIVITY, P_DISEASE, FPR)
        assert abs(p_b - P_POS) < 1e-12

    def test_full_posterior_matches_frozen(self):
        """Full posterior must match the frozen constant to high precision."""
        m = _i()
        result = m.bayes_full(P_DISEASE, SENSITIVITY, FPR)
        assert abs(result - POSTERIOR) < 1e-10

    def test_posterior_is_valid_probability(self):
        """Posterior must be in [0, 1]."""
        m = _i()
        result = m.bayes_full(P_DISEASE, SENSITIVITY, FPR)
        assert 0.0 <= result <= 1.0

    def test_complement_error_caught(self):
        """Using 1-sensitivity as FPR (complement error) gives wrong P(+)."""
        m = _i()
        # Correct: FPR = 1 - specificity = 0.10
        # Wrong:   FPR = 1 - sensitivity = 0.05
        wrong_fpr = 1 - SENSITIVITY  # 0.05
        wrong_p_pos = m.total_probability(SENSITIVITY, P_DISEASE, wrong_fpr)
        correct_p_pos = m.total_probability(SENSITIVITY, P_DISEASE, FPR)
        assert abs(wrong_p_pos - correct_p_pos) > 0.01
