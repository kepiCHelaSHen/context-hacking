"""cat-econ-externality — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_externality_constants import *
IMPL = Path(__file__).parent.parent / "econ_externality.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_msc_includes_mec(self):
        """MSC must equal MPC + MEC, not MPC alone."""
        m = _i()
        mpc_val = A_MPC + B_MPC * 10
        mec_val = B_MEC * 10
        result = m.msc(mpc_val, mec_val)
        assert abs(result - (mpc_val + mec_val)) < 1e-9
        assert result > mpc_val  # MSC > MPC when MEC > 0

    def test_market_overproduces(self):
        """Negative externality => market overproduces (Q_mkt > Q_soc)."""
        m = _i()
        Q_m, _ = m.market_equilibrium(A_MPC, B_MPC, A_MB, B_MB)
        Q_s, _ = m.social_optimum(A_MPC, B_MPC, B_MEC, A_MB, B_MB)
        assert Q_m > Q_s

    def test_tax_at_social_not_market_q(self):
        """Pigouvian tax = MEC at Q_soc, NOT at Q_mkt."""
        m = _i()
        tax = m.pigouvian_tax(B_MEC, Q_SOC)
        tax_wrong = B_MEC * Q_MKT
        assert abs(tax - TAX_PIGOUVIAN) < 1e-9
        assert abs(tax - tax_wrong) > 0.01  # must differ from wrong answer

class TestCorrectness:
    def test_market_equilibrium_Q(self):
        m = _i(); Q, P = m.market_equilibrium(A_MPC, B_MPC, A_MB, B_MB)
        assert abs(Q - Q_MKT) < 1e-9

    def test_market_equilibrium_P(self):
        m = _i(); Q, P = m.market_equilibrium(A_MPC, B_MPC, A_MB, B_MB)
        assert abs(P - P_MKT) < 1e-9

    def test_social_optimum_Q(self):
        m = _i(); Q, P = m.social_optimum(A_MPC, B_MPC, B_MEC, A_MB, B_MB)
        assert abs(Q - Q_SOC) < 1e-9

    def test_social_optimum_P(self):
        m = _i(); Q, P = m.social_optimum(A_MPC, B_MPC, B_MEC, A_MB, B_MB)
        assert abs(P - P_SOC) < 1e-9

    def test_pigouvian_tax_value(self):
        m = _i(); tax = m.pigouvian_tax(B_MEC, Q_SOC)
        assert abs(tax - TAX_PIGOUVIAN) < 1e-9

    def test_deadweight_loss(self):
        m = _i(); dwl = m.deadweight_loss(A_MPC, B_MPC, B_MEC, A_MB, B_MB)
        assert abs(dwl - DWL) < 1e-9
