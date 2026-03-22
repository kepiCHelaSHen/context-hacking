"""cat-eng-pid-controller — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_pid_controller_constants import *
IMPL = Path(__file__).parent.parent / "eng_pid_controller.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_integral_includes_dt(self):
        """Integral must multiply by dt — catches 'integral_no_dt' bug."""
        m = _i()
        # If dt is forgotten, integral_term(0.5, 1.0, 0.1) would give 0.5 instead of 0.05
        # With correct formula: error_sum = e*dt = 1.0*0.1 = 0.1, I = Ki*0.1 = 0.05
        error_sum_with_dt = ERRORS[0] * DT  # 0.1
        result = m.integral_term(KI, error_sum_with_dt, DT)
        assert abs(result - I_TERMS[0]) < 1e-9, f"I term at step 0 should be {I_TERMS[0]}, got {result}"

    def test_derivative_sign_correct(self):
        """D term must use (e[n]-e[n-1]), not (e[n-1]-e[n]) — catches 'derivative_wrong_sign' bug."""
        m = _i()
        # Step 3: e[3]=0.5, e[2]=1.0 → D = 0.1*(0.5-1.0)/0.1 = -0.5
        d = m.derivative_term(KD, ERRORS[3], ERRORS[2], DT)
        assert abs(d - D_TERMS[3]) < 1e-9, f"D term at step 3 should be {D_TERMS[3]}, got {d}"
        # Must be negative when error decreases
        assert d < 0, "D term must be negative when error is decreasing"

    def test_derivative_on_error_not_pv(self):
        """D term must act on error signal, not process variable — catches 'derivative_on_pv' bug."""
        m = _i()
        # If setpoint=1 and e=[1.0, 0.5], process variable pv = [0.0, 0.5]
        # D on error: Kd*(0.5-1.0)/dt = 0.1*(-0.5)/0.1 = -0.5
        # D on pv:    Kd*(0.5-0.0)/dt = 0.1*(0.5)/0.1  = +0.5 (wrong sign!)
        d = m.derivative_term(KD, 0.5, 1.0, DT)
        assert d < 0, "D on error must be negative when error decreases (pv increases)"
        assert abs(d - (-0.5)) < 1e-9


class TestCorrectness:
    def test_proportional(self):
        m = _i()
        for n, e in enumerate(ERRORS):
            assert abs(m.proportional(KP, e) - P_TERMS[n]) < 1e-9

    def test_integral_term_accumulates(self):
        m = _i()
        error_sum = 0.0
        for n, e in enumerate(ERRORS):
            error_sum += e * DT
            assert abs(error_sum - I_SUMS[n]) < 1e-9
            assert abs(m.integral_term(KI, error_sum, DT) - I_TERMS[n]) < 1e-9

    def test_derivative_term_all_steps(self):
        m = _i()
        for n in range(1, len(ERRORS)):
            d = m.derivative_term(KD, ERRORS[n], ERRORS[n - 1], DT)
            assert abs(d - D_TERMS[n]) < 1e-9, f"Step {n}: expected {D_TERMS[n]}, got {d}"

    def test_pid_output_combines_terms(self):
        m = _i()
        for n in range(len(ERRORS)):
            u = m.pid_output(KP, KI, KD, ERRORS[n], I_TERMS[n], D_TERMS[n])
            assert abs(u - U_EXPECTED[n]) < 1e-9, f"Step {n}: expected {U_EXPECTED[n]}, got {u}"

    def test_full_step_response(self):
        m = _i()
        results = m.simulate_step_response(KP, KI, KD, ERRORS, DT)
        for n, (u, u_exp) in enumerate(zip(results, U_EXPECTED)):
            assert abs(u - u_exp) < 1e-9, f"Step {n}: expected {u_exp}, got {u}"

    def test_zero_error_zero_output(self):
        """Zero error throughout should yield zero output."""
        m = _i()
        results = m.simulate_step_response(KP, KI, KD, [0.0, 0.0, 0.0], DT)
        for u in results:
            assert abs(u) < 1e-9
