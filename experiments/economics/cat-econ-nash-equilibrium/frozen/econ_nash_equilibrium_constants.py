"""
Nash Equilibrium — 2×2 Game Solutions — Frozen Constants
Source: Osborne Introduction to Game Theory Ch4-5, Gibbons Game Theory Ch1
DO NOT MODIFY.
"""

# ── Payoff matrix format ──────────────────────────────────────────────
# payoff_matrix[row][col] = (P1_payoff, P2_payoff)
# Row player = Player 1, Column player = Player 2
# Strategies indexed: 0 = first strategy, 1 = second strategy

# ── Prisoner's Dilemma ────────────────────────────────────────────────
# Strategies: 0 = Cooperate, 1 = Defect
#        P2: C        P2: D
# P1: C  (-1,-1)      (-3, 0)
# P1: D  ( 0,-3)      (-2,-2)
PD_MATRIX = [[(-1, -1), (-3, 0)],
             [( 0, -3), (-2, -2)]]

# Dominant strategy: Defect dominates Cooperate for both players
#   P1: if P2=C, D gives 0 > -1 (C); if P2=D, D gives -2 > -3 (C)
#   P2: symmetric
# Unique pure NE: (Defect, Defect) = strategy pair (1, 1)
PD_PURE_NE = [(1, 1)]
PD_NE_PAYOFFS = (-2, -2)

# No mixed strategy NE (dominant strategy => unique pure NE)
PD_HAS_MIXED_NE = False

# ── Battle of the Sexes ──────────────────────────────────────────────
# Strategies: 0 = Opera, 1 = Fight
#          P2: Opera   P2: Fight
# P1: Opera  (3, 2)     (0, 0)
# P1: Fight  (0, 0)     (2, 3)
BOS_MATRIX = [[(3, 2), (0, 0)],
              [(0, 0), (2, 3)]]

# Two pure NE: (Opera, Opera) and (Fight, Fight)
BOS_PURE_NE = [(0, 0), (1, 1)]
BOS_PURE_NE_PAYOFFS = [(3, 2), (2, 3)]

# Mixed strategy NE:
# KEY INSIGHT: player mixes to make OPPONENT indifferent, not self.
#
# Let p = prob P1 plays Opera, q = prob P2 plays Opera.
#
# To find p: make P2 indifferent between Opera and Fight
#   P2 payoff from Opera: 2*p + 0*(1-p) = 2p
#   P2 payoff from Fight: 0*p + 3*(1-p) = 3 - 3p
#   Set equal: 2p = 3 - 3p  =>  5p = 3  =>  p = 3/5
#
# To find q: make P1 indifferent between Opera and Fight
#   P1 payoff from Opera: 3*q + 0*(1-q) = 3q
#   P1 payoff from Fight: 0*q + 2*(1-q) = 2 - 2q
#   Set equal: 3q = 2 - 2q  =>  5q = 2  =>  q = 2/5
#
# Expected payoff at mixed NE:
#   P1: 3q = 3*(2/5) = 6/5 = 1.2
#   P2: 2p = 2*(3/5) = 6/5 = 1.2
BOS_HAS_MIXED_NE = True
BOS_MIXED_P = 3 / 5       # 0.6  — P1 plays Opera with this probability
BOS_MIXED_Q = 2 / 5       # 0.4  — P2 plays Opera with this probability
BOS_MIXED_PAYOFF_P1 = 6 / 5   # 1.2
BOS_MIXED_PAYOFF_P2 = 6 / 5   # 1.2

# ── General 2×2 mixed strategy formula ────────────────────────────────
# For matrix [[(a11_1,a11_2),(a12_1,a12_2)],[(a21_1,a21_2),(a22_1,a22_2)]]
#
# p (P1 mixing) makes P2 indifferent:
#   P2 col0: a11_2*p + a21_2*(1-p)  vs  P2 col1: a12_2*p + a22_2*(1-p)
#   p = (a22_2 - a21_2) / (a11_2 - a12_2 - a21_2 + a22_2)
#
# q (P2 mixing) makes P1 indifferent:
#   P1 row0: a11_1*q + a12_1*(1-q)  vs  P1 row1: a21_1*q + a22_1*(1-q)
#   q = (a22_1 - a12_1) / (a11_1 - a12_1 - a21_1 + a22_1)

PRIOR_ERRORS = {
    "mixed_makes_self_indifferent": "Uses own payoffs to find own mixing prob (should use opponent's payoffs)",
    "dominant_not_nash":            "Confuses dominant strategy with Nash equilibrium (dominant implies Nash, not vice versa)",
    "mixed_prob_wrong":             "Swaps p and q — assigns P1's mixing prob to P2 or vice versa",
}
