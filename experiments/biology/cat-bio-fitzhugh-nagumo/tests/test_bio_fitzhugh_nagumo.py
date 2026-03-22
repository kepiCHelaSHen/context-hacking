"""cat-bio-fitzhugh-nagumo — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_fitzhugh_nagumo_constants import *
IMPL = Path(__file__).parent.parent / "bio_fitzhugh_nagumo.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_v_nullcline_is_cubic_not_linear(self):
        """v-nullcline must be cubic: w = v - v^3/3, NOT a linear function."""
        m = _i()
        # Evaluate at 5 points — a linear function would have constant first differences
        vs = [-2.0, -1.0, 0.0, 1.0, 2.0]
        ws = [m.v_nullcline(v) for v in vs]
        # First differences
        d1 = [ws[i + 1] - ws[i] for i in range(len(ws) - 1)]
        # Second differences — must be nonzero for a cubic
        d2 = [d1[i + 1] - d1[i] for i in range(len(d1) - 1)]
        assert any(abs(d) > 0.1 for d in d2), \
            f"v-nullcline looks linear (second differences ~0): d2={d2}"

    def test_v_nullcline_cubic_values(self):
        """v-nullcline at specific points must match w = v - v^3/3."""
        m = _i()
        for v, expected_w in V_NULL_POINTS.items():
            w = m.v_nullcline(v)
            assert math.isclose(w, expected_w, abs_tol=1e-9), \
                f"v_nullcline({v}) = {w}, expected {expected_w}"

    def test_v_nullcline_sign_of_cubic_term(self):
        """v^3/3 must be subtracted, not added: v_nullcline(2) < 0."""
        m = _i()
        # w = 2 - 8/3 = -0.6667 < 0. Wrong sign would give 2 + 8/3 = 4.6667 > 0
        w_at_2 = m.v_nullcline(2.0)
        assert w_at_2 < 0, \
            f"v_nullcline(2.0) = {w_at_2}, should be negative (v - v^3/3 = -0.667)"

    def test_epsilon_appears_in_dw_dt(self):
        """dw/dt must include epsilon — timescale separation is essential."""
        m = _i()
        # With eps=0.08: dw/dt = 0.08*(1.0 + 0.7 - 0.8*0) = 0.08*1.7 = 0.136
        # Without eps: dw/dt = 1.7
        dw = m.dw_dt(1.0, 0.0, a=0.7, b=0.8, eps=0.08)
        assert math.isclose(dw, 0.08 * 1.7, rel_tol=1e-9), \
            f"dw_dt(1,0) = {dw}, expected {0.08*1.7} — epsilon may be missing"
        # Sanity: value must be much less than 1.7 (proving eps is included)
        assert dw < 0.5, \
            f"dw_dt(1,0) = {dw} is too large — epsilon factor likely missing"


class TestCorrectness:
    def test_nullcline_intersection_is_fixed_point(self):
        """At the fixed point, both dv/dt and dw/dt must be ~0."""
        m = _i()
        dv = m.dv_dt(V_FP, W_FP, I_EXT)
        dw = m.dw_dt(V_FP, W_FP, A, B, EPS)
        assert abs(dv) < 1e-3, f"dv/dt at fixed point = {dv}, expected ~0"
        assert abs(dw) < 1e-3, f"dw/dt at fixed point = {dw}, expected ~0"

    def test_dv_dt_formula(self):
        """dv/dt = v - v^3/3 - w + I_ext at known values."""
        m = _i()
        # v=0, w=0, I=0: dv/dt = 0
        assert math.isclose(m.dv_dt(0, 0, 0), 0.0, abs_tol=1e-12)
        # v=1, w=0, I=0: dv/dt = 1 - 1/3 - 0 = 2/3
        assert math.isclose(m.dv_dt(1, 0, 0), 2.0 / 3.0, rel_tol=1e-9)
        # v=1, w=0.5, I=0.3: dv/dt = 1 - 1/3 - 0.5 + 0.3 = 0.4667
        expected = 1.0 - 1.0 / 3.0 - 0.5 + 0.3
        assert math.isclose(m.dv_dt(1, 0.5, 0.3), expected, rel_tol=1e-9)

    def test_dw_dt_formula(self):
        """dw/dt = eps*(v + a - b*w) at known values."""
        m = _i()
        # v=0, w=0: dw/dt = 0.08*(0 + 0.7 - 0) = 0.056
        assert math.isclose(m.dw_dt(0, 0), 0.08 * 0.7, rel_tol=1e-9)
        # v=-0.7, w=0: dw/dt = 0.08*(-0.7 + 0.7 - 0) = 0
        assert math.isclose(m.dw_dt(-0.7, 0), 0.0, abs_tol=1e-12)

    def test_v_nullcline_at_origin(self):
        """v_nullcline(0) = 0 when I_ext=0."""
        m = _i()
        assert math.isclose(m.v_nullcline(0, 0), 0.0, abs_tol=1e-12)

    def test_w_nullcline_is_linear(self):
        """w-nullcline must be linear: w = (v+a)/b."""
        m = _i()
        vs = [-2.0, -1.0, 0.0, 1.0, 2.0]
        ws = [m.w_nullcline(v) for v in vs]
        # First differences must be constant for a linear function
        d1 = [ws[i + 1] - ws[i] for i in range(len(ws) - 1)]
        for i in range(len(d1) - 1):
            assert math.isclose(d1[i], d1[i + 1], rel_tol=1e-9), \
                f"w-nullcline is not linear: diffs={d1}"
        # Slope must be 1/b = 1.25
        assert math.isclose(d1[0], 1.0 / B, rel_tol=1e-9), \
            f"w-nullcline slope = {d1[0]}, expected {1.0/B}"

    def test_fixed_point_on_both_nullclines(self):
        """Fixed point must lie on both nullclines simultaneously."""
        m = _i()
        w_from_v = m.v_nullcline(V_FP, I_EXT)
        w_from_w = m.w_nullcline(V_FP, A, B)
        assert math.isclose(w_from_v, W_FP, abs_tol=1e-3), \
            f"FP not on v-nullcline: v_null({V_FP})={w_from_v}, w={W_FP}"
        assert math.isclose(w_from_w, W_FP, abs_tol=1e-3), \
            f"FP not on w-nullcline: w_null({V_FP})={w_from_w}, w={W_FP}"
