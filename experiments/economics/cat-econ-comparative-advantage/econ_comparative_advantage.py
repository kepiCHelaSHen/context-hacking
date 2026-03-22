"""Ricardo's Comparative Advantage — CHP Economics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_comparative_advantage_constants import (
    A_HOURS_WINE, A_HOURS_CLOTH, B_HOURS_WINE, B_HOURS_CLOTH,
)


def opportunity_cost(hours_good_x, hours_good_y):
    """Opportunity cost of producing one unit of good X, measured in units of good Y forgone.

    OC(X) = hours_X / hours_Y
    """
    return hours_good_x / hours_good_y


def has_comparative_advantage(oc_a, oc_b):
    """Return True if country A has comparative advantage (lower OC) in the good."""
    return oc_a < oc_b


def gains_from_trade(oc_a, oc_b):
    """Return True if both countries gain from trade (OCs differ → specialisation pays)."""
    return oc_a != oc_b


def terms_of_trade_range(oc_a_wine, oc_b_wine):
    """Return (min, max) cloth-per-wine for mutually beneficial trade.

    The range lies between the two countries' opportunity costs of wine.
    Below min, the low-OC country won't export; above max, the other won't import.
    """
    return (min(oc_a_wine, oc_b_wine), max(oc_a_wine, oc_b_wine))


if __name__ == "__main__":
    oc_a_wine  = opportunity_cost(A_HOURS_WINE,  A_HOURS_CLOTH)
    oc_a_cloth = opportunity_cost(A_HOURS_CLOTH, A_HOURS_WINE)
    oc_b_wine  = opportunity_cost(B_HOURS_WINE,  B_HOURS_CLOTH)
    oc_b_cloth = opportunity_cost(B_HOURS_CLOTH, B_HOURS_WINE)

    print(f"OC(A, wine) = {oc_a_wine:.4f} cloth  |  OC(A, cloth) = {oc_a_cloth:.4f} wine")
    print(f"OC(B, wine) = {oc_b_wine:.4f} cloth  |  OC(B, cloth) = {oc_b_cloth:.4f} wine")
    print(f"A comp. adv. in cloth? {has_comparative_advantage(oc_a_cloth, oc_b_cloth)}")
    print(f"B comp. adv. in wine?  {has_comparative_advantage(oc_b_wine, oc_a_wine)}")
    print(f"Gains from trade?      {gains_from_trade(oc_a_wine, oc_b_wine)}")
    lo, hi = terms_of_trade_range(oc_a_wine, oc_b_wine)
    print(f"Terms of trade (wine): {lo:.4f} – {hi:.4f} cloth per wine")
