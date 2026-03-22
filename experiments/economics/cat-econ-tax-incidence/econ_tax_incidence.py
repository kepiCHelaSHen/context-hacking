"""Tax Incidence — CHP Economics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_tax_incidence_constants import (
    ES_TEST, ED_TEST, CONSUMER_SHARE_EXPECTED, PRODUCER_SHARE_EXPECTED,
    TAX_TEST, Q_BEFORE, Q_AFTER, DQ_TEST, DWL_EXPECTED, TAX_REVENUE_EXPECTED,
)


def consumer_burden_share(Es, Ed):
    """Consumer's share of tax burden = Es / (Es + Ed).

    Es: supply elasticity (positive)
    Ed: |demand elasticity| (absolute value, positive)
    Returns fraction [0, 1]. Higher when demand is more inelastic.
    """
    if Es + Ed == 0:
        raise ValueError("Both elasticities cannot be zero")
    return Es / (Es + Ed)


def producer_burden_share(Es, Ed):
    """Producer's share of tax burden = Ed / (Es + Ed).

    Es: supply elasticity (positive)
    Ed: |demand elasticity| (absolute value, positive)
    Returns fraction [0, 1]. Higher when supply is more inelastic.
    """
    if Es + Ed == 0:
        raise ValueError("Both elasticities cannot be zero")
    return Ed / (Es + Ed)


def deadweight_loss(tax, dQ):
    """Deadweight loss (Harberger triangle) = 0.5 * tax * ΔQ.

    tax: per-unit tax amount
    dQ:  reduction in quantity traded (Q_before - Q_after), positive
    Returns the DWL in currency units.
    """
    return 0.5 * tax * dQ


def tax_revenue(tax, Q_after):
    """Tax revenue = tax * Q_after.

    tax:     per-unit tax amount
    Q_after: quantity traded after tax is imposed
    Returns total government revenue from the tax.
    """
    return tax * Q_after


if __name__ == "__main__":
    cs = consumer_burden_share(ES_TEST, ED_TEST)
    ps = producer_burden_share(ES_TEST, ED_TEST)
    print(f"Es = {ES_TEST}, Ed = {ED_TEST}")
    print(f"Consumer burden share: {cs:.2f}  ({cs*100:.0f}%)")
    print(f"Producer burden share: {ps:.2f}  ({ps*100:.0f}%)")
    print(f"Sum: {cs + ps:.2f}")
    print(f"  -> Consumers bear MORE because demand is more INELASTIC")
    print()
    dwl = deadweight_loss(TAX_TEST, DQ_TEST)
    rev = tax_revenue(TAX_TEST, Q_AFTER)
    print(f"Tax = ${TAX_TEST}, Q_before = {Q_BEFORE}, Q_after = {Q_AFTER}")
    print(f"Deadweight loss: ${dwl:.2f}")
    print(f"Tax revenue:     ${rev:.2f}")
