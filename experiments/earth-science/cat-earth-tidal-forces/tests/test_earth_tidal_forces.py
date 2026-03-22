"""cat-earth-tidal-forces — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_tidal_forces_constants import *
IMPL = Path(__file__).parent.parent / "earth_tidal_forces.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_sun_not_ignored(self):
        """LLM trap: Sun's tidal force is ~46% of Moon's — NOT negligible."""
        m = _i(); ratio = m.sun_moon_ratio()
        assert ratio > 0.40, "Sun/Moon ratio must be > 0.40 — Sun is NOT negligible"
        assert ratio < 0.55, "Sun/Moon ratio must be < 0.55"

    def test_uses_d_cubed_not_squared(self):
        """LLM trap: tidal force ∝ M/d³, NOT M/d² (gravity)."""
        m = _i()
        tf_moon_correct = m.tidal_force_ratio(M_MOON, D_MOON)
        tf_moon_wrong = M_MOON / D_MOON**2  # gravity, not tidal
        # The two must differ by orders of magnitude
        assert abs(tf_moon_correct - tf_moon_wrong) / tf_moon_wrong > 1e-6, \
            "Tidal force must use d³, not d²"
        assert abs(tf_moon_correct - TF_MOON) / TF_MOON < 1e-6

    def test_spring_neap_not_confused(self):
        """LLM trap: spring > 1 (aligned), neap < 1 (perpendicular)."""
        m = _i()
        assert m.spring_tide_factor() > 1.0, "Spring tide must amplify (>1)"
        assert m.neap_tide_factor() < 1.0, "Neap tide must reduce (<1)"
        assert m.spring_tide_factor() > m.neap_tide_factor()


class TestCorrectness:
    def test_tidal_force_moon(self):
        m = _i(); tf = m.tidal_force_ratio(M_MOON, D_MOON)
        assert abs(tf - TF_MOON) / TF_MOON < 1e-6

    def test_tidal_force_sun(self):
        m = _i(); tf = m.tidal_force_ratio(M_SUN, D_SUN)
        assert abs(tf - TF_SUN) / TF_SUN < 1e-6

    def test_sun_moon_ratio_value(self):
        m = _i(); ratio = m.sun_moon_ratio()
        assert abs(ratio - SUN_MOON_RATIO) / SUN_MOON_RATIO < 1e-6

    def test_spring_factor_value(self):
        m = _i(); sf = m.spring_tide_factor()
        assert abs(sf - SPRING_FACTOR) / SPRING_FACTOR < 1e-6

    def test_neap_factor_value(self):
        m = _i(); nf = m.neap_tide_factor()
        assert abs(nf - NEAP_FACTOR) / NEAP_FACTOR < 1e-6

    def test_spring_plus_neap_equals_two(self):
        """Spring + Neap = (1+r) + (1-r) = 2 exactly."""
        m = _i()
        assert abs(m.spring_tide_factor() + m.neap_tide_factor() - 2.0) < 1e-10
