"""econ-supply-demand — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_supply_demand_constants import *

IMPL = Path(__file__).parent.parent / "econ_supply_demand.py"


def _i():
    if not IMPL.exists():
        pytest.skip("implementation not yet written")
    import importlib.util
    spec = importlib.util.spec_from_file_location("impl", IMPL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestPriorErrors:
    """Each test catches one known LLM prior error."""

    def test_supply_shift_right_lowers_price(self):
        """PRIOR: supply_shift_price_up — LLM claims supply increase raises price."""
        mod = _i()
        fx = mod.supply_shift_effect("right")
        assert fx["price"] == "decrease", "Supply increase should LOWER price"

    def test_equilibrium_formula_correct(self):
        """PRIOR: equilibrium_formula_wrong — LLM uses (a+c)/(b-d) not (a-c)/(b+d)."""
        mod = _i()
        P = mod.equilibrium_price(DEMAND_A, DEMAND_B, SUPPLY_C, SUPPLY_D)
        assert abs(P - EQUILIBRIUM_PRICE) < 1e-9, (
            f"P*={P}, expected {EQUILIBRIUM_PRICE}: must be (a-c)/(b+d)"
        )

    def test_demand_slope_negative(self):
        """PRIOR: slope_sign_wrong — demand must slope downward (Qd = a - bP, b > 0)."""
        mod = _i()
        Q_at_10 = mod.demand(DEMAND_A, DEMAND_B, 10)
        Q_at_20 = mod.demand(DEMAND_A, DEMAND_B, 20)
        assert Q_at_20 < Q_at_10, "Demand must decrease as price rises"


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_equilibrium_price(self):
        mod = _i()
        P = mod.equilibrium_price(DEMAND_A, DEMAND_B, SUPPLY_C, SUPPLY_D)
        assert abs(P - EQUILIBRIUM_PRICE) < 1e-9

    def test_equilibrium_quantity(self):
        mod = _i()
        P = mod.equilibrium_price(DEMAND_A, DEMAND_B, SUPPLY_C, SUPPLY_D)
        Q = mod.equilibrium_quantity(DEMAND_A, DEMAND_B, P)
        assert abs(Q - EQUILIBRIUM_QUANTITY) < 1e-9

    def test_equilibrium_quantity_alt(self):
        """Q* from both demand and supply sides must agree."""
        mod = _i()
        P = mod.equilibrium_price(DEMAND_A, DEMAND_B, SUPPLY_C, SUPPLY_D)
        Q_demand = mod.demand(DEMAND_A, DEMAND_B, P)
        Q_supply = mod.supply(SUPPLY_C, SUPPLY_D, P)
        assert abs(Q_demand - Q_supply) < 1e-9
        assert abs(Q_demand - EQUILIBRIUM_Q_ALT) < 1e-9

    def test_demand_at_zero_price(self):
        mod = _i()
        Q = mod.demand(DEMAND_A, DEMAND_B, 0)
        assert abs(Q - DEMAND_A) < 1e-9

    def test_supply_at_zero_price(self):
        mod = _i()
        Q = mod.supply(SUPPLY_C, SUPPLY_D, 0)
        assert abs(Q - SUPPLY_C) < 1e-9

    def test_supply_shift_left_raises_price(self):
        mod = _i()
        fx = mod.supply_shift_effect("left")
        assert fx["price"] == "increase"
        assert fx["quantity"] == "decrease"

    def test_supply_shift_right_increases_quantity(self):
        mod = _i()
        fx = mod.supply_shift_effect("right")
        assert fx["quantity"] == "increase"

    def test_supply_shift_invalid_raises(self):
        mod = _i()
        with pytest.raises(ValueError):
            mod.supply_shift_effect("up")
