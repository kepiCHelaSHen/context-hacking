"""Ricardo's Comparative Advantage — Frozen Constants. Source: Ricardo, Principles of Political Economy (1817). DO NOT MODIFY."""

# ── Definitions ──────────────────────────────────────────────────────
# Absolute advantage:    produce MORE of a good with the same resources
#                        (equivalently, fewer hours per unit)
# Comparative advantage: lower OPPORTUNITY COST of producing a good
# KEY: A country can have absolute advantage in BOTH goods but
#      comparative advantage in only ONE.

# ── Test Scenario ────────────────────────────────────────────────────
# Hours to produce ONE unit:
#              Wine    Cloth
# Country A:   10       5
# Country B:   20      15
A_HOURS_WINE  = 10
A_HOURS_CLOTH =  5
B_HOURS_WINE  = 20
B_HOURS_CLOTH = 15

# A has absolute advantage in BOTH (fewer hours for both goods).

# ── Opportunity Costs ────────────────────────────────────────────────
# OC(good_X) = hours_X / hours_Y  (what you give up of Y to make one X)
# A: 1 wine costs 10/5 = 2.0 cloth;   1 cloth costs 5/10 = 0.5 wine
# B: 1 wine costs 20/15 ≈ 1.333 cloth; 1 cloth costs 15/20 = 0.75 wine
OC_A_WINE  = A_HOURS_WINE  / A_HOURS_CLOTH   # 2.0     cloth per wine
OC_A_CLOTH = A_HOURS_CLOTH / A_HOURS_WINE     # 0.5     wine per cloth
OC_B_WINE  = B_HOURS_WINE  / B_HOURS_CLOTH    # 1.3333  cloth per wine
OC_B_CLOTH = B_HOURS_CLOTH / B_HOURS_WINE     # 0.75    wine per cloth

# ── Comparative Advantage ────────────────────────────────────────────
# Cloth: A (0.5 wine) < B (0.75 wine) → A has comp. adv. in CLOTH
# Wine:  B (1.333 cloth) < A (2.0 cloth) → B has comp. adv. in WINE
# Both benefit from trade even though A is better at everything!

# ── Terms of Trade ───────────────────────────────────────────────────
# Mutually beneficial terms-of-trade range for wine (in cloth per wine):
#   min = OC_B_WINE = 1.333  (B's OC — below this B won't trade)
#   max = OC_A_WINE = 2.0    (A's OC — above this A won't trade)
TOT_WINE_MIN = OC_B_WINE   # 1.3333 cloth per wine
TOT_WINE_MAX = OC_A_WINE   # 2.0    cloth per wine

# ── Prior LLM Errors ────────────────────────────────────────────────
PRIOR_ERRORS = {
    "absolute_is_comparative":    "Treats absolute advantage as comparative advantage (they are distinct concepts)",
    "both_advantage_one_country": "Claims one country has comparative advantage in BOTH goods (impossible — each must specialise in one)",
    "opportunity_cost_wrong":     "Computes opportunity cost incorrectly (e.g., inverts the ratio or uses absolute hours)",
}
