"""cat-eng-rl-circuit — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_rl_circuit_constants import *
IMPL = Path(__file__).parent.parent / "eng_rl_circuit.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    """Guards against known LLM mistakes."""
    def test_tau_is_L_over_R_not_R_over_L(self):
        """τ = L/R must give seconds, NOT R/L which gives s⁻¹."""
        m = _i(); tau = m.time_constant(L_TEST, R_TEST)
        assert abs(tau - TAU_TEST) < 1e-12
        assert abs(tau - TAU_WRONG) > 1.0, "Got R/L instead of L/R!"

    def test_63_percent_at_tau_not_50(self):
        """At t=τ the current reaches 63.2% of final, NOT 50%."""
        m = _i(); i_tau = m.current_rise(V_TEST, R_TEST, L_TEST, TAU_TEST)
        assert abs(i_tau - I_AT_TAU) < 1e-6
        assert abs(i_tau / I_FINAL - FRACTION_AT_TAU) < 1e-6

    def test_current_rise_not_voltage(self):
        """current_rise must return current (A), not voltage (V)."""
        m = _i(); i_val = m.current_rise(V_TEST, R_TEST, L_TEST, TAU_TEST)
        # Must be near 0.063 A, not near 6.32 V or 10 V
        assert i_val < 1.0, "Returned voltage-scale value instead of current"

class TestTimeConstant:
    def test_tau_value(self):
        m = _i(); tau = m.time_constant(L_TEST, R_TEST)
        assert abs(tau - 0.005) < 1e-12

    def test_tau_units_are_seconds(self):
        """L(H)/R(Ω) = H/Ω = s."""
        m = _i(); tau = m.time_constant(0.5, 100.0)
        assert tau < 1.0, "τ should be 5 ms, not 200"

class TestCurrentRise:
    def test_zero_time(self):
        m = _i(); assert abs(m.current_rise(V_TEST, R_TEST, L_TEST, 0.0)) < 1e-15

    def test_at_one_tau(self):
        m = _i(); i_val = m.current_rise(V_TEST, R_TEST, L_TEST, TAU_TEST)
        assert abs(i_val - I_AT_TAU) < 1e-6

    def test_steady_state(self):
        """At t >> τ, i(t) → V/R."""
        m = _i(); i_val = m.current_rise(V_TEST, R_TEST, L_TEST, 10 * TAU_TEST)
        assert abs(i_val - I_FINAL) < 1e-4

class TestCurrentDecay:
    def test_zero_time(self):
        m = _i(); assert abs(m.current_decay(I0_DECAY, R_TEST, L_TEST, 0.0) - I0_DECAY) < 1e-15

    def test_at_one_tau(self):
        m = _i(); i_val = m.current_decay(I0_DECAY, R_TEST, L_TEST, TAU_TEST)
        assert abs(i_val - I_DECAY_AT_TAU) < 1e-6

    def test_approaches_zero(self):
        m = _i(); i_val = m.current_decay(I0_DECAY, R_TEST, L_TEST, 10 * TAU_TEST)
        assert i_val < 1e-4

class TestCutoffFreq:
    def test_cutoff_value(self):
        m = _i(); fc = m.cutoff_freq(R_TEST, L_TEST)
        assert abs(fc - F_C) < 1e-3

    def test_cutoff_formula(self):
        """f_c = R/(2πL)."""
        m = _i(); fc = m.cutoff_freq(200.0, 1.0)
        expected = 200.0 / (2.0 * math.pi * 1.0)
        assert abs(fc - expected) < 1e-6
