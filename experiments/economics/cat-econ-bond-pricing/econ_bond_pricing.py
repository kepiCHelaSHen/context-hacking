"""
Bond Pricing (YTM, Duration, Convexity) — CHP Economics Sprint
Semi-annual coupon bonds, yield to maturity, Macaulay duration.
All constants from frozen spec.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_bond_pricing_constants import (
    FACE_VALUE, COUPON_RATE, YTM, YEARS, M,
    COUPON_PER_PERIOD, NUM_PERIODS, YIELD_PER_PERIOD,
    BOND_PRICE_SEMI, MACAULAY_DURATION_YEARS, CURRENT_YIELD,
)


def coupon_per_period(FV, coupon_rate, m):
    """
    Coupon payment per period.

    Parameters
    ----------
    FV : float          Face (par) value
    coupon_rate : float  Annual coupon rate (e.g. 0.06 for 6%)
    m : int             Payments per year (2 for semi-annual)

    Returns
    -------
    float  Coupon payment each period = FV * coupon_rate / m
    """
    return FV * coupon_rate / m


def bond_price(FV, coupon_rate, ytm, years, m=2):
    """
    Price of a fixed-rate bond.

    P = C * [(1 - (1+y)^(-n)) / y] + FV / (1+y)^n

    where C = FV * coupon_rate / m, y = ytm / m, n = years * m.

    US bonds default to semi-annual coupons (m=2).

    Parameters
    ----------
    FV : float          Face value
    coupon_rate : float  Annual coupon rate
    ytm : float         Annual yield to maturity
    years : int/float   Years to maturity
    m : int             Coupon payments per year (default 2 = semi-annual)

    Returns
    -------
    float  Bond price (present value of all cash flows)
    """
    C = FV * coupon_rate / m       # coupon per period
    y = ytm / m                    # yield per period
    n = int(years * m)             # total number of periods

    if y == 0:
        # Special case: zero yield => no discounting
        return C * n + FV

    pv_coupons = C * (1 - (1 + y) ** (-n)) / y
    pv_face = FV / (1 + y) ** n
    return pv_coupons + pv_face


def macaulay_duration(FV, coupon_rate, ytm, years, m=2):
    """
    Macaulay duration in YEARS.

    D = (1/P) * sum_{t=1..n} [ t * CF_t / (1+y)^t ] / m

    Cash flows MUST be discounted — omitting the (1+y)^t denominator
    is a common error.

    Parameters
    ----------
    FV : float          Face value
    coupon_rate : float  Annual coupon rate
    ytm : float         Annual yield to maturity
    years : int/float   Years to maturity
    m : int             Coupon payments per year (default 2)

    Returns
    -------
    float  Macaulay duration in years
    """
    C = FV * coupon_rate / m
    y = ytm / m
    n = int(years * m)
    P = bond_price(FV, coupon_rate, ytm, years, m)

    weighted_sum = 0.0
    for t in range(1, n + 1):
        cf = C if t < n else C + FV
        weighted_sum += t * cf / (1 + y) ** t

    return (weighted_sum / P) / m


def current_yield(FV, coupon_rate, price):
    """
    Current yield = annual coupon / market price.

    Parameters
    ----------
    FV : float          Face value
    coupon_rate : float  Annual coupon rate
    price : float       Current market price

    Returns
    -------
    float  Current yield as a decimal (e.g. 0.0653)
    """
    return (FV * coupon_rate) / price


if __name__ == "__main__":
    print("=== Bond Pricing ===\n")

    fv, cr, y_, yrs, m_ = FACE_VALUE, COUPON_RATE, YTM, YEARS, M

    cpp = coupon_per_period(fv, cr, m_)
    print(f"Face value = {fv},  Coupon rate = {cr*100:.1f}%,  YTM = {y_*100:.1f}%")
    print(f"Maturity = {yrs} years,  Payments/year = {m_}")
    print(f"Coupon per period = {cpp:.2f}  (frozen: {COUPON_PER_PERIOD})")
    print()

    P = bond_price(fv, cr, y_, yrs, m_)
    print(f"Bond price (semi-annual) = {P:.4f}  (frozen: {BOND_PRICE_SEMI})")

    P_annual = bond_price(fv, cr, y_, yrs, m=1)
    print(f"Bond price (annual, WRONG for US) = {P_annual:.4f}")
    print()

    dur = macaulay_duration(fv, cr, y_, yrs, m_)
    print(f"Macaulay duration = {dur:.4f} years  (frozen: {MACAULAY_DURATION_YEARS})")
    print()

    cy = current_yield(fv, cr, P)
    print(f"Current yield = {cy:.6f}  (frozen: {CURRENT_YIELD})")
