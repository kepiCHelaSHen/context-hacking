"""cat-bio-pharmacokinetics-1c — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_pharmacokinetics_1c_constants import *
IMPL = Path(__file__).parent.parent / "bio_pharmacokinetics_1c.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_half_life_is_ln2_over_ke_not_1_over_ke(self):
        """The #1 LLM error: using 1/ke instead of ln(2)/ke for half-life."""
        m = _i()
        t_half = m.half_life(KE)
        assert math.isclose(t_half, HALF_LIFE, rel_tol=1e-9), \
            f"t½ should be ln(2)/ke={HALF_LIFE:.4f}, got {t_half:.4f}"
        assert not math.isclose(t_half, WRONG_HALF_LIFE, rel_tol=0.01), \
            f"Got 1/ke={WRONG_HALF_LIFE} — must use ln(2)/ke!"

    def test_concentration_at_half_life_is_half_C0(self):
        """At t = t½, concentration must be exactly C₀/2."""
        m = _i()
        c = m.concentration(C0, KE, HALF_LIFE)
        assert math.isclose(c, C_AT_HALF_LIFE, rel_tol=1e-9), \
            f"C(t½) should be {C_AT_HALF_LIFE}, got {c:.4f}"
        assert math.isclose(c, C0 / 2, rel_tol=1e-9), \
            f"C(t½) should be C₀/2={C0/2}, got {c:.4f}"

class TestCorrectness:
    def test_half_life_value(self):
        m = _i()
        t_half = m.half_life(KE)
        assert math.isclose(t_half, 6.931471805599453, rel_tol=1e-9)

    def test_volume_of_distribution(self):
        m = _i()
        vd = m.volume_of_distribution(DOSE, C0)
        assert math.isclose(vd, VD, rel_tol=1e-9), f"Vd should be {VD}, got {vd}"

    def test_clearance(self):
        m = _i()
        cl = m.clearance(KE, VD)
        assert math.isclose(cl, CL, rel_tol=1e-9), f"CL should be {CL}, got {cl}"

    def test_concentration_at_10hr(self):
        m = _i()
        c = m.concentration(C0, KE, 10.0)
        assert math.isclose(c, C_AT_10HR, rel_tol=1e-6), \
            f"C(10) should be {C_AT_10HR:.4f}, got {c:.4f}"
        assert not math.isclose(c, 50.0, rel_tol=0.01), \
            "C(10) must NOT be 50 — that would mean t½=10 (wrong)"

    def test_time_to_fraction(self):
        """time_to_fraction(ke, 0.5) must equal half_life(ke)."""
        m = _i()
        t = m.time_to_fraction(KE, 0.5)
        t_half = m.half_life(KE)
        assert math.isclose(t, t_half, rel_tol=1e-9), \
            f"time_to_fraction(ke, 0.5)={t:.4f} should equal t½={t_half:.4f}"

    def test_time_to_quarter(self):
        """time_to_fraction(ke, 0.25) = 2 * t½."""
        m = _i()
        t = m.time_to_fraction(KE, 0.25)
        t_half = m.half_life(KE)
        assert math.isclose(t, 2 * t_half, rel_tol=1e-9), \
            f"Time to 25% should be 2*t½={2*t_half:.4f}, got {t:.4f}"
