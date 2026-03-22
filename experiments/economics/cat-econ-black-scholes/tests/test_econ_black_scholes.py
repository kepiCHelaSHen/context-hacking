"""cat-econ-black-scholes — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_black_scholes_constants import *
IMPL = Path(__file__).parent.parent / "econ_black_scholes.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_sigma_is_annualized(self):
        """sigma_not_annualized: monthly sigma=0.20 must be scaled by sqrt(12)."""
        m = _i()
        # Using annualized sigma=0.20 should give our known call price
        C = m.black_scholes_call(S_TEST, K_TEST, R_TEST, SIGMA_TEST, T_TEST)
        assert abs(C - CALL_TEST) < 1e-6, f"Call={C}, expected={CALL_TEST}"

    def test_d2_minus_not_plus(self):
        """d2_wrong_sign: d2 must be d1 - sigma*sqrt(T), not d1 + sigma*sqrt(T)."""
        m = _i()
        d1_v = m.d1(S_TEST, K_TEST, R_TEST, SIGMA_TEST, T_TEST)
        d2_v = m.d2_val(d1_v, SIGMA_TEST, T_TEST)
        assert abs(d2_v - D2_TEST) < 1e-10, f"d2={d2_v}, expected={D2_TEST}"
        # d2 must be LESS than d1 (since sigma*sqrt(T) > 0)
        assert d2_v < d1_v, "d2 must be less than d1"

    def test_put_call_parity(self):
        """put_call_parity_wrong: C - P must equal S - K*e^(-rT)."""
        m = _i()
        C = m.black_scholes_call(S_TEST, K_TEST, R_TEST, SIGMA_TEST, T_TEST)
        P = m.black_scholes_put(S_TEST, K_TEST, R_TEST, SIGMA_TEST, T_TEST)
        assert m.put_call_parity_check(C, P, S_TEST, K_TEST, R_TEST, T_TEST)

class TestCorrectness:
    def test_d1_value(self):
        m = _i()
        d1_v = m.d1(S_TEST, K_TEST, R_TEST, SIGMA_TEST, T_TEST)
        assert abs(d1_v - D1_TEST) < 1e-10, f"d1={d1_v}, expected={D1_TEST}"

    def test_d2_value(self):
        m = _i()
        d1_v = m.d1(S_TEST, K_TEST, R_TEST, SIGMA_TEST, T_TEST)
        d2_v = m.d2_val(d1_v, SIGMA_TEST, T_TEST)
        assert abs(d2_v - D2_TEST) < 1e-10, f"d2={d2_v}, expected={D2_TEST}"

    def test_call_price(self):
        m = _i()
        C = m.black_scholes_call(S_TEST, K_TEST, R_TEST, SIGMA_TEST, T_TEST)
        assert abs(C - CALL_TEST) < 1e-6, f"Call={C}, expected={CALL_TEST}"

    def test_put_price(self):
        m = _i()
        P = m.black_scholes_put(S_TEST, K_TEST, R_TEST, SIGMA_TEST, T_TEST)
        assert abs(P - PUT_TEST) < 1e-6, f"Put={P}, expected={PUT_TEST}"

    def test_parity_numerical(self):
        """C - P should exactly equal S - K*e^(-rT)."""
        m = _i()
        C = m.black_scholes_call(S_TEST, K_TEST, R_TEST, SIGMA_TEST, T_TEST)
        P = m.black_scholes_put(S_TEST, K_TEST, R_TEST, SIGMA_TEST, T_TEST)
        lhs = C - P
        assert abs(lhs - PARITY_RHS) < 1e-10, f"C-P={lhs}, S-Ke^(-rT)={PARITY_RHS}"
