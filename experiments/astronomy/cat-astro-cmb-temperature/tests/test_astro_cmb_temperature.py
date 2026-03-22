"""cat-astro-cmb-temperature — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_cmb_temperature_constants import *
IMPL = Path(__file__).parent.parent / "astro_cmb_temperature.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


# ── Prior-error tests ──────────────────────────────────────────────

class TestPriorErrors:
    def test_t_cmb_not_3k(self):
        """t_cmb_3k: CMB temperature must be 2.7255 K, NOT rounded to 3 K."""
        m = _i()
        T = m.cmb_temperature()
        assert abs(T - 2.7255) < 0.001, f"Got {T}, expected 2.7255 K (not 3 K)"
        assert abs(T - 3.0) > 0.1, f"Got {T}, appears to be rounded to 3 K"

    def test_peak_in_microwave_not_visible(self):
        """peak_wrong_band: CMB peak at 1.063 mm is microwave, not visible/IR."""
        m = _i()
        lam = m.cmb_peak_wavelength(T_CMB)
        lam_mm = lam * 1e3
        # Microwave range: ~1 mm to ~1 m; visible: 380–700 nm; IR: 700 nm–1 mm
        assert lam_mm > 1.0, f"Peak {lam_mm:.3f} mm — should be > 1 mm (microwave)"
        assert lam_mm < 10.0, f"Peak {lam_mm:.3f} mm — unexpectedly large"
        # Must NOT be in visible or near-IR range
        lam_nm = lam * 1e9
        assert lam_nm > 1e6, f"Peak {lam_nm:.0f} nm — in visible/IR range, should be microwave"

    def test_cmb_is_perfect_blackbody(self):
        """not_blackbody: CMB peak wavelength matches Wien's law to < 0.01%."""
        m = _i()
        lam = m.cmb_peak_wavelength(T_CMB, b=WIEN_B)
        expected = WIEN_B / T_CMB
        deviation = abs(lam - expected) / expected
        assert deviation < 1e-4, f"Deviation {deviation:.2e} exceeds 0.01% — consistent with perfect blackbody"

    def test_3k_error_propagates_to_peak(self):
        """t_cmb_3k: Using 3 K instead of 2.7255 K gives ~10% wrong peak."""
        m = _i()
        lam_correct = m.cmb_peak_wavelength(T_CMB)
        lam_wrong = m.cmb_peak_wavelength(T_CMB_WRONG_3K)
        error_frac = abs(lam_wrong - lam_correct) / lam_correct
        assert error_frac > 0.09, f"3K error should cause >9% shift, got {error_frac*100:.1f}%"


# ── Correctness tests ──────────────────────────────────────────────

class TestCmbTemperature:
    def test_returns_precise_value(self):
        m = _i()
        assert m.cmb_temperature() == 2.7255

    def test_matches_frozen_constant(self):
        m = _i()
        assert m.cmb_temperature() == T_CMB


class TestCmbPeakWavelength:
    def test_default_peak(self):
        """Default (T=2.7255, b=2.898e-3) -> ~1.063e-3 m."""
        m = _i()
        lam = m.cmb_peak_wavelength()
        assert abs(lam - LAMBDA_MAX_M) / LAMBDA_MAX_M < 1e-6

    def test_peak_mm(self):
        """Peak should be ~1.063 mm."""
        m = _i()
        lam = m.cmb_peak_wavelength()
        mm = lam * 1e3
        assert abs(mm - 1.063) < 0.001

    def test_custom_temperature(self):
        m = _i()
        lam = m.cmb_peak_wavelength(T=5778)
        expected = 2.898e-3 / 5778
        assert abs(lam - expected) / expected < 1e-6

    def test_zero_temperature_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.cmb_peak_wavelength(T=0)

    def test_negative_temperature_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.cmb_peak_wavelength(T=-1)


class TestCmbPeakFrequency:
    def test_from_peak_wavelength(self):
        """c / lambda_max should give ~281.95 GHz."""
        m = _i()
        lam = m.cmb_peak_wavelength()
        nu = m.cmb_peak_frequency(lam)
        expected = C_LIGHT / LAMBDA_MAX_M
        assert abs(nu - expected) / expected < 1e-4

    def test_zero_wavelength_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.cmb_peak_frequency(0)

    def test_negative_wavelength_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.cmb_peak_frequency(-1e-3)


class TestWienFrequencyPeak:
    def test_default_cmb(self):
        """Wien frequency peak at T_CMB should be ~160.23 GHz."""
        m = _i()
        nu = m.wien_frequency_peak()
        assert abs(nu / 1e9 - 160.23) < 0.1

    def test_matches_frozen_constant(self):
        m = _i()
        nu = m.wien_frequency_peak(T_CMB)
        assert abs(nu - NU_MAX_HZ) / NU_MAX_HZ < 1e-6

    def test_zero_temperature_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.wien_frequency_peak(T=0)


class TestTemperatureAtRedshift:
    def test_last_scattering(self):
        """At z=1089, T should be ~2970.8 K."""
        m = _i()
        T = m.temperature_at_redshift(T_CMB, Z_LAST_SCATTERING)
        assert abs(T - T_LAST_SCATTERING) < 0.1

    def test_present_day(self):
        """At z=0, T should equal T_now."""
        m = _i()
        T = m.temperature_at_redshift(T_CMB, 0)
        assert T == T_CMB

    def test_redshift_1(self):
        """At z=1, T should be 2*T_now."""
        m = _i()
        T = m.temperature_at_redshift(T_CMB, 1)
        assert abs(T - 2 * T_CMB) < 1e-10

    def test_negative_redshift_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.temperature_at_redshift(T_CMB, -1)

    def test_high_redshift(self):
        """At z=1089, temperature should be ~2968-2971 K."""
        m = _i()
        T = m.temperature_at_redshift(T_CMB, 1089)
        assert 2968 < T < 2972


class TestRoundTrip:
    def test_wavelength_roundtrip(self):
        """T -> lambda -> T via b/lambda must recover T."""
        m = _i()
        lam = m.cmb_peak_wavelength(T_CMB)
        T_back = WIEN_B / lam
        assert abs(T_back - T_CMB) < 1e-10

    def test_hotter_gives_shorter_wavelength(self):
        """Higher temperature must give shorter peak wavelength."""
        m = _i()
        lam_cmb = m.cmb_peak_wavelength(T_CMB)
        lam_hot = m.cmb_peak_wavelength(T=6000)
        assert lam_hot < lam_cmb
