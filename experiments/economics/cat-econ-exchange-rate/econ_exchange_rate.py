"""
Exchange Rate Determination — CHP Economics Sprint
PPP, Relative PPP, Uncovered Interest Rate Parity, Real Exchange Rate.
All constants from frozen spec.

Convention: exchange rate E = domestic currency per unit of foreign currency
(e.g. $/£).  Higher E = domestic currency weaker (depreciates).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_exchange_rate_constants import (
    P_US, P_UK, PPP_RATE_USD_PER_GBP,
    INFLATION_US, INFLATION_UK, EXPECTED_PCT_CHANGE, EXPECTED_NEXT_E,
    I_US, I_UK, IRP_EXPECTED_CHANGE,
)


def ppp_rate(P_domestic, P_foreign):
    """Absolute PPP: E = P_domestic / P_foreign.
    NOT P_foreign/P_domestic (common LLM error).
    Higher domestic prices -> higher E -> domestic currency weaker.
    """
    return P_domestic / P_foreign


def relative_ppp(inflation_dom, inflation_for):
    """Relative PPP: expected %ΔE ≈ π_domestic - π_foreign.
    Positive result = domestic currency DEPRECIATES (E rises).
    NOT inflation_for - inflation_dom (that would give wrong sign).
    """
    return inflation_dom - inflation_for


def expected_exchange_rate(E_current, pct_change):
    """Expected future exchange rate given current rate and expected % change.
    E_next = E_current * (1 + pct_change).
    pct_change > 0 means domestic currency depreciates.
    """
    return E_current * (1.0 + pct_change)


def real_exchange_rate(E, P_foreign, P_domestic):
    """Real exchange rate: q = E * P_foreign / P_domestic.
    E is nominal rate (domestic/foreign units).
    q = 1 when PPP holds exactly.
    q > 1: foreign goods more expensive in domestic terms (domestic undervalued).
    q < 1: foreign goods cheaper (domestic overvalued).
    """
    return E * P_foreign / P_domestic


def irp_expected_change(i_dom, i_for):
    """Uncovered Interest Rate Parity: expected %ΔE = (1+i_d)/(1+i_f) - 1.
    Higher domestic interest rate -> EXPECTED DEPRECIATION (positive return).
    NOT appreciation — that is the common LLM error.
    """
    return (1.0 + i_dom) / (1.0 + i_for) - 1.0


if __name__ == "__main__":
    print("=== Exchange Rate Determination ===\n")

    # Absolute PPP
    E = ppp_rate(P_US, P_UK)
    print(f"PPP rate (P_US={P_US}, P_UK={P_UK}): {E:.2f} $/£")
    print(f"  Expected: {PPP_RATE_USD_PER_GBP}")

    # Relative PPP
    pct = relative_ppp(INFLATION_US, INFLATION_UK)
    print(f"\nRelative PPP (pi_US={INFLATION_US}, pi_UK={INFLATION_UK}): {pct:.4f}")
    print(f"  Expected: {EXPECTED_PCT_CHANGE} ($ depreciates)")

    # Expected next-period rate
    E_next = expected_exchange_rate(E, pct)
    print(f"\nExpected next E: {E_next:.4f} $/£")
    print(f"  Expected: {EXPECTED_NEXT_E}")

    # Real exchange rate
    q = real_exchange_rate(E, P_UK, P_US)
    print(f"\nReal exchange rate: {q:.4f}")
    print(f"  Expected: 1.0 (PPP holds)")

    # Interest Rate Parity
    irp = irp_expected_change(I_US, I_UK)
    print(f"\nIRP expected pct_dE (i_US={I_US}, i_UK={I_UK}): {irp:.6f}")
    print(f"  Expected: {IRP_EXPECTED_CHANGE:.6f} ($ expected to depreciate)")
