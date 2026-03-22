"""Consumer / Producer Surplus — Frozen Constants. Source: Mankiw Principles of Economics, Ch 7. DO NOT MODIFY."""
# Consumer Surplus  = area above P* and below demand curve
#   CS = integral from 0 to Q* of (P_demand(Q) - P*) dQ
#   For linear demand Qd = a - bP  =>  P = (a - Q) / b
#   CS = (1/2) * (P_max - P*) * Q*
# Producer Surplus  = area below P* and above supply curve
#   PS = integral from 0 to Q* of (P* - P_supply(Q)) dQ
#   For linear supply Qs = c + dP  =>  P = (Q - c) / d
#   PS = (1/2) * (P* - P_min) * Q*
# Total Surplus = CS + PS

# Test: Demand Qd = 100 - 2P,  Supply Qs = -20 + 3P
# Equilibrium: 100 - 2P = -20 + 3P  =>  5P = 120  =>  P* = 24,  Q* = 52
A_DEMAND = 100          # Qd = a - bP
B_DEMAND = 2
C_SUPPLY = -20          # Qs = c + dP
D_SUPPLY = 3

P_EQ = 24.0
Q_EQ = 52.0

# Demand intercept: P when Q=0 => P_max = a/b = 100/2 = 50
P_MAX = A_DEMAND / B_DEMAND                     # 50.0

# Supply intercept: P when Q=0 => P_min = -c/d = 20/3 = 6.6667
P_MIN = -C_SUPPLY / D_SUPPLY                    # 6.6667

# CS = 0.5 * (P_max - P*) * Q* = 0.5 * (50 - 24) * 52 = 676
CS_EXPECTED = 0.5 * (P_MAX - P_EQ) * Q_EQ       # 676.0

# PS = 0.5 * (P* - P_min) * Q* = 0.5 * (24 - 6.6667) * 52 = 450.6667
PS_EXPECTED = 0.5 * (P_EQ - P_MIN) * Q_EQ       # 450.6667

# Total = CS + PS = 1126.6667
TOTAL_SURPLUS_EXPECTED = CS_EXPECTED + PS_EXPECTED  # 1126.6667

PRIOR_ERRORS = {
    "cs_total_area":      "Computes total area under demand curve instead of area above P*",
    "ps_wrong_base":      "Uses 0 as minimum price instead of supply intercept P_min",
    "surplus_from_quantity": "Integrates with respect to the wrong variable",
}
