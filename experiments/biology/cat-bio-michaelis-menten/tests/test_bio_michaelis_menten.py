"""cat-bio-michaelis-menten — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_michaelis_menten_constants import *
IMPL = Path(__file__).parent.parent / "bio_michaelis_menten.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_v_at_km_is_half_vmax_not_vmax(self):
        """The #1 LLM error: thinks [S]=Km gives v=Vmax (should be Vmax/2)."""
        m = _i()
        v = m.michaelis_menten(VMAX, KM, KM)
        assert math.isclose(v, VMAX / 2, rel_tol=1e-9), (
            f"v at [S]=Km should be Vmax/2={VMAX/2}, got {v}"
        )
        assert not math.isclose(v, VMAX, rel_tol=1e-3), (
            f"v at [S]=Km must NOT equal Vmax={VMAX} — Km is the HALF-max concentration!"
        )

    def test_at_km_returns_half_vmax(self):
        """at_km() must return Vmax/2, not Vmax."""
        m = _i()
        result = m.at_km(VMAX)
        assert math.isclose(result, VMAX / 2, rel_tol=1e-9), (
            f"at_km({VMAX}) should be {VMAX/2}, got {result}"
        )

    def test_v_never_reaches_vmax(self):
        """v approaches Vmax asymptotically — even at very high [S], v < Vmax."""
        m = _i()
        # At [S] = 1,000,000 * Km, v should still be < Vmax
        v_huge = m.michaelis_menten(VMAX, KM, 1_000_000 * KM)
        assert v_huge < VMAX, (
            f"v should never reach Vmax at finite [S]; got v={v_huge}, Vmax={VMAX}"
        )
        # But it should be very close
        assert v_huge > VMAX * 0.999, f"v at huge [S] should be nearly Vmax, got {v_huge}"

    def test_lineweaver_burk_x_intercept_is_negative(self):
        """x-intercept of Lineweaver-Burk is -1/Km (negative), not 1/Km."""
        assert LB_X_INTERCEPT < 0, (
            f"LB x-intercept must be negative (-1/Km), got {LB_X_INTERCEPT}"
        )
        assert math.isclose(LB_X_INTERCEPT, -1.0 / KM, rel_tol=1e-9)


class TestCorrectness:
    def test_v_at_km(self):
        m = _i()
        v = m.michaelis_menten(VMAX, KM, KM)
        assert math.isclose(v, V_AT_KM, rel_tol=1e-9)

    def test_v_at_s_10(self):
        m = _i()
        v = m.michaelis_menten(VMAX, KM, 10)
        assert math.isclose(v, V_AT_10, rel_tol=1e-9), f"v(10)={v}, expected {V_AT_10}"

    def test_v_at_s_50(self):
        m = _i()
        v = m.michaelis_menten(VMAX, KM, 50)
        assert math.isclose(v, V_AT_50, rel_tol=1e-9), f"v(50)={v}, expected {V_AT_50}"

    def test_v_at_s_100(self):
        m = _i()
        v = m.michaelis_menten(VMAX, KM, 100)
        assert math.isclose(v, V_AT_100, rel_tol=1e-9), f"v(100)={v}, expected {V_AT_100}"

    def test_lineweaver_burk_values(self):
        """1/v via lineweaver_burk matches direct computation."""
        m = _i()
        for s in [1, 5, 10, 50, 100]:
            lb = m.lineweaver_burk(VMAX, KM, s)
            v = m.michaelis_menten(VMAX, KM, s)
            assert math.isclose(lb, 1.0 / v, rel_tol=1e-9), (
                f"LB({s})={lb}, expected {1.0/v}"
            )

    def test_km_from_lineweaver_back_calculation(self):
        """Back-calculate Km from LB slope and y-intercept."""
        m = _i()
        km_back = m.km_from_lineweaver(LB_SLOPE, LB_Y_INTERCEPT)
        assert math.isclose(km_back, KM, rel_tol=1e-9), (
            f"Km back-calculated={km_back}, expected {KM}"
        )

    def test_v_increases_monotonically(self):
        """v must increase as [S] increases (enzyme not yet saturated)."""
        m = _i()
        prev_v = 0
        for s in [0.1, 1, 5, 10, 50, 100, 1000]:
            v = m.michaelis_menten(VMAX, KM, s)
            assert v > prev_v, f"v({s})={v} should be > v_prev={prev_v}"
            prev_v = v

    def test_v_at_zero_substrate(self):
        """At [S]=0, v=0."""
        m = _i()
        v = m.michaelis_menten(VMAX, KM, 0)
        assert math.isclose(v, 0.0, abs_tol=1e-15), f"v(0) should be 0, got {v}"
