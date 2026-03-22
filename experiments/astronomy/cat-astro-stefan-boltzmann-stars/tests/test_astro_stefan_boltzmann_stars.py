"""cat-astro-stefan-boltzmann-stars — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_stefan_boltzmann_stars_constants import *
IMPL = Path(__file__).parent.parent / "astro_stefan_boltzmann_stars.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


# ── Prior-error tests ──────────────────────────────────────────────

class TestPriorErrors:
    def test_wien_constant_correct(self):
        """wien_constant_wrong: wrong b gives wildly wrong peak wavelength."""
        m = _i()
        lam_correct = m.wien_peak(T_SUN, b=WIEN_B)
        lam_wrong   = m.wien_peak(T_SUN, b=WIEN_B_WRONG)  # 2.898e-4 (10x too small)
        assert abs(lam_correct - LAMBDA_SUN) / LAMBDA_SUN < 0.001
        assert abs(lam_wrong - LAMBDA_SUN) / LAMBDA_SUN > 0.5  # off by 10x

    def test_spectral_boundaries_sun_is_G(self):
        """spectral_boundaries_wrong: Sun at 5778 K must be G, not F or K."""
        m = _i()
        assert m.spectral_type(T_SUN) == "G"

    def test_spectral_boundaries_sirius_is_A(self):
        """spectral_boundaries_wrong: Sirius at 9940 K must be A, not B."""
        m = _i()
        assert m.spectral_type(T_SIRIUS) == "A"

    def test_spectral_boundaries_betelgeuse_is_M(self):
        """spectral_boundaries_wrong: Betelgeuse at 3600 K must be M, not K."""
        m = _i()
        assert m.spectral_type(T_BETELGEUSE) == "M"

    def test_peak_is_not_color(self):
        """peak_is_color: Sun peaks at ~502 nm (green) but appears white/yellow.
        Test that peak is in green range, proving peak != perceived color."""
        m = _i()
        nm = m.peak_to_nm(m.wien_peak(T_SUN))
        # Peak falls in green band (495–570 nm), yet Sun appears yellow-white
        assert 495 < nm < 570, f"Sun peak {nm:.1f} nm should be in green band"


# ── Correctness tests ──────────────────────────────────────────────

class TestWienPeak:
    def test_sun_peak(self):
        m = _i()
        lam = m.wien_peak(T_SUN)
        assert abs(lam - LAMBDA_SUN) / LAMBDA_SUN < 1e-6

    def test_sirius_peak(self):
        m = _i()
        lam = m.wien_peak(T_SIRIUS)
        assert abs(lam - LAMBDA_SIRIUS) / LAMBDA_SIRIUS < 1e-6

    def test_betelgeuse_peak(self):
        m = _i()
        lam = m.wien_peak(T_BETELGEUSE)
        assert abs(lam - LAMBDA_BETELGEUSE) / LAMBDA_BETELGEUSE < 1e-6

    def test_sun_peak_nm(self):
        """Sun peak should be ~501.6 nm."""
        m = _i()
        nm = m.peak_to_nm(m.wien_peak(T_SUN))
        assert abs(nm - 501.6) < 0.5

    def test_sirius_peak_nm(self):
        """Sirius peak should be ~291.5 nm (UV)."""
        m = _i()
        nm = m.peak_to_nm(m.wien_peak(T_SIRIUS))
        assert abs(nm - 291.5) < 0.5

    def test_betelgeuse_peak_nm(self):
        """Betelgeuse peak should be ~805.0 nm (near-IR)."""
        m = _i()
        nm = m.peak_to_nm(m.wien_peak(T_BETELGEUSE))
        assert abs(nm - 805.0) < 0.5

    def test_zero_temperature_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.wien_peak(0)

    def test_negative_temperature_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.wien_peak(-100)


class TestSpectralType:
    @pytest.mark.parametrize("T,expected", [
        (50000, "O"), (30001, "O"),
        (30000, "B"), (10001, "B"),
        (10000, "A"), (7501, "A"),
        (7500, "F"), (6001, "F"),
        (6000, "G"), (5201, "G"),
        (5200, "K"), (3701, "K"),
        (3700, "M"), (2400, "M"),
    ])
    def test_spectral_boundaries(self, T, expected):
        m = _i()
        assert m.spectral_type(T) == expected

    def test_below_M_range_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.spectral_type(2399)


class TestRoundTrip:
    def test_temperature_from_peak_sun(self):
        """Round-trip: T -> lambda -> T must recover original T."""
        m = _i()
        lam = m.wien_peak(T_SUN)
        T_back = m.temperature_from_peak(lam)
        assert abs(T_back - T_SUN) < 0.01

    def test_temperature_from_peak_sirius(self):
        m = _i()
        lam = m.wien_peak(T_SIRIUS)
        T_back = m.temperature_from_peak(lam)
        assert abs(T_back - T_SIRIUS) < 0.01

    def test_temperature_from_peak_betelgeuse(self):
        m = _i()
        lam = m.wien_peak(T_BETELGEUSE)
        T_back = m.temperature_from_peak(lam)
        assert abs(T_back - T_BETELGEUSE) < 0.01

    def test_zero_wavelength_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.temperature_from_peak(0)

    def test_hotter_star_shorter_wavelength(self):
        """Hotter star must have shorter peak wavelength."""
        m = _i()
        lam_cool = m.wien_peak(3000)
        lam_hot  = m.wien_peak(30000)
        assert lam_hot < lam_cool
