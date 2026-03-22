"""cat-astro-parallax — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_parallax_constants import *
IMPL = Path(__file__).parent.parent / "astro_parallax.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


# ── Prior-Error Tests (the mistakes LLMs make) ──────────────────────────

class TestPriorErrors:
    def test_parsec_not_light_year(self):
        """parsec_wrong_definition: 1 pc != 1 ly; must be ~3.262 ly."""
        m = _i()
        d_pc = m.parallax_distance_pc(1.0)  # p=1" → d=1 pc
        d_ly = m.pc_to_ly(d_pc)
        # If someone thinks 1 pc = 1 ly, d_ly would equal d_pc
        assert abs(d_ly - PC_IN_LY) < 0.01, (
            f"1 pc should be {PC_IN_LY} ly, got {d_ly}"
        )
        assert abs(d_ly - 1.0) > 2.0, "1 pc != 1 ly"

    def test_parsec_not_au(self):
        """parsec_wrong_definition: 1 pc != 1 AU; 1 pc = 206265 AU."""
        # Just verify the frozen constant is used correctly
        assert abs(PC_IN_AU - 206265) < 1

    def test_semi_angle_not_full_angle(self):
        """full_angle_not_semi: d=1/p uses the semi-angle, not full shift.
        If someone uses full shift (2p), distance would be halved."""
        m = _i()
        d = m.parallax_distance_pc(P_PROXIMA_ARCSEC)
        # Correct: d = 1/0.7687 = 1.3009 pc
        # Wrong (full angle): d = 1/(2*0.7687) = 0.6505 pc
        assert abs(d - D_PROXIMA_PC) / D_PROXIMA_PC < 1e-6, (
            f"Expected {D_PROXIMA_PC:.4f} pc, got {d:.4f} pc — "
            "likely using full angle instead of semi-angle"
        )

    def test_arcsec_to_rad_correct_factor(self):
        """arcsec_to_rad_wrong: 1 arcsec = 1/206265 rad, NOT 1/3600 rad."""
        m = _i()
        rad = m.arcsec_to_rad(1.0)
        correct = 1.0 / 206265
        wrong_deg = 1.0 / 3600  # this would be degrees, not radians
        assert abs(rad - correct) / correct < 1e-6, (
            f"arcsec_to_rad(1) = {rad}, expected {correct}"
        )
        assert abs(rad - wrong_deg) > 1e-6, (
            "Using 1/3600 (degree conversion) instead of 1/206265"
        )


# ── Correctness Tests ────────────────────────────────────────────────────

class TestCorrectness:
    def test_proxima_centauri_distance_pc(self):
        """Proxima Cen: p=0.7687\" → d=1.3009 pc."""
        m = _i()
        d = m.parallax_distance_pc(P_PROXIMA_ARCSEC)
        assert abs(d - D_PROXIMA_PC) / D_PROXIMA_PC < 1e-6

    def test_proxima_centauri_distance_ly(self):
        """Proxima Cen: d = 4.244 ly."""
        m = _i()
        d = m.parallax_distance_pc(P_PROXIMA_ARCSEC)
        d_ly = m.pc_to_ly(d)
        assert abs(d_ly - D_PROXIMA_LY) / D_PROXIMA_LY < 1e-4

    def test_case_p01(self):
        """Test case: p=0.1\" → d=10 pc = 32.62 ly."""
        m = _i()
        d = m.parallax_distance_pc(P_TEST_ARCSEC)
        assert abs(d - D_TEST_PC) < 1e-10
        assert abs(m.pc_to_ly(d) - D_TEST_LY) / D_TEST_LY < 1e-4

    def test_case_p01_metres(self):
        """Test case: p=0.1\" → d = 3.086e17 m."""
        m = _i()
        d = m.parallax_distance_pc(P_TEST_ARCSEC)
        d_m = m.pc_to_m(d)
        assert abs(d_m - D_TEST_M) / D_TEST_M < 1e-6

    def test_barnard_star(self):
        """Barnard's Star: p=0.5469\" → d=1.8285 pc."""
        m = _i()
        d = m.parallax_distance_pc(P_BARNARD_ARCSEC)
        assert abs(d - D_BARNARD_PC) / D_BARNARD_PC < 1e-4

    def test_sirius(self):
        """Sirius: p=0.3792\" → d=2.637 pc."""
        m = _i()
        d = m.parallax_distance_pc(P_SIRIUS_ARCSEC)
        assert abs(d - D_SIRIUS_PC) / D_SIRIUS_PC < 1e-4

    def test_gaia_limit(self):
        """Gaia limit: p=0.001\" → d=1000 pc."""
        m = _i()
        d = m.parallax_distance_pc(P_GAIA_LIMIT_ARCSEC)
        assert abs(d - D_GAIA_LIMIT_PC) < 1e-6

    def test_pc_to_m_conversion(self):
        """1 pc = 3.08567758e16 m."""
        m = _i()
        assert abs(m.pc_to_m(1.0) - PC_IN_METERS) < 1e8  # within 100 m

    def test_arcsec_to_rad_roundtrip(self):
        """206265 arcsec = 1 radian."""
        m = _i()
        rad = m.arcsec_to_rad(206265.0)
        assert abs(rad - 1.0) < 1e-6

    def test_negative_parallax_raises(self):
        """Negative parallax must raise ValueError."""
        m = _i()
        with pytest.raises(ValueError):
            m.parallax_distance_pc(-0.1)

    def test_zero_parallax_raises(self):
        """Zero parallax must raise ValueError (infinite distance)."""
        m = _i()
        with pytest.raises(ValueError):
            m.parallax_distance_pc(0.0)
