"""
Supply and Demand Equilibrium — CHP Economics Sprint
Linear supply/demand, equilibrium price/quantity, shift effects.
All constants from frozen spec.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_supply_demand_constants import (
    DEMAND_A, DEMAND_B, SUPPLY_C, SUPPLY_D,
    EQUILIBRIUM_PRICE, EQUILIBRIUM_QUANTITY,
)


def demand(a, b, P):
    """Quantity demanded: Qd = a - b*P (downward sloping, b > 0)."""
    return a - b * P


def supply(c, d, P):
    """Quantity supplied: Qs = c + d*P (upward sloping, d > 0)."""
    return c + d * P


def equilibrium_price(a, b, c, d):
    """Equilibrium price: P* = (a - c) / (b + d)."""
    return (a - c) / (b + d)


def equilibrium_quantity(a, b, P_eq):
    """Equilibrium quantity from demand side: Q* = a - b*P*."""
    return a - b * P_eq


def supply_shift_effect(direction):
    """
    Return dict describing price and quantity changes when supply shifts.

    Parameters
    ----------
    direction : str
        "right" (supply increases) or "left" (supply decreases)

    Returns
    -------
    dict with keys "price" and "quantity", values "increase" or "decrease"
    """
    if direction == "right":
        # More supply => price falls, quantity rises
        return {"price": "decrease", "quantity": "increase"}
    elif direction == "left":
        # Less supply => price rises, quantity falls
        return {"price": "increase", "quantity": "decrease"}
    else:
        raise ValueError(f"direction must be 'right' or 'left', got {direction!r}")


if __name__ == "__main__":
    print("=== Supply and Demand Equilibrium ===\n")

    a, b, c, d = DEMAND_A, DEMAND_B, SUPPLY_C, SUPPLY_D

    P_star = equilibrium_price(a, b, c, d)
    Q_star = equilibrium_quantity(a, b, P_star)

    print(f"Demand: Qd = {a} - {b}P")
    print(f"Supply: Qs = {c} + {d}P")
    print(f"Equilibrium price  P* = {P_star:.2f}  (frozen: {EQUILIBRIUM_PRICE})")
    print(f"Equilibrium quantity Q* = {Q_star:.2f}  (frozen: {EQUILIBRIUM_QUANTITY})")
    print()

    # Verify from supply side
    Q_star_supply = supply(c, d, P_star)
    print(f"Q* from supply side = {Q_star_supply:.2f}  (should match)")
    print()

    # Shift effects
    for dir_ in ("right", "left"):
        fx = supply_shift_effect(dir_)
        print(f"Supply shift {dir_}: price {fx['price']}, quantity {fx['quantity']}")
