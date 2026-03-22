"""cat-eng-mohr-circle — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_mohr_circle_constants import *
IMPL = Path(__file__).parent.parent / "eng_mohr_circle.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the known LLM failure modes."""

    def test_center_uses_sum_not_difference(self):
        """Center must be (σ_x + σ_y)/2, NOT (σ_x - σ_y)/2."""
        m = _i(); c = m.mohr_center(SX_REF, SY_REF)
        assert abs(c - CENTER_REF) < 0.001
        assert abs(c - CENTER_WRONG) > 10, "Used (σ_x - σ_y)/2 for center — must be (σ_x + σ_y)/2!"

    def test_radius_includes_shear(self):
        """Radius must include τ_xy² term — not just ((σ_x - σ_y)/2)²."""
        m = _i(); r = m.mohr_radius(SX_REF, SY_REF, TXY_REF)
        assert abs(r - RADIUS_REF) < 0.001
        assert abs(r - RADIUS_NO_SHEAR) > 10, "Missing τ_xy² in radius formula!"

    def test_angle_has_half_factor(self):
        """Principal angle must include 1/2 factor."""
        m = _i(); theta = m.principal_angle_deg(SX_REF, SY_REF, TXY_REF)
        assert abs(theta - THETA_P_DEG_REF) < 0.01
        assert abs(theta - THETA_P_NO_HALF) > 10, "Missing 1/2 factor in principal angle!"


class TestCorrectness:
    """Verify numerical accuracy of all functions."""

    def test_center_value(self):
        m = _i(); c = m.mohr_center(SX_REF, SY_REF)
        assert abs(c - 60.0) < 1e-10

    def test_radius_value(self):
        m = _i(); r = m.mohr_radius(SX_REF, SY_REF, TXY_REF)
        assert abs(r - math.sqrt(1300.0)) < 1e-8

    def test_sigma1_value(self):
        m = _i(); s1, _ = m.principal_stresses(SX_REF, SY_REF, TXY_REF)
        assert abs(s1 - SIGMA1_REF) < 1e-8

    def test_sigma2_value(self):
        m = _i(); _, s2 = m.principal_stresses(SX_REF, SY_REF, TXY_REF)
        assert abs(s2 - SIGMA2_REF) < 1e-8

    def test_sigma1_gt_sigma2(self):
        """σ₁ must always be >= σ₂."""
        m = _i(); s1, s2 = m.principal_stresses(SX_REF, SY_REF, TXY_REF)
        assert s1 >= s2

    def test_max_shear_equals_radius(self):
        m = _i(); ts = m.max_shear(SX_REF, SY_REF, TXY_REF)
        assert abs(ts - RADIUS_REF) < 1e-10

    def test_max_shear_equals_half_sigma_diff(self):
        """τ_max = (σ₁ - σ₂) / 2 — consistency check."""
        m = _i()
        s1, s2 = m.principal_stresses(SX_REF, SY_REF, TXY_REF)
        ts = m.max_shear(SX_REF, SY_REF, TXY_REF)
        assert abs(ts - (s1 - s2) / 2.0) < 1e-10

    def test_principal_angle_deg(self):
        m = _i(); theta = m.principal_angle_deg(SX_REF, SY_REF, TXY_REF)
        assert abs(theta - THETA_P_DEG_REF) < 1e-6

    def test_pure_shear_center_zero(self):
        """When σ_x = σ_y = 0, center should be 0."""
        m = _i(); c = m.mohr_center(0.0, 0.0)
        assert abs(c) < 1e-12

    def test_pure_shear_radius_equals_txy(self):
        """When σ_x = σ_y = 0, radius = |τ_xy|."""
        m = _i(); r = m.mohr_radius(0.0, 0.0, 50.0)
        assert abs(r - 50.0) < 1e-10

    def test_no_shear_principals_are_normals(self):
        """When τ_xy = 0, principal stresses are just σ_x and σ_y (sorted)."""
        m = _i(); s1, s2 = m.principal_stresses(100.0, 30.0, 0.0)
        assert abs(s1 - 100.0) < 1e-10
        assert abs(s2 - 30.0) < 1e-10

    def test_hydrostatic_no_shear(self):
        """When σ_x = σ_y and τ_xy = 0, radius = 0, no shear."""
        m = _i()
        r = m.mohr_radius(50.0, 50.0, 0.0)
        assert abs(r) < 1e-12
        s1, s2 = m.principal_stresses(50.0, 50.0, 0.0)
        assert abs(s1 - 50.0) < 1e-10
        assert abs(s2 - 50.0) < 1e-10
