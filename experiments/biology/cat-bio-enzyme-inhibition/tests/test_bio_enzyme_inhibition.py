"""cat-bio-enzyme-inhibition — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_enzyme_inhibition_constants import *
IMPL = Path(__file__).parent.parent / "bio_enzyme_inhibition.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Tests that directly target known LLM errors about enzyme inhibition."""

    def test_competitive_km_increases_but_vmax_unchanged(self):
        """Prior error 'competitive_changes_vmax': competitive changes Km, NOT Vmax."""
        m = _i()
        km_app = m.apparent_km_competitive(KM, I, KI)
        assert km_app > KM, (
            f"Competitive Km_app={km_app} must be > Km={KM}"
        )
        assert math.isclose(km_app, COMPETITIVE_KM_APP, rel_tol=1e-9), (
            f"Competitive Km_app={km_app}, expected {COMPETITIVE_KM_APP}"
        )
        # Vmax must be unchanged under competitive inhibition
        # At very high [S], competitive inhibition is overcome: v -> Vmax
        v_high = m.competitive(VMAX, KM, 1_000_000, I, KI)
        assert math.isclose(v_high, VMAX, rel_tol=1e-3), (
            f"At very high [S], competitive v should approach Vmax={VMAX}, got {v_high}"
        )

    def test_uncompetitive_km_decreases_not_increases(self):
        """Prior error 'uncompetitive_increases_km': apparent Km DECREASES under uncompetitive."""
        m = _i()
        km_app = m.apparent_km_uncompetitive(KM, I, KI)
        assert km_app < KM, (
            f"Uncompetitive Km_app={km_app} must be LESS than Km={KM} — it decreases!"
        )
        assert math.isclose(km_app, UNCOMPETITIVE_KM_APP, rel_tol=1e-9), (
            f"Uncompetitive Km_app={km_app}, expected {UNCOMPETITIVE_KM_APP}"
        )

    def test_uncompetitive_vmax_also_decreases(self):
        """Uncompetitive inhibition decreases BOTH apparent Km and apparent Vmax."""
        m = _i()
        vmax_app = m.apparent_vmax_uncompetitive(VMAX, I, KI)
        assert vmax_app < VMAX, (
            f"Uncompetitive Vmax_app={vmax_app} must be < Vmax={VMAX}"
        )
        assert math.isclose(vmax_app, UNCOMPETITIVE_VMAX_APP, rel_tol=1e-9), (
            f"Uncompetitive Vmax_app={vmax_app}, expected {UNCOMPETITIVE_VMAX_APP}"
        )

    def test_lb_competitive_yintercept_unchanged(self):
        """Prior error 'lb_intercepts_swapped': competitive keeps y-intercept constant."""
        # Competitive L-B: y-intercept = 1/Vmax (same as uninhibited)
        assert math.isclose(LB_COMPETITIVE_YINT, LB_UNINHIBITED_YINT, rel_tol=1e-9), (
            f"Competitive L-B y-int should equal uninhibited y-int, "
            f"got {LB_COMPETITIVE_YINT} vs {LB_UNINHIBITED_YINT}"
        )
        # But slope changes
        assert not math.isclose(LB_COMPETITIVE_SLOPE, LB_UNINHIBITED_SLOPE, rel_tol=1e-3), (
            "Competitive L-B slope must differ from uninhibited"
        )

    def test_lb_uncompetitive_slope_unchanged(self):
        """Prior error 'lb_intercepts_swapped': uncompetitive keeps slope constant."""
        # Uncompetitive L-B: slope = Km/Vmax (same as uninhibited)
        assert math.isclose(LB_UNCOMPETITIVE_SLOPE, LB_UNINHIBITED_SLOPE, rel_tol=1e-9), (
            f"Uncompetitive L-B slope should equal uninhibited slope, "
            f"got {LB_UNCOMPETITIVE_SLOPE} vs {LB_UNINHIBITED_SLOPE}"
        )
        # But y-intercept changes
        assert not math.isclose(LB_UNCOMPETITIVE_YINT, LB_UNINHIBITED_YINT, rel_tol=1e-3), (
            "Uncompetitive L-B y-intercept must differ from uninhibited"
        )

    def test_lb_noncompetitive_xintercept_unchanged(self):
        """Noncompetitive L-B: x-intercept stays at -1/Km (slope and y-int both change)."""
        assert math.isclose(LB_NONCOMPETITIVE_XINT, LB_UNINHIBITED_XINT, rel_tol=1e-9), (
            f"Noncompetitive L-B x-int should equal uninhibited x-int, "
            f"got {LB_NONCOMPETITIVE_XINT} vs {LB_UNINHIBITED_XINT}"
        )


class TestCorrectness:
    """Verify computed velocities and apparent parameters against frozen constants."""

    def test_competitive_v_at_s5(self):
        m = _i()
        v = m.competitive(VMAX, KM, 5.0, I, KI)
        assert math.isclose(v, V_COMPETITIVE_AT_5, rel_tol=1e-9), (
            f"competitive(S=5)={v}, expected {V_COMPETITIVE_AT_5}"
        )

    def test_competitive_v_at_s10(self):
        m = _i()
        v = m.competitive(VMAX, KM, 10.0, I, KI)
        assert math.isclose(v, V_COMPETITIVE_AT_10, rel_tol=1e-9), (
            f"competitive(S=10)={v}, expected {V_COMPETITIVE_AT_10}"
        )

    def test_competitive_v_at_s20(self):
        m = _i()
        v = m.competitive(VMAX, KM, 20.0, I, KI)
        assert math.isclose(v, V_COMPETITIVE_AT_20, rel_tol=1e-9), (
            f"competitive(S=20)={v}, expected {V_COMPETITIVE_AT_20}"
        )

    def test_uncompetitive_v_at_s5(self):
        m = _i()
        v = m.uncompetitive(VMAX, KM, 5.0, I, KI)
        assert math.isclose(v, V_UNCOMPETITIVE_AT_5, rel_tol=1e-9), (
            f"uncompetitive(S=5)={v}, expected {V_UNCOMPETITIVE_AT_5}"
        )

    def test_uncompetitive_v_at_s10(self):
        m = _i()
        v = m.uncompetitive(VMAX, KM, 10.0, I, KI)
        assert math.isclose(v, V_UNCOMPETITIVE_AT_10, rel_tol=1e-9), (
            f"uncompetitive(S=10)={v}, expected {V_UNCOMPETITIVE_AT_10}"
        )

    def test_uncompetitive_v_at_s20(self):
        m = _i()
        v = m.uncompetitive(VMAX, KM, 20.0, I, KI)
        assert math.isclose(v, V_UNCOMPETITIVE_AT_20, rel_tol=1e-9), (
            f"uncompetitive(S=20)={v}, expected {V_UNCOMPETITIVE_AT_20}"
        )

    def test_noncompetitive_v_at_s5(self):
        m = _i()
        v = m.noncompetitive(VMAX, KM, 5.0, I, KI)
        assert math.isclose(v, V_NONCOMPETITIVE_AT_5, rel_tol=1e-9), (
            f"noncompetitive(S=5)={v}, expected {V_NONCOMPETITIVE_AT_5}"
        )

    def test_noncompetitive_v_at_s10(self):
        m = _i()
        v = m.noncompetitive(VMAX, KM, 10.0, I, KI)
        assert math.isclose(v, V_NONCOMPETITIVE_AT_10, rel_tol=1e-9), (
            f"noncompetitive(S=10)={v}, expected {V_NONCOMPETITIVE_AT_10}"
        )

    def test_noncompetitive_v_at_s20(self):
        m = _i()
        v = m.noncompetitive(VMAX, KM, 20.0, I, KI)
        assert math.isclose(v, V_NONCOMPETITIVE_AT_20, rel_tol=1e-9), (
            f"noncompetitive(S=20)={v}, expected {V_NONCOMPETITIVE_AT_20}"
        )

    def test_apparent_km_competitive_value(self):
        m = _i()
        result = m.apparent_km_competitive(KM, I, KI)
        assert math.isclose(result, COMPETITIVE_KM_APP, rel_tol=1e-9)

    def test_apparent_km_uncompetitive_value(self):
        m = _i()
        result = m.apparent_km_uncompetitive(KM, I, KI)
        assert math.isclose(result, UNCOMPETITIVE_KM_APP, rel_tol=1e-9)

    def test_apparent_vmax_uncompetitive_value(self):
        m = _i()
        result = m.apparent_vmax_uncompetitive(VMAX, I, KI)
        assert math.isclose(result, UNCOMPETITIVE_VMAX_APP, rel_tol=1e-9)

    def test_competitive_and_uncompetitive_equal_at_s5(self):
        """At [S]=5, competitive and uncompetitive both give 100/3."""
        m = _i()
        v_c = m.competitive(VMAX, KM, 5.0, I, KI)
        v_u = m.uncompetitive(VMAX, KM, 5.0, I, KI)
        assert math.isclose(v_c, v_u, rel_tol=1e-9), (
            f"At [S]=5 with these params, competitive ({v_c}) and "
            f"uncompetitive ({v_u}) should both equal 100/3"
        )

    def test_all_inhibited_less_than_uninhibited(self):
        """All inhibition types reduce velocity below uninhibited rate."""
        m = _i()
        for s in [1, 5, 10, 20, 50]:
            v_uninhib = VMAX * s / (KM + s)
            v_c = m.competitive(VMAX, KM, s, I, KI)
            v_uc = m.uncompetitive(VMAX, KM, s, I, KI)
            v_nc = m.noncompetitive(VMAX, KM, s, I, KI)
            assert v_c < v_uninhib, f"competitive v at S={s} must be < uninhibited"
            assert v_uc < v_uninhib, f"uncompetitive v at S={s} must be < uninhibited"
            assert v_nc < v_uninhib, f"noncompetitive v at S={s} must be < uninhibited"

    def test_v_at_zero_substrate(self):
        """All types give v=0 when [S]=0."""
        m = _i()
        assert math.isclose(m.competitive(VMAX, KM, 0, I, KI), 0.0, abs_tol=1e-15)
        assert math.isclose(m.uncompetitive(VMAX, KM, 0, I, KI), 0.0, abs_tol=1e-15)
        assert math.isclose(m.noncompetitive(VMAX, KM, 0, I, KI), 0.0, abs_tol=1e-15)
