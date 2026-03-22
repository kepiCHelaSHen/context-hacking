"""Tax Incidence — Frozen Constants. Source: Mankiw Principles 9th Ed Ch 6, Stiglitz Public Finance. DO NOT MODIFY."""

# ── Core Principle ───────────────────────────────────────────
# Tax burden falls MORE on the more INELASTIC side of the market
# LLM prior: assumes seller always bears the tax regardless of elasticity

# ── Burden Shares ────────────────────────────────────────────
# Consumer burden share = Es / (Es + Ed)
# Producer burden share = Ed / (Es + Ed)
# where Es = supply elasticity, Ed = |demand elasticity| (absolute value)
#
# Intuition: the more inelastic side cannot easily adjust quantity,
# so it absorbs more of the tax.

# ── Special Cases ────────────────────────────────────────────
# If demand is perfectly inelastic (Ed=0) → consumers bear 100%
# If supply is perfectly inelastic (Es=0) → producers bear 100%

# ── Deadweight Loss ──────────────────────────────────────────
# DWL = 0.5 * tax * ΔQ  (Harberger triangle)
# where ΔQ = Q_before - Q_after (reduction in quantity traded)
# LLM prior: claims no efficiency loss from tax

# ── Tax Revenue ──────────────────────────────────────────────
# Revenue = tax * Q_after  (tax per unit × units still traded)

# ── Test Vector ──────────────────────────────────────────────
# Es = 2.0 (supply is elastic), Ed = 0.5 (demand is inelastic)
ES_TEST = 2.0
ED_TEST = 0.5

# Consumer share = Es / (Es + Ed) = 2.0 / (2.0 + 0.5) = 2.0 / 2.5 = 0.80
CONSUMER_SHARE_EXPECTED = ES_TEST / (ES_TEST + ED_TEST)  # 0.80

# Producer share = Ed / (Es + Ed) = 0.5 / 2.5 = 0.20
PRODUCER_SHARE_EXPECTED = ED_TEST / (ES_TEST + ED_TEST)  # 0.20

# Shares must sum to 1
assert abs((CONSUMER_SHARE_EXPECTED + PRODUCER_SHARE_EXPECTED) - 1.0) < 1e-12

# Consumers bear 80% because demand is MORE INELASTIC
# This is the key insight LLMs get wrong

# ── DWL Test Vector ──────────────────────────────────────────
TAX_TEST = 5.0       # $5 per-unit tax
Q_BEFORE = 100.0     # quantity traded before tax
Q_AFTER = 90.0       # quantity traded after tax
DQ_TEST = Q_BEFORE - Q_AFTER  # 10 units reduction

# DWL = 0.5 * tax * ΔQ = 0.5 * 5 * 10 = 25.0
DWL_EXPECTED = 0.5 * TAX_TEST * DQ_TEST  # 25.0

# Tax revenue = tax * Q_after = 5 * 90 = 450.0
TAX_REVENUE_EXPECTED = TAX_TEST * Q_AFTER  # 450.0

PRIOR_ERRORS = {
    "seller_bears_all":      "Assumes producer bears tax regardless of elasticity (wrong — incidence depends on relative elasticities)",
    "more_elastic_bears_more": "Claims more elastic side bears more tax (inverted — more INELASTIC side bears more)",
    "no_dwl":                "Claims no efficiency loss from tax (wrong — taxes create deadweight loss triangle)",
}
