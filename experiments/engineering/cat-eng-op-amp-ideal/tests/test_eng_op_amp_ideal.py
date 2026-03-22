"""cat-eng-op-amp-ideal — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_op_amp_ideal_constants import *
IMPL = Path(__file__).parent.parent / "eng_op_amp_ideal.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Guard against the three catalogued LLM errors."""

    def test_inverting_gain_is_negative(self):
        """PRIOR_ERROR inverting_positive: gain must be negative."""
        m = _i()
        g = m.inverting_gain(RF, RIN)
        assert g < 0, f"Inverting gain must be negative, got {g}"
        assert abs(g - INVERTING_GAIN) < 1e-9

    def test_noninverting_gain_has_plus_1(self):
        """PRIOR_ERROR noninverting_no_plus_1: gain = 1 + Rf/Rin, not Rf/Rin."""
        m = _i()
        g = m.noninverting_gain(RF, RIN)
        assert g >= 1.0, f"Non-inverting gain must be >= 1, got {g}"
        assert abs(g - NONINVERTING_GAIN) < 1e-9

    def test_virtual_ground_inverting(self):
        """PRIOR_ERROR virtual_ground_wrong: inverting input sits at 0 V (virtual ground).
        This means Vout = -(Rf/Rin)*Vin, NOT +(Rf/Rin)*Vin."""
        m = _i()
        vout = m.inverting_output(VIN, RF, RIN)
        # Virtual ground => V- = V+ = 0 => current through Rin flows into Rf => negative output
        assert vout < 0, f"With virtual ground applied, inverting output must be negative, got {vout}"
        assert abs(vout - INVERTING_VOUT) < 1e-9


class TestCorrectness:
    """Verify all formulas against frozen constants."""

    def test_inverting_output(self):
        m = _i()
        assert abs(m.inverting_output(VIN, RF, RIN) - INVERTING_VOUT) < 1e-9

    def test_noninverting_output(self):
        m = _i()
        assert abs(m.noninverting_output(VIN, RF, RIN) - NONINVERTING_VOUT) < 1e-9

    def test_difference_output(self):
        m = _i()
        assert abs(m.difference_output(V1_DIFF, V2_DIFF, RF, RIN) - DIFF_VOUT) < 1e-9

    def test_voltage_follower(self):
        """Follower: Rf=0, Rin->inf. Use noninverting_gain(0, large_R) ~ 1."""
        m = _i()
        g = m.noninverting_gain(0, 1e6)
        assert abs(g - 1.0) < 1e-6

    def test_inverting_gain_scales(self):
        """Double Rf => double the magnitude of gain."""
        m = _i()
        g1 = m.inverting_gain(RF, RIN)
        g2 = m.inverting_gain(2 * RF, RIN)
        assert abs(g2 / g1 - 2.0) < 1e-9

    def test_noninverting_always_gte_1(self):
        """Non-inverting gain is always >= 1, even with tiny Rf."""
        m = _i()
        assert m.noninverting_gain(0, RIN) >= 1.0
        assert m.noninverting_gain(1, RIN) >= 1.0

    def test_difference_symmetry(self):
        """Swapping V1 and V2 flips the sign."""
        m = _i()
        d1 = m.difference_output(V1_DIFF, V2_DIFF, RF, RIN)
        d2 = m.difference_output(V2_DIFF, V1_DIFF, RF, RIN)
        assert abs(d1 + d2) < 1e-9
