"""cat-econ-tax-incidence — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_tax_incidence_constants import *
IMPL = Path(__file__).parent.parent / "econ_tax_incidence.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Tests that specifically catch known LLM errors."""

    def test_inelastic_side_bears_more(self):
        """PRIOR: seller_bears_all — burden depends on elasticity, not on who is taxed."""
        m = _i()
        # Ed=0.5 (inelastic demand), Es=2.0 (elastic supply)
        # Consumers should bear MORE (80%), not producers
        cs = m.consumer_burden_share(ES_TEST, ED_TEST)
        ps = m.producer_burden_share(ES_TEST, ED_TEST)
        assert cs > ps, f"Consumers should bear more when demand is inelastic: cs={cs}, ps={ps}"

    def test_more_inelastic_not_more_elastic(self):
        """PRIOR: more_elastic_bears_more — more INELASTIC bears more, not more elastic."""
        m = _i()
        # When supply is more elastic than demand, consumers (the inelastic side) bear more
        cs = m.consumer_burden_share(2.0, 0.5)
        assert cs > 0.5, f"More inelastic side (demand) should bear >50%, got {cs:.2f}"
        # Flip: when demand is more elastic than supply, producers bear more
        ps = m.producer_burden_share(0.5, 2.0)
        assert ps > 0.5, f"More inelastic side (supply) should bear >50%, got {ps:.2f}"

    def test_dwl_is_positive(self):
        """PRIOR: no_dwl — taxes DO create deadweight loss."""
        m = _i()
        dwl = m.deadweight_loss(TAX_TEST, DQ_TEST)
        assert dwl > 0, f"Deadweight loss must be positive, got {dwl}"


class TestCorrectness:
    """Numerical verification against frozen constants."""

    def test_consumer_share_value(self):
        m = _i()
        cs = m.consumer_burden_share(ES_TEST, ED_TEST)
        assert abs(cs - CONSUMER_SHARE_EXPECTED) < 1e-9, f"Expected {CONSUMER_SHARE_EXPECTED}, got {cs}"

    def test_producer_share_value(self):
        m = _i()
        ps = m.producer_burden_share(ES_TEST, ED_TEST)
        assert abs(ps - PRODUCER_SHARE_EXPECTED) < 1e-9, f"Expected {PRODUCER_SHARE_EXPECTED}, got {ps}"

    def test_shares_sum_to_one(self):
        m = _i()
        cs = m.consumer_burden_share(ES_TEST, ED_TEST)
        ps = m.producer_burden_share(ES_TEST, ED_TEST)
        assert abs((cs + ps) - 1.0) < 1e-12, f"Shares must sum to 1, got {cs + ps}"

    def test_dwl_value(self):
        m = _i()
        dwl = m.deadweight_loss(TAX_TEST, DQ_TEST)
        assert abs(dwl - DWL_EXPECTED) < 1e-9, f"Expected {DWL_EXPECTED}, got {dwl}"

    def test_tax_revenue_value(self):
        m = _i()
        rev = m.tax_revenue(TAX_TEST, Q_AFTER)
        assert abs(rev - TAX_REVENUE_EXPECTED) < 1e-9, f"Expected {TAX_REVENUE_EXPECTED}, got {rev}"

    def test_perfectly_inelastic_demand(self):
        """Ed=0 → consumers bear 100%."""
        m = _i()
        cs = m.consumer_burden_share(2.0, 0.0)
        assert abs(cs - 1.0) < 1e-12, f"Perfectly inelastic demand: consumers should bear 100%, got {cs}"

    def test_perfectly_inelastic_supply(self):
        """Es=0 → producers bear 100%."""
        m = _i()
        ps = m.producer_burden_share(0.0, 2.0)
        assert abs(ps - 1.0) < 1e-12, f"Perfectly inelastic supply: producers should bear 100%, got {ps}"

    def test_equal_elasticity_50_50(self):
        """Es=Ed → 50/50 split."""
        m = _i()
        cs = m.consumer_burden_share(1.0, 1.0)
        ps = m.producer_burden_share(1.0, 1.0)
        assert abs(cs - 0.5) < 1e-12, f"Equal elasticity should give 50/50, got cs={cs}"
        assert abs(ps - 0.5) < 1e-12, f"Equal elasticity should give 50/50, got ps={ps}"

    def test_dwl_zero_when_no_quantity_change(self):
        """No quantity reduction → no DWL."""
        m = _i()
        dwl = m.deadweight_loss(5.0, 0.0)
        assert abs(dwl) < 1e-12, f"DWL should be zero when dQ=0, got {dwl}"
