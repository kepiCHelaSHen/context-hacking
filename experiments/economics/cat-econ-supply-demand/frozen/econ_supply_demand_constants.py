"""
Supply and Demand Equilibrium — Frozen Constants
Source: Mankiw Principles of Economics 9th Ed Ch4, Varian Microeconomic Analysis 3rd Ed Ch1
DO NOT MODIFY.
"""

# Linear demand: Qd = a - b*P  (downward sloping, b > 0)
# Linear supply:  Qs = c + d*P  (upward sloping,  d > 0)

# Test case: Qd = 100 - 2P,  Qs = -20 + 3P
DEMAND_A = 100     # intercept (max quantity demanded at P=0)
DEMAND_B = 2       # slope magnitude (positive, demand slopes down)
SUPPLY_C = -20     # intercept
SUPPLY_D = 3       # slope magnitude (positive, supply slopes up)

# Equilibrium: Qd = Qs  =>  a - bP = c + dP  =>  P* = (a - c) / (b + d)
# P* = (100 - (-20)) / (2 + 3) = 120 / 5 = 24
# Q* = a - b*P* = 100 - 2*24 = 52  (or Q* = c + d*P* = -20 + 3*24 = 52)
EQUILIBRIUM_PRICE    = 24.0
EQUILIBRIUM_QUANTITY = 52.0

# Alternative derivation: Q* = (a*d + b*c) / (b + d)
# Q* = (100*3 + 2*(-20)) / (2 + 3) = (300 - 40) / 5 = 260 / 5 = 52
EQUILIBRIUM_Q_ALT = 52.0

# Shift effects (correct directions):
# Supply shift RIGHT (increase supply): P decreases, Q increases
# Supply shift LEFT  (decrease supply): P increases, Q decreases
# Demand shift RIGHT (increase demand): P increases, Q increases
# Demand shift LEFT  (decrease demand): P decreases, Q decreases
SUPPLY_SHIFT_RIGHT_PRICE  = "decrease"
SUPPLY_SHIFT_RIGHT_QTY    = "increase"
DEMAND_SHIFT_RIGHT_PRICE  = "increase"
DEMAND_SHIFT_RIGHT_QTY    = "increase"

PRIOR_ERRORS = {
    "supply_shift_price_up":    "LLM claims supply increase raises price (actually lowers it)",
    "equilibrium_formula_wrong": "LLM uses P* = (a+c)/(b-d) instead of (a-c)/(b+d)",
    "slope_sign_wrong":         "LLM gives demand a positive slope (should be negative: Qd = a - bP)",
}
