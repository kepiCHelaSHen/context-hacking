"""Compound Interest — APR vs EAR — CHP Economics Sprint."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_compound_interest_constants import *


def ear_from_apr(apr, m):
    """Effective Annual Rate from nominal APR with m compounding periods.

    EAR = (1 + APR/m)^m - 1
    """
    return (1 + apr / m) ** m - 1


def ear_continuous(apr):
    """Effective Annual Rate under continuous compounding.

    EAR = e^APR - 1
    """
    return math.exp(apr) - 1


def compound_amount(P, apr, m, years):
    """Future value of principal P at nominal APR compounded m times/year.

    FV = P * (1 + APR/m)^(m * years)
    """
    return P * (1 + apr / m) ** (m * years)


def rule_of_72(rate_pct):
    """Approximate doubling time in years using the Rule of 72.

    T_double ≈ 72 / rate_pct   (rate_pct is the rate in percent, e.g. 12)
    """
    return 72.0 / rate_pct


def exact_doubling_time(rate):
    """Exact doubling time in years.

    T_double = ln(2) / ln(1 + rate)   (rate as decimal, e.g. 0.12)
    """
    return math.log(2) / math.log(1 + rate)


if __name__ == "__main__":
    print("=== Compound Interest: APR vs EAR ===\n")

    ear = ear_from_apr(APR, M)
    ear_cont = ear_continuous(APR)
    fv = compound_amount(P_PRINCIPAL, APR, M, T_YEARS)
    r72 = rule_of_72(RATE_PCT)
    exact_dt = exact_doubling_time(APR)

    print(f"APR = {APR:.2%}, compounding periods m = {M}")
    print(f"EAR (discrete)   = {ear:.5%}  (expected {EAR_EXPECTED:.5%})")
    print(f"EAR (continuous) = {ear_cont:.5%}  (expected {EAR_CONTINUOUS_EXPECTED:.5%})")
    print(f"WRONG (APR=EAR)  = {APR:.5%}  (underestimates by {ear - APR:.3%})")
    print()
    print(f"FV of ${P_PRINCIPAL:,.0f} after {T_YEARS} years = ${fv:,.4f}"
          f"  (expected ${COMPOUND_AMOUNT_EXPECTED:,.4f})")
    print()
    print(f"Rule of 72 approx doubling time = {r72:.2f} years")
    print(f"Exact doubling time              = {exact_dt:.5f} years")
    print(f"Rule of 72 error                 = {r72 - exact_dt:.5f} years")
