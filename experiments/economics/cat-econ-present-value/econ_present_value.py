"""
Present Value (NPV, IRR, Annuities) -- CHP Economics Sprint
Time value of money: discrete vs continuous compounding, NPV, annuities.
All constants from frozen spec.
"""
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_present_value_constants import (
    TEST_FV, TEST_RATE, TEST_N, TEST_PMT,
    DISCRETE_PV, CONTINUOUS_PV, ANNUITY_PV, PERPETUITY_PV,
    NPV_EXPECTED, TEST_CASHFLOWS,
)


def pv_discrete(FV, r, n):
    """Present value with DISCRETE compounding: PV = FV / (1+r)^n.
    NOT e^(-rn) -- that is the continuous formula."""
    return FV / (1 + r) ** n


def pv_continuous(FV, r, n):
    """Present value with CONTINUOUS compounding: PV = FV * e^(-rn).
    NOT 1/(1+r)^n -- that is the discrete formula."""
    return FV * math.exp(-r * n)


def npv(cashflows, r):
    """Net present value: NPV = sum( CF_t / (1+r)^t ) for t=0..T.
    cashflows[0] is C0 (typically negative = initial outlay).
    Does NOT omit the t=0 term -- C0 is included at face value (discounted by 1)."""
    return sum(cf / (1 + r) ** t for t, cf in enumerate(cashflows))


def annuity_pv(PMT, r, n):
    """Present value of ordinary annuity: PMT * [1 - (1+r)^(-n)] / r.
    NOT PMT/r -- that is the PERPETUITY formula (n -> infinity)."""
    return PMT * (1 - (1 + r) ** (-n)) / r


def perpetuity_pv(PMT, r):
    """Present value of perpetuity: PMT / r.
    Only valid when payments continue forever (n -> infinity)."""
    return PMT / r


if __name__ == "__main__":
    print("=== Present Value: Time Value of Money ===\n")

    # Discrete vs continuous
    d_pv = pv_discrete(TEST_FV, TEST_RATE, TEST_N)
    c_pv = pv_continuous(TEST_FV, TEST_RATE, TEST_N)
    print(f"FV={TEST_FV}, r={TEST_RATE}, n={TEST_N}")
    print(f"  Discrete  PV = {d_pv:.2f}  (expected {DISCRETE_PV:.2f})")
    print(f"  Continuous PV = {c_pv:.2f}  (expected {CONTINUOUS_PV:.2f})")
    print(f"  Difference    = {d_pv - c_pv:.2f}  ({(d_pv - c_pv)/d_pv*100:.1f}%)")
    print(f"  KEY: e^(-rn) != 1/(1+r)^n for same r!\n")

    # NPV
    npv_val = npv(TEST_CASHFLOWS, TEST_RATE)
    print(f"NPV of {TEST_CASHFLOWS} at r={TEST_RATE}:")
    print(f"  NPV = {npv_val:.2f}  (expected {NPV_EXPECTED:.2f})\n")

    # Annuity vs perpetuity
    ann_pv = annuity_pv(TEST_PMT, TEST_RATE, TEST_N)
    perp_pv = perpetuity_pv(TEST_PMT, TEST_RATE)
    print(f"PMT={TEST_PMT}, r={TEST_RATE}, n={TEST_N}")
    print(f"  Annuity PV   = {ann_pv:.2f}  (expected {ANNUITY_PV:.2f})")
    print(f"  Perpetuity PV = {perp_pv:.2f}  (expected {PERPETUITY_PV:.2f})")
    print(f"  Annuity < Perpetuity: {ann_pv < perp_pv}")
