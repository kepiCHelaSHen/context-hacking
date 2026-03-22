"""Consumer / Producer Surplus — CHP Economics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_consumer_surplus_constants import *


def demand_intercept_price(a, b):
    """P when Q=0 on demand curve Qd = a - bP  =>  P_max = a / b."""
    return a / b


def supply_intercept_price(c, d):
    """P when Q=0 on supply curve Qs = c + dP  =>  P_min = -c / d."""
    return -c / d


def consumer_surplus_linear(P_max, P_eq, Q_eq):
    """CS = area above P* and below demand curve = (1/2)(P_max - P*)*Q*."""
    return 0.5 * (P_max - P_eq) * Q_eq


def producer_surplus_linear(P_min, P_eq, Q_eq):
    """PS = area below P* and above supply curve = (1/2)(P* - P_min)*Q*."""
    return 0.5 * (P_eq - P_min) * Q_eq


def total_surplus(cs, ps):
    """Total surplus = CS + PS."""
    return cs + ps


if __name__ == "__main__":
    p_max = demand_intercept_price(A_DEMAND, B_DEMAND)
    p_min = supply_intercept_price(C_SUPPLY, D_SUPPLY)
    cs = consumer_surplus_linear(p_max, P_EQ, Q_EQ)
    ps = producer_surplus_linear(p_min, P_EQ, Q_EQ)
    ts = total_surplus(cs, ps)
    print(f"P*={P_EQ}, Q*={Q_EQ}")
    print(f"P_max={p_max}, P_min={p_min:.4f}")
    print(f"CS={cs:.4f}, PS={ps:.4f}, Total={ts:.4f}")
