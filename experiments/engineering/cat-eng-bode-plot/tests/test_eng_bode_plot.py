"""cat-eng-bode-plot — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_bode_plot_constants import *
IMPL = Path(__file__).parent.parent / "eng_bode_plot.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the known LLM failure modes."""

    def test_phase_at_pole_is_minus_45_not_minus_90(self):
        """At ω = ω₀ the phase MUST be −45°, not −90°."""
        m = _i(); phase = m.first_order_phase(OMEGA_0, OMEGA_0)
        assert abs(phase - PHASE_AT_POLE) < 1e-10, \
            f"Phase at pole = {phase}°; expected −45° (not −90°!)"
        assert abs(phase - WRONG_PHASE_AT_POLE) > 40, \
            "Phase incorrectly returns −90° at pole frequency"

    def test_gain_is_in_db_not_linear(self):
        """Gain at ω₀ must be ≈ −3.01 dB, not ≈ 0.707 (linear)."""
        m = _i(); g = m.first_order_gain_db(OMEGA_0, OMEGA_0)
        # Correct: −3.0103 dB.  Wrong if linear: 0.7071.
        assert g < 0, "Gain in dB at pole must be negative"
        assert abs(g - GAIN_DB_AT_POLE) < 1e-6, \
            f"Gain = {g} dB; expected {GAIN_DB_AT_POLE} dB"
        assert abs(g - WRONG_GAIN_LINEAR) > 1.0, \
            "Gain returned as linear ratio, not converted to dB"

    def test_pole_slope_is_negative(self):
        """A pole produces −20 dB/decade slope, NOT +20 dB/decade."""
        m = _i()
        g_low  = m.first_order_gain_db(0.1 * OMEGA_0, OMEGA_0)
        g_high = m.first_order_gain_db(10.0 * OMEGA_0, OMEGA_0)
        # Gain must decrease with frequency for a pole
        assert g_high < g_low, "Pole should attenuate at higher frequencies"
        slope = g_high - g_low  # should be ≈ −20 dB over 2 decades → ~−10 per decade
        assert slope < 0, "Pole slope must be negative (−20 dB/dec)"


class TestGainFunction:
    """Verify first_order_gain_db numerical accuracy."""

    def test_gain_at_pole(self):
        m = _i(); g = m.first_order_gain_db(OMEGA_0, OMEGA_0)
        assert abs(g - GAIN_DB_AT_POLE) < 1e-6

    def test_gain_at_10x(self):
        m = _i(); g = m.first_order_gain_db(10.0 * OMEGA_0, OMEGA_0)
        assert abs(g - GAIN_DB_AT_10X) < 1e-4

    def test_gain_at_01x(self):
        m = _i(); g = m.first_order_gain_db(0.1 * OMEGA_0, OMEGA_0)
        assert abs(g - GAIN_DB_AT_01X) < 1e-4

    def test_gain_at_dc(self):
        """At ω = 0, gain = 0 dB."""
        m = _i(); g = m.first_order_gain_db(0.0, OMEGA_0)
        assert abs(g - 0.0) < 1e-12

    def test_gain_decreases_with_frequency(self):
        """Monotonically decreasing gain for a first-order pole."""
        m = _i()
        freqs = [1.0, 10.0, 100.0, 1000.0, 10000.0]
        gains = [m.first_order_gain_db(w, OMEGA_0) for w in freqs]
        for i in range(len(gains) - 1):
            assert gains[i] > gains[i + 1], \
                f"Gain not decreasing: {gains[i]} vs {gains[i+1]} at {freqs[i+1]} rad/s"


class TestPhaseFunction:
    """Verify first_order_phase numerical accuracy."""

    def test_phase_at_pole(self):
        m = _i(); p = m.first_order_phase(OMEGA_0, OMEGA_0)
        assert abs(p - PHASE_AT_POLE) < 1e-10

    def test_phase_at_10x(self):
        m = _i(); p = m.first_order_phase(10.0 * OMEGA_0, OMEGA_0)
        assert abs(p - PHASE_AT_10X) < 1e-4

    def test_phase_at_01x(self):
        m = _i(); p = m.first_order_phase(0.1 * OMEGA_0, OMEGA_0)
        assert abs(p - PHASE_AT_01X) < 1e-4

    def test_phase_at_dc(self):
        """At ω = 0, phase = 0°."""
        m = _i(); p = m.first_order_phase(0.0, OMEGA_0)
        assert abs(p) < 1e-12

    def test_phase_approaches_minus_90(self):
        """At very high ω, phase → −90° (but never reaches it)."""
        m = _i(); p = m.first_order_phase(1e6 * OMEGA_0, OMEGA_0)
        assert -90.0 < p < -89.99, f"Phase at very high freq = {p}°"


class TestDbConversions:
    """Verify dB ↔ linear conversion functions."""

    def test_db_to_linear_0db(self):
        m = _i(); assert abs(m.db_to_linear(0.0) - 1.0) < 1e-12

    def test_db_to_linear_minus3(self):
        m = _i(); val = m.db_to_linear(GAIN_DB_AT_POLE)
        assert abs(val - LINEAR_OF_M3DB) < 1e-10

    def test_db_to_linear_minus6(self):
        m = _i(); val = m.db_to_linear(DB_OF_HALF)
        assert abs(val - 0.5) < 1e-10

    def test_linear_to_db_1(self):
        m = _i(); assert abs(m.linear_to_db(1.0)) < 1e-12

    def test_linear_to_db_half(self):
        m = _i(); val = m.linear_to_db(0.5)
        assert abs(val - DB_OF_HALF) < 1e-6

    def test_linear_to_db_double(self):
        m = _i(); val = m.linear_to_db(2.0)
        assert abs(val - DB_OF_DOUBLE) < 1e-6

    def test_roundtrip_db_linear(self):
        """db_to_linear(linear_to_db(x)) == x."""
        m = _i()
        for x in [0.001, 0.5, 1.0, 2.0, 100.0]:
            assert abs(m.db_to_linear(m.linear_to_db(x)) - x) < 1e-10

    def test_linear_to_db_rejects_nonpositive(self):
        m = _i()
        with pytest.raises(ValueError):
            m.linear_to_db(0.0)
        with pytest.raises(ValueError):
            m.linear_to_db(-1.0)
