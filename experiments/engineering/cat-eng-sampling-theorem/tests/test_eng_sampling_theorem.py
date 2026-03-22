"""cat-eng-sampling-theorem — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_sampling_theorem_constants import *
IMPL = Path(__file__).parent.parent / "eng_sampling_theorem.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the known LLM failure modes."""

    def test_nyquist_rate_is_2x_not_1x(self):
        """Nyquist rate must be 2*f_max — the #1 LLM error."""
        m = _i(); rate = m.nyquist_rate(F_MAX_AUDIO)
        assert rate == NYQUIST_RATE, f"Nyquist rate should be {NYQUIST_RATE}, got {rate}"
        assert rate != NYQUIST_RATE_WRONG, "Using f_s = f_max (1x) instead of 2*f_max!"

    def test_nyquist_rate_not_equal_f_max(self):
        """Nyquist rate must NOT equal f_max."""
        m = _i(); rate = m.nyquist_rate(F_MAX_AUDIO)
        assert rate != F_MAX_AUDIO, "Nyquist rate = f_max is WRONG; must be 2*f_max"

    def test_alias_frequency_correct_formula(self):
        """Alias frequency uses |f_signal - k*f_s| for nearest k."""
        m = _i(); af = m.alias_frequency(ALIAS_SIGNAL_FREQ, ALIAS_SAMPLE_RATE)
        assert af == ALIASED_FREQ, f"Alias of {ALIAS_SIGNAL_FREQ} Hz at {ALIAS_SAMPLE_RATE} Hz should be {ALIASED_FREQ}, got {af}"

    def test_nyquist_freq_vs_rate_distinct(self):
        """Nyquist frequency (f_s/2) and Nyquist rate (2*f_max) are distinct concepts."""
        m = _i()
        freq = m.nyquist_frequency(CD_SAMPLE_RATE)
        rate = m.nyquist_rate(F_MAX_AUDIO)
        # Nyquist freq of CD = 22050 Hz; Nyquist rate for audio = 40000 Hz — different!
        assert freq == CD_NYQUIST_FREQ, f"Nyquist frequency of CD should be {CD_NYQUIST_FREQ}, got {freq}"
        assert rate == NYQUIST_RATE, f"Nyquist rate for audio should be {NYQUIST_RATE}, got {rate}"
        assert freq != rate, "Nyquist frequency and Nyquist rate must not be confused"


class TestCorrectness:
    """Verify numerical accuracy of all functions."""

    def test_nyquist_rate_audio(self):
        """20 kHz audio -> 40 kHz minimum sampling rate."""
        m = _i(); rate = m.nyquist_rate(F_MAX_AUDIO)
        assert rate == 40000

    def test_nyquist_rate_generic(self):
        """Generic: f_max=5000 -> rate=10000."""
        m = _i(); rate = m.nyquist_rate(5000)
        assert rate == 10000

    def test_nyquist_frequency_cd(self):
        """CD sample rate 44100 -> Nyquist freq 22050."""
        m = _i(); freq = m.nyquist_frequency(CD_SAMPLE_RATE)
        assert freq == 22050.0

    def test_nyquist_frequency_generic(self):
        """f_s=8000 -> Nyquist freq 4000."""
        m = _i(); freq = m.nyquist_frequency(8000)
        assert freq == 4000.0

    def test_is_aliased_above(self):
        """Signal above Nyquist frequency is aliased."""
        m = _i(); result = m.is_aliased(ALIAS_SIGNAL_FREQ, ALIAS_SAMPLE_RATE)
        assert result is True

    def test_is_aliased_below(self):
        """Signal below Nyquist frequency is NOT aliased."""
        m = _i(); result = m.is_aliased(SAFE_SIGNAL_FREQ, ALIAS_SAMPLE_RATE)
        assert result is False

    def test_is_aliased_at_boundary(self):
        """Signal exactly at Nyquist frequency (f_s/2) is NOT aliased."""
        m = _i(); result = m.is_aliased(15000, 30000)
        assert result is False

    def test_alias_frequency_25k_at_30k(self):
        """25 kHz at 30 kHz -> |25000 - 1*30000| = 5000 Hz."""
        m = _i(); af = m.alias_frequency(25000, 30000)
        assert af == 5000

    def test_alias_frequency_not_aliased(self):
        """Signal below Nyquist freq returns unchanged."""
        m = _i(); af = m.alias_frequency(SAFE_SIGNAL_FREQ, ALIAS_SAMPLE_RATE)
        assert af == float(SAFE_SIGNAL_FREQ)

    def test_alias_frequency_high_harmonic(self):
        """50 kHz at 30 kHz -> |50000 - 2*30000| = |50000 - 60000| = 10000 Hz."""
        m = _i(); af = m.alias_frequency(50000, 30000)
        assert af == 10000

    def test_cd_rate_above_nyquist(self):
        """CD rate (44100) must exceed Nyquist rate (40000) for 20 kHz audio."""
        m = _i(); rate = m.nyquist_rate(F_MAX_AUDIO)
        assert CD_SAMPLE_RATE > rate, "CD rate should exceed Nyquist rate for margin"

    def test_relationship_rate_and_freq(self):
        """Nyquist rate for f_max should give Nyquist freq = f_max."""
        m = _i()
        rate = m.nyquist_rate(F_MAX_AUDIO)
        freq = m.nyquist_frequency(rate)
        assert freq == F_MAX_AUDIO, "Nyquist freq at Nyquist rate should equal f_max"
