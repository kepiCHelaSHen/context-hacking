"""cat-eng-signal-filtering — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_signal_filtering_constants import *
IMPL = Path(__file__).parent.parent / "eng_signal_filtering.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the known LLM failure modes."""

    def test_fc_has_2pi(self):
        """f_c must include 2*pi — the #1 LLM error (fc_no_2pi)."""
        m = _i(); fc = m.cutoff_frequency(R_REF, C_REF)
        assert abs(fc - FC_REF) < 0.01
        assert abs(fc - FC_WRONG_NO_2PI) > 1000, "Missing 2*pi in cutoff formula!"

    def test_gain_at_cutoff_is_minus_3db(self):
        """At cutoff, gain must be -3 dB (1/sqrt(2)), NOT 0 dB or -6 dB (gain_at_cutoff_wrong)."""
        m = _i(); fc = m.cutoff_frequency(R_REF, C_REF)
        lp_g = m.lp_gain(fc, fc)
        hp_g = m.hp_gain(fc, fc)
        assert abs(lp_g - GAIN_AT_CUTOFF) < 1e-10, "LP gain at cutoff must be 1/sqrt(2)"
        assert abs(hp_g - GAIN_AT_CUTOFF) < 1e-10, "HP gain at cutoff must be 1/sqrt(2)"
        lp_db = m.gain_to_db(lp_g)
        hp_db = m.gain_to_db(hp_g)
        assert abs(lp_db - DB_AT_CUTOFF) < 1e-6, f"LP at cutoff must be -3 dB, got {lp_db}"
        assert abs(hp_db - DB_AT_CUTOFF) < 1e-6, f"HP at cutoff must be -3 dB, got {hp_db}"

    def test_lp_hp_tap_not_swapped(self):
        """LP and HP must give correct gains deep in stop-band (lp_hp_tap_swap).

        If swapped, LP would pass high and HP would pass low — both wrong.
        LP at 10*fc should be ~-20 dB (attenuated); HP at 0.1*fc should be ~-20 dB.
        """
        m = _i(); fc = m.cutoff_frequency(R_REF, C_REF)
        lp_at_10fc = m.lp_gain(10 * fc, fc)
        hp_at_01fc = m.hp_gain(0.1 * fc, fc)
        # Both should be small (~0.0995)
        assert lp_at_10fc < 0.15, "LP should attenuate at 10*fc"
        assert hp_at_01fc < 0.15, "HP should attenuate at 0.1*fc"
        # LP at low freq should be ~1; HP at high freq should be ~1
        lp_at_01fc = m.lp_gain(0.1 * fc, fc)
        hp_at_10fc = m.hp_gain(10 * fc, fc)
        assert lp_at_01fc > 0.95, "LP should pass at 0.1*fc"
        assert hp_at_10fc > 0.95, "HP should pass at 10*fc"


class TestCorrectness:
    """Verify numerical accuracy of all functions."""

    def test_cutoff_frequency_value(self):
        m = _i(); fc = m.cutoff_frequency(R_REF, C_REF)
        assert abs(fc - FC_REF) < 1e-6

    def test_lp_gain_at_10fc(self):
        m = _i(); fc = m.cutoff_frequency(R_REF, C_REF)
        g = m.lp_gain(10 * fc, fc)
        assert abs(g - LP_GAIN_AT_10FC) < 1e-10

    def test_hp_gain_at_01fc(self):
        m = _i(); fc = m.cutoff_frequency(R_REF, C_REF)
        g = m.hp_gain(0.1 * fc, fc)
        assert abs(g - HP_GAIN_AT_01FC) < 1e-10

    def test_lp_db_at_10fc(self):
        m = _i(); fc = m.cutoff_frequency(R_REF, C_REF)
        db = m.gain_to_db(m.lp_gain(10 * fc, fc))
        assert abs(db - LP_DB_AT_10FC) < 1e-6

    def test_hp_db_at_01fc(self):
        m = _i(); fc = m.cutoff_frequency(R_REF, C_REF)
        db = m.gain_to_db(m.hp_gain(0.1 * fc, fc))
        assert abs(db - HP_DB_AT_01FC) < 1e-6

    def test_gain_to_db_unity(self):
        """gain=1 => 0 dB."""
        m = _i(); assert abs(m.gain_to_db(1.0)) < 1e-15

    def test_gain_to_db_half(self):
        """gain=0.5 => ~-6.02 dB."""
        m = _i(); db = m.gain_to_db(0.5)
        assert abs(db - 20 * math.log10(0.5)) < 1e-10

    def test_design_rc(self):
        """design_rc(fc, R) should return correct C."""
        m = _i(); c = m.design_rc(FC_DESIGN_TARGET, R_DESIGN)
        assert abs(c - C_DESIGN) < 1e-15

    def test_design_rc_roundtrip(self):
        """Designing C then computing fc should give back the target."""
        m = _i()
        c = m.design_rc(FC_DESIGN_TARGET, R_DESIGN)
        fc_back = m.cutoff_frequency(R_DESIGN, c)
        assert abs(fc_back - FC_DESIGN_TARGET) < 1e-8

    def test_lp_gain_dc(self):
        """LP gain at DC (f=0) should be exactly 1."""
        m = _i(); assert abs(m.lp_gain(0.0, FC_REF) - 1.0) < 1e-15

    def test_hp_gain_dc(self):
        """HP gain at DC (f=0) should be exactly 0."""
        m = _i(); assert abs(m.hp_gain(0.0, FC_REF)) < 1e-15

    def test_lp_hp_complementary(self):
        """LP^2 + HP^2 = 1 for any frequency (power complementary)."""
        m = _i()
        for ratio in [0.01, 0.1, 0.5, 1.0, 2.0, 10.0, 100.0]:
            f = ratio * FC_REF
            lp = m.lp_gain(f, FC_REF)
            hp = m.hp_gain(f, FC_REF)
            assert abs(lp**2 + hp**2 - 1.0) < 1e-12, f"Not complementary at f/fc={ratio}"
