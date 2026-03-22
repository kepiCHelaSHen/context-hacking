"""cat-stat-survival-analysis — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_survival_analysis_constants import *
IMPL = Path(__file__).parent.parent / "stat_survival_analysis.py"


def _i():
    if not IMPL.exists():
        pytest.skip("not yet written")
    import importlib.util
    s = importlib.util.spec_from_file_location("m", IMPL)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


TOL = 1e-5


class TestPriorErrors:
    """Verify the implementation does NOT make the documented prior errors."""

    def test_censored_not_treated_as_event(self):
        """Censored observations must NOT reduce S — S(2) should equal S(1)."""
        m = _i()
        curve = m.kaplan_meier(TIMES, EVENTS)
        s1 = m.survival_at_time(curve, 1)
        s2 = m.survival_at_time(curve, 2)
        # t=2 is censored: survival must not drop
        assert abs(s2 - s1) < TOL, (
            f"S(2)={s2} differs from S(1)={s1} — censored observation wrongly treated as event"
        )

    def test_wrong_censored_value_rejected(self):
        """S(2) must NOT equal the wrong value that treats censored as events."""
        m = _i()
        curve = m.kaplan_meier(TIMES, EVENTS)
        s2 = m.survival_at_time(curve, 2)
        assert abs(s2 - S_WRONG_AT_2) > TOL, (
            f"S(2)={s2} matches the WRONG value {S_WRONG_AT_2} — censored treated as event"
        )

    def test_at_risk_reduced_after_censoring(self):
        """After censoring at t=2, at-risk count must decrease for t=3.
        Correct: n=5 at t=3 → S(3) = S(1)*(4/5).
        Wrong (no reduction): n=6 at t=3 → S(3) = S(1)*(5/6).
        """
        m = _i()
        curve = m.kaplan_meier(TIMES, EVENTS)
        s3 = m.survival_at_time(curve, 3)
        s_wrong_no_reduce = S_AT_1 * (5 / 6)  # if n wasn't reduced after censoring
        assert abs(s3 - s_wrong_no_reduce) > TOL, (
            f"S(3)={s3} matches wrong_at_risk value {s_wrong_no_reduce}"
        )


class TestCorrectness:
    """Verify computed survival matches frozen gold-standard values."""

    def test_S_at_1(self):
        m = _i()
        curve = m.kaplan_meier(TIMES, EVENTS)
        assert abs(m.survival_at_time(curve, 1) - S_AT_1) < TOL

    def test_S_at_3(self):
        m = _i()
        curve = m.kaplan_meier(TIMES, EVENTS)
        assert abs(m.survival_at_time(curve, 3) - S_AT_3) < TOL

    def test_S_at_4(self):
        m = _i()
        curve = m.kaplan_meier(TIMES, EVENTS)
        assert abs(m.survival_at_time(curve, 4) - S_AT_4) < TOL

    def test_S_at_6(self):
        m = _i()
        curve = m.kaplan_meier(TIMES, EVENTS)
        assert abs(m.survival_at_time(curve, 6) - S_AT_6) < TOL

    def test_S_at_8_equals_zero(self):
        m = _i()
        curve = m.kaplan_meier(TIMES, EVENTS)
        assert abs(m.survival_at_time(curve, 8) - S_AT_8) < TOL

    def test_at_risk_helper(self):
        m = _i()
        assert m.at_risk(7, 0) == 7
        assert m.at_risk(6, 1) == 5
