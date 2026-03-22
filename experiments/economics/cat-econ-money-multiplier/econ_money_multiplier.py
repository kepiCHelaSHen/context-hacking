"""Money Multiplier — CHP Economics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_money_multiplier_constants import (
    RR, CR, MB, INITIAL_DEPOSIT,
    SIMPLE_MULTIPLIER, EXTENDED_MULTIPLIER,
    TOTAL_DEPOSITS, TOTAL_RESERVES,
    MONEY_SUPPLY_SIMPLE, MONEY_SUPPLY_EXTENDED,
)


def simple_multiplier(rr):
    """Simple money multiplier: m = 1/rr. NOT 1/(1-rr)!"""
    if rr <= 0 or rr > 1:
        raise ValueError(f"Reserve ratio must be in (0, 1], got {rr}")
    return 1.0 / rr


def extended_multiplier(rr, cr):
    """Extended multiplier with currency drain: m = (1+cr)/(rr+cr)."""
    if rr <= 0 or rr > 1:
        raise ValueError(f"Reserve ratio must be in (0, 1], got {rr}")
    if cr < 0:
        raise ValueError(f"Currency/deposit ratio must be >= 0, got {cr}")
    return (1.0 + cr) / (rr + cr)


def money_supply(monetary_base, multiplier):
    """Money supply M = MB × m."""
    return monetary_base * multiplier


def total_deposits(initial_deposit, rr):
    """Total deposits from geometric series: D₀/rr."""
    if rr <= 0 or rr > 1:
        raise ValueError(f"Reserve ratio must be in (0, 1], got {rr}")
    return initial_deposit / rr


def total_reserves(total_dep, rr):
    """Total reserves = total deposits × rr."""
    return total_dep * rr


if __name__ == "__main__":
    m_simple = simple_multiplier(RR)
    print(f"Simple multiplier (rr={RR}): {m_simple:.1f}  <-- 1/rr, NOT 1/(1-rr)")
    print(f"  Wrong formula 1/(1-rr) would give: {1/(1-RR):.4f}")
    print()

    m_ext = extended_multiplier(RR, CR)
    print(f"Extended multiplier (rr={RR}, cr={CR}): {m_ext:.1f}")
    print(f"  Formula: (1+{CR})/({RR}+{CR}) = {1+CR}/{RR+CR} = {m_ext:.1f}")
    print()

    td = total_deposits(INITIAL_DEPOSIT, RR)
    tr = total_reserves(td, RR)
    print(f"${ INITIAL_DEPOSIT:.0f} initial deposit -> ${td:.0f} total deposits")
    print(f"Total reserves: ${tr:.0f} (equals initial deposit)")
    print()

    ms_simple = money_supply(MB, m_simple)
    ms_ext = money_supply(MB, m_ext)
    print(f"Money supply (MB=${MB:.0f}):")
    print(f"  Simple:   ${ms_simple:.0f}")
    print(f"  Extended: ${ms_ext:.0f}")
