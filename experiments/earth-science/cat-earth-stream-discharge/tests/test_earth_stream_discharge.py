"""cat-earth-stream-discharge — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_stream_discharge_constants import *
IMPL = Path(__file__).parent.parent / "earth_stream_discharge.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the three known LLM errors."""

    def test_R_not_equal_depth(self):
        """PRIOR_ERROR: r_equals_depth — R = A/P, NOT depth."""
        m = _i()
        A = B_CHANNEL * D_CHANNEL
        P = m.wetted_perimeter_rect(B_CHANNEL, D_CHANNEL)
        R = m.hydraulic_radius(A, P)
        # R must NOT equal depth (2.0); correct R = 10/9 ≈ 1.1111
        assert abs(R - D_CHANNEL) > 0.5, f"R={R} equals depth — wrong!"
        assert abs(R - R_HYDRAULIC) < 1e-10

    def test_wetted_perimeter_includes_sides(self):
        """PRIOR_ERROR: wetted_perimeter_no_sides — P = b + 2d, not just b."""
        m = _i()
        P = m.wetted_perimeter_rect(B_CHANNEL, D_CHANNEL)
        # P must be 9.0 (5 + 2*2), NOT 5.0
        assert P != B_CHANNEL, f"P={P} equals bottom width only — missing sides!"
        assert abs(P - P_WETTED) < 1e-10

    def test_wetted_perimeter_both_sides(self):
        """Wetted perimeter must include BOTH sides, not just one."""
        m = _i()
        P = m.wetted_perimeter_rect(B_CHANNEL, D_CHANNEL)
        # One side missing: P = b + d = 7, both: P = b + 2d = 9
        assert abs(P - (B_CHANNEL + D_CHANNEL)) > 0.5, "Only one side counted"
        assert abs(P - (B_CHANNEL + 2 * D_CHANNEL)) < 1e-10


class TestCorrectness:
    """Verify computed values against frozen constants."""

    def test_cross_section_area(self):
        m = _i()
        A = B_CHANNEL * D_CHANNEL
        assert abs(A - A_CHANNEL) < 1e-10

    def test_wetted_perimeter_value(self):
        m = _i()
        P = m.wetted_perimeter_rect(B_CHANNEL, D_CHANNEL)
        assert abs(P - 9.0) < 1e-10

    def test_hydraulic_radius_value(self):
        m = _i()
        R = m.hydraulic_radius(A_CHANNEL, P_WETTED)
        assert abs(R - 10.0/9.0) < 1e-10

    def test_manning_velocity(self):
        m = _i()
        v = m.manning_velocity(N_MANNING, R_HYDRAULIC, S_SLOPE)
        assert abs(v - V_CORRECT) < 1e-4, f"v={v}, expected {V_CORRECT}"

    def test_discharge(self):
        m = _i()
        Q = m.discharge(V_CORRECT, A_CHANNEL)
        assert abs(Q - Q_CORRECT) < 1e-3, f"Q={Q}, expected {Q_CORRECT}"

    def test_full_pipeline(self):
        """End-to-end: channel params -> Q."""
        m = _i()
        A = B_CHANNEL * D_CHANNEL
        P = m.wetted_perimeter_rect(B_CHANNEL, D_CHANNEL)
        R = m.hydraulic_radius(A, P)
        v = m.manning_velocity(N_MANNING, R, S_SLOPE)
        Q = m.discharge(v, A)
        assert abs(Q - Q_CORRECT) < 1e-3

    def test_wrong_R_gives_wrong_Q(self):
        """Sanity: using depth as R gives ~48% overestimate."""
        m = _i()
        v_wrong = m.manning_velocity(N_MANNING, D_CHANNEL, S_SLOPE)
        Q_wrong = m.discharge(v_wrong, A_CHANNEL)
        error_pct = (Q_wrong - Q_CORRECT) / Q_CORRECT * 100
        assert error_pct > 40, f"Wrong R should overestimate by ~48%, got {error_pct:.1f}%"

    def test_wider_channel_higher_R(self):
        """As channel widens, R -> d (sides become negligible)."""
        m = _i()
        P_narrow = m.wetted_perimeter_rect(2.0, 2.0)   # 2 + 4 = 6
        R_narrow = m.hydraulic_radius(4.0, P_narrow)     # 4/6 = 0.667
        P_wide = m.wetted_perimeter_rect(100.0, 2.0)    # 100 + 4 = 104
        R_wide = m.hydraulic_radius(200.0, P_wide)       # 200/104 = 1.923 ≈ d
        assert R_wide > R_narrow

    def test_square_channel_symmetry(self):
        """Square channel: b=d → R = d/3 * b/(b+2d) = b^2/(3b) ... no, R = b*d/(b+2d)."""
        m = _i()
        s = 3.0  # square channel 3x3
        P = m.wetted_perimeter_rect(s, s)
        R = m.hydraulic_radius(s * s, P)
        assert abs(P - 3 * s) < 1e-10   # P = b + 2d = 3s for square
        assert abs(R - s / 3) < 1e-10   # R = s^2/(3s) = s/3
