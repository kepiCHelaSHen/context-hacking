"""cat-eng-rlc-resonance — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_rlc_resonance_constants import *
IMPL = Path(__file__).parent.parent / "eng_rlc_resonance.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_q_uses_1_over_r(self):
        """Q for series RLC is (1/R)*sqrt(L/C), NOT R*sqrt(C/L)."""
        m = _i()
        Q = m.q_factor_series(R_ALT, L_REF, C_REF)
        assert abs(Q - Q_ALT_CORRECT) < 1e-9, f"Got {Q}, expected {Q_ALT_CORRECT} (not {Q_ALT_WRONG})"

    def test_bandwidth_is_f0_over_q(self):
        """BW = f0/Q, NOT f0*Q."""
        m = _i()
        BW = m.bandwidth(F0_REF, Q_REF)
        assert abs(BW - BW_REF) < 1e-6

    def test_omega_vs_f(self):
        """omega0 != f0 — off by factor 2*pi."""
        m = _i()
        w0 = m.resonance_freq_rad(L_REF, C_REF)
        f0 = m.resonance_freq_hz(L_REF, C_REF)
        assert abs(w0 / f0 - 2.0 * math.pi) < 1e-6


class TestCorrectness:
    def test_omega0(self):
        m = _i()
        w0 = m.resonance_freq_rad(L_REF, C_REF)
        assert abs(w0 - OMEGA0_REF) < 1e-6

    def test_f0(self):
        m = _i()
        f0 = m.resonance_freq_hz(L_REF, C_REF)
        assert abs(f0 - F0_REF) < 1e-6

    def test_q_ref(self):
        m = _i()
        Q = m.q_factor_series(R_REF, L_REF, C_REF)
        assert abs(Q - Q_REF) < 1e-9

    def test_bandwidth_ref(self):
        m = _i()
        BW = m.bandwidth(F0_REF, Q_REF)
        assert abs(BW - BW_REF) < 1e-6

    def test_impedance_at_resonance(self):
        m = _i()
        Z = m.impedance_at_resonance(R_REF)
        assert Z == R_REF

    def test_bw_alternate_formula(self):
        """BW should also equal R/(2*pi*L)."""
        m = _i()
        f0 = m.resonance_freq_hz(L_REF, C_REF)
        Q = m.q_factor_series(R_REF, L_REF, C_REF)
        BW = m.bandwidth(f0, Q)
        BW_alt = R_REF / (2.0 * math.pi * L_REF)
        assert abs(BW - BW_alt) < 1e-6
