"""cat-eng-heat-exchanger — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_heat_exchanger_constants import *
IMPL = Path(__file__).parent.parent / "eng_heat_exchanger.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    """Catch the three documented LLM failure modes."""

    def test_counter_not_parallel_swap(self):
        """counter_parallel_swap: counter-flow must NOT pair hot-in with cold-in."""
        m = _i()
        dT1, dT2 = m.counter_flow_deltas(TH_IN, TH_OUT, TC_IN, TC_OUT)
        # Correct: dT1 = Th_in - Tc_out = 40, dT2 = Th_out - Tc_in = 30
        # Wrong (parallel): dT1 = Th_in - Tc_in = 60, dT2 = Th_out - Tc_out = 10
        assert abs(dT1 - DT1_COUNTER) < 0.01, f"Expected ΔT₁={DT1_COUNTER}, got {dT1}"
        assert abs(dT2 - DT2_COUNTER) < 0.01, f"Expected ΔT₂={DT2_COUNTER}, got {dT2}"

    def test_lmtd_is_log_mean_not_arithmetic(self):
        """lmtd_arithmetic_mean: must use log-mean, not (ΔT₁+ΔT₂)/2."""
        m = _i()
        result = m.lmtd(DT1_COUNTER, DT2_COUNTER)
        arithmetic_mean = (DT1_COUNTER + DT2_COUNTER) / 2  # = 35.0
        # Log-mean ≈ 34.76, arithmetic = 35.0 — they differ
        assert abs(result - LMTD_COUNTER) < 0.1, f"Expected LMTD={LMTD_COUNTER:.2f}, got {result:.2f}"
        assert abs(result - arithmetic_mean) > 0.1, "LMTD should differ from arithmetic mean"

    def test_wrong_endpoint_pairing_rejected(self):
        """wrong_endpoint_pairing: counter-flow must pair hot-in with cold-OUT, not cold-in."""
        m = _i()
        dT1, _ = m.counter_flow_deltas(TH_IN, TH_OUT, TC_IN, TC_OUT)
        wrong_dT1 = TH_IN - TC_IN  # = 60 (wrong pairing)
        assert abs(dT1 - wrong_dT1) > 1.0, "Counter-flow ΔT₁ must NOT be Th_in - Tc_in"

class TestCorrectness:
    """Verify numerical accuracy against frozen constants."""

    def test_counter_flow_lmtd_value(self):
        m = _i()
        dT1, dT2 = m.counter_flow_deltas(TH_IN, TH_OUT, TC_IN, TC_OUT)
        result = m.lmtd(dT1, dT2)
        assert abs(result - LMTD_COUNTER) < 0.01

    def test_parallel_flow_lmtd_value(self):
        m = _i()
        dT1, dT2 = m.parallel_flow_deltas(TH_IN, TH_OUT, TC_IN, TC_OUT)
        result = m.lmtd(dT1, dT2)
        assert abs(result - LMTD_PARALLEL) < 0.01

    def test_counter_lmtd_greater_than_parallel(self):
        m = _i()
        dT1_c, dT2_c = m.counter_flow_deltas(TH_IN, TH_OUT, TC_IN, TC_OUT)
        dT1_p, dT2_p = m.parallel_flow_deltas(TH_IN, TH_OUT, TC_IN, TC_OUT)
        assert m.lmtd(dT1_c, dT2_c) > m.lmtd(dT1_p, dT2_p)

    def test_heat_transfer_counter(self):
        m = _i()
        Q = m.heat_transfer(U_TEST, A_TEST, LMTD_COUNTER)
        assert abs(Q - Q_COUNTER_TEST) < 1.0

    def test_heat_transfer_parallel(self):
        m = _i()
        Q = m.heat_transfer(U_TEST, A_TEST, LMTD_PARALLEL)
        assert abs(Q - Q_PARALLEL_TEST) < 1.0

    def test_parallel_flow_deltas(self):
        m = _i()
        dT1, dT2 = m.parallel_flow_deltas(TH_IN, TH_OUT, TC_IN, TC_OUT)
        assert abs(dT1 - DT1_PARALLEL) < 0.01
        assert abs(dT2 - DT2_PARALLEL) < 0.01

    def test_lmtd_equal_deltas(self):
        """When ΔT₁ == ΔT₂, LMTD should degenerate to that value."""
        m = _i()
        result = m.lmtd(30.0, 30.0)
        assert abs(result - 30.0) < 0.01
