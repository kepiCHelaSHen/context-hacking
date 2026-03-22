"""cat-eng-rc-circuit — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_rc_circuit_constants import *
IMPL = Path(__file__).parent.parent / "eng_rc_circuit.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the known LLM failure modes."""

    def test_fc_has_2pi(self):
        """f_c must include 2*pi — the #1 LLM error."""
        m = _i(); fc = m.cutoff_freq_hz(R_REF, C_REF)
        # Correct: ~159.15 Hz.  Wrong: 1000 Hz (off by 2*pi).
        assert abs(fc - FC_REF) < 0.01
        assert abs(fc - FC_WRONG) > 100, "Missing 2*pi in cutoff formula!"

    def test_fc_not_omega(self):
        """f_c and omega_c must differ by factor 2*pi."""
        m = _i()
        fc = m.cutoff_freq_hz(R_REF, C_REF)
        wc = m.cutoff_freq_rad(R_REF, C_REF)
        ratio = wc / fc
        assert abs(ratio - 2 * math.pi) < 0.001, "f_c and omega_c should differ by 2*pi"

    def test_tau_correct(self):
        """tau = R * C exactly."""
        m = _i(); tau = m.time_constant(R_REF, C_REF)
        assert abs(tau - TAU_REF) < 1e-12

    def test_charging_not_discharging(self):
        """Charging voltage at t=tau must be ABOVE V0/2 (rising), not below."""
        m = _i(); v = m.charging_voltage(V0_TEST, R_REF, C_REF, TAU_REF)
        assert v > V0_TEST / 2, "Charging should be above V0/2 at t=tau"
        assert abs(v - V_CHARGE_AT_TAU) < 1e-6

    def test_discharging_not_charging(self):
        """Discharging voltage at t=tau must be BELOW V0/2 (falling), not above."""
        m = _i(); v = m.discharging_voltage(V0_TEST, R_REF, C_REF, TAU_REF)
        assert v < V0_TEST / 2, "Discharging should be below V0/2 at t=tau"
        assert abs(v - V_DISCHARGE_AT_TAU) < 1e-6


class TestCorrectness:
    """Verify numerical accuracy of all functions."""

    def test_time_constant_value(self):
        m = _i(); tau = m.time_constant(R_REF, C_REF)
        assert abs(tau - 1e-3) < 1e-12

    def test_cutoff_freq_hz_value(self):
        m = _i(); fc = m.cutoff_freq_hz(R_REF, C_REF)
        expected = 1.0 / (2.0 * math.pi * 1e-3)
        assert abs(fc - expected) < 1e-6

    def test_cutoff_freq_rad_value(self):
        m = _i(); wc = m.cutoff_freq_rad(R_REF, C_REF)
        assert abs(wc - 1000.0) < 1e-6

    def test_gain_at_cutoff(self):
        m = _i(); g = m.gain_at_cutoff()
        assert abs(g - GAIN_AT_CUTOFF) < 1e-10

    def test_charging_at_zero(self):
        """At t=0, charging voltage = 0."""
        m = _i(); v = m.charging_voltage(V0_TEST, R_REF, C_REF, 0.0)
        assert abs(v) < 1e-12

    def test_discharging_at_zero(self):
        """At t=0, discharging voltage = V0."""
        m = _i(); v = m.discharging_voltage(V0_TEST, R_REF, C_REF, 0.0)
        assert abs(v - V0_TEST) < 1e-12

    def test_charging_at_5tau(self):
        """At t=5*tau, charging is ~99.3% of V0."""
        m = _i(); v = m.charging_voltage(V0_TEST, R_REF, C_REF, 5 * TAU_REF)
        assert abs(v - V0_TEST * (1 - math.exp(-5))) < 1e-8

    def test_omega_equals_2pi_f(self):
        """omega_c = 2*pi*f_c — fundamental relationship."""
        m = _i()
        fc = m.cutoff_freq_hz(R_REF, C_REF)
        wc = m.cutoff_freq_rad(R_REF, C_REF)
        assert abs(wc - 2 * math.pi * fc) < 1e-6
