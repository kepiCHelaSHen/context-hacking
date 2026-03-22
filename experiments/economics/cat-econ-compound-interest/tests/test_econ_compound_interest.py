"""cat-econ-compound-interest — Sigma Gate Tests"""
import math
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_compound_interest_constants import *

IMPL = Path(__file__).parent.parent / "econ_compound_interest.py"


def _i():
    if not IMPL.exists():
        pytest.skip("not yet written")
    import importlib.util
    s = importlib.util.spec_from_file_location("m", IMPL)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


# ── Prior-Error Guards ──────────────────────────────────────────────
class TestPriorErrors:
    """Guard against known LLM mistakes."""

    def test_ear_not_equal_to_apr(self):
        """EAR must NOT equal APR when m > 1 (catches apr_equals_ear)."""
        m = _i()
        ear = m.ear_from_apr(APR, M)
        assert abs(ear - APR) > 0.001, \
            f"EAR={ear} equals APR={APR} — must differ when m>1"

    def test_rule72_is_approximate(self):
        """Rule of 72 must NOT equal exact doubling time (catches rule72_exact)."""
        m = _i()
        approx = m.rule_of_72(RATE_PCT)
        exact = m.exact_doubling_time(APR)
        assert abs(approx - exact) > 0.01, \
            "Rule of 72 returned exact doubling time — it should be an approximation"

    def test_discrete_not_continuous(self):
        """Discrete EAR must NOT equal continuous EAR (catches continuous_wrong)."""
        m = _i()
        ear_disc = m.ear_from_apr(APR, M)
        ear_cont = m.ear_continuous(APR)
        assert abs(ear_disc - ear_cont) > 0.0001, \
            "Discrete EAR equals continuous EAR — wrong formula used"


# ── Correctness Tests ──────────────────────────────────────────────
class TestCorrectness:

    def test_ear_from_apr_value(self):
        m = _i()
        ear = m.ear_from_apr(APR, M)
        assert abs(ear - EAR_EXPECTED) < 1e-10, \
            f"EAR={ear}, expected {EAR_EXPECTED}"

    def test_ear_continuous_value(self):
        m = _i()
        ear = m.ear_continuous(APR)
        assert abs(ear - EAR_CONTINUOUS_EXPECTED) < 1e-10, \
            f"EAR_cont={ear}, expected {EAR_CONTINUOUS_EXPECTED}"

    def test_ear_greater_than_apr(self):
        """EAR > APR when m > 1 — fundamental property."""
        m = _i()
        ear = m.ear_from_apr(APR, M)
        assert ear > APR, f"EAR={ear} should be > APR={APR}"

    def test_continuous_greater_than_discrete(self):
        """Continuous EAR > discrete EAR for same APR."""
        m = _i()
        ear_disc = m.ear_from_apr(APR, M)
        ear_cont = m.ear_continuous(APR)
        assert ear_cont > ear_disc, \
            f"Continuous EAR={ear_cont} should be > discrete EAR={ear_disc}"

    def test_compound_amount_value(self):
        m = _i()
        fv = m.compound_amount(P_PRINCIPAL, APR, M, T_YEARS)
        assert abs(fv - COMPOUND_AMOUNT_EXPECTED) < 1e-6, \
            f"FV={fv}, expected {COMPOUND_AMOUNT_EXPECTED}"

    def test_compound_amount_one_year(self):
        """After 1 year, FV/P - 1 should equal EAR."""
        m = _i()
        fv = m.compound_amount(1.0, APR, M, 1)
        ear = m.ear_from_apr(APR, M)
        assert abs((fv - 1.0) - ear) < 1e-10, \
            f"FV-1={fv - 1.0} should equal EAR={ear}"

    def test_rule_of_72_value(self):
        m = _i()
        r72 = m.rule_of_72(RATE_PCT)
        assert abs(r72 - RULE_72_APPROX) < 1e-10, \
            f"Rule72={r72}, expected {RULE_72_APPROX}"

    def test_exact_doubling_time_value(self):
        m = _i()
        dt = m.exact_doubling_time(APR)
        assert abs(dt - EXACT_DOUBLING_TIME) < 1e-10, \
            f"ExactDT={dt}, expected {EXACT_DOUBLING_TIME}"

    def test_exact_doubling_time_actually_doubles(self):
        """Verify that after exact_doubling_time years, the amount has doubled."""
        m = _i()
        dt = m.exact_doubling_time(APR)
        # Use annual compounding for clean check: (1+r)^dt = 2
        doubled = (1 + APR) ** dt
        assert abs(doubled - 2.0) < 1e-8, \
            f"(1+{APR})^{dt} = {doubled}, expected 2.0"

    def test_ear_m1_equals_apr(self):
        """When m=1, EAR should equal APR (annual compounding, no difference)."""
        m = _i()
        ear = m.ear_from_apr(APR, 1)
        assert abs(ear - APR) < 1e-12, \
            f"EAR with m=1 should equal APR; got {ear}"
