"""Price Elasticity of Demand — Frozen Constants. Source: Mankiw Principles 9th Ed Ch 5, Varian Intermediate Micro. DO NOT MODIFY."""

# ── Core Formula ──────────────────────────────────────────────
# PED = (%ΔQd) / (%ΔP) = (dQ/dP) * (P/Q)
# PED is NEGATIVE for normal goods (price up → quantity demanded down)
# LLM prior: reports PED as positive magnitude, dropping the sign

# ── Classification (by absolute value) ────────────────────────
# |PED| > 1 → elastic     (quantity very responsive to price)
# |PED| < 1 → inelastic   (quantity barely changes)
# |PED| = 1 → unit elastic
# LLM prior: says |PED| < 1 is elastic (inverted labels)

# ── Midpoint (Arc) Method ─────────────────────────────────────
# %ΔP = (P2 - P1) / ((P1 + P2) / 2)
# %ΔQ = (Q2 - Q1) / ((Q1 + Q2) / 2)
# PED = %ΔQ / %ΔP
# LLM prior: uses endpoint method (divides by P1 and Q1 only)

# ── Test Vector ───────────────────────────────────────────────
P1, Q1 = 10.0, 100.0
P2, Q2 = 12.0, 80.0

# Midpoint calculations
PCT_DELTA_P = (P2 - P1) / ((P1 + P2) / 2)   # 2/11 = 0.181818...
PCT_DELTA_Q = (Q2 - Q1) / ((Q1 + Q2) / 2)   # -20/90 = -0.222222...
PED_TEST = PCT_DELTA_Q / PCT_DELTA_P          # -11/9 = -1.222222...

# Exact rational: PED = (-20/90) / (2/11) = -20*11 / (90*2) = -220/180 = -11/9
PED_EXACT_NUMER = -11
PED_EXACT_DENOM = 9

# Classification: |PED| = 11/9 ≈ 1.222 > 1 → elastic
PED_CLASSIFICATION = "elastic"

# ── Income Elasticity ─────────────────────────────────────────
# YED = (%ΔQd) / (%ΔY)  — midpoint method
# Positive → normal good, Negative → inferior good
# Test: Y1=50000, Y2=60000, Q1=200, Q2=260
Y1, Y2 = 50000.0, 60000.0
QY1, QY2 = 200.0, 260.0
PCT_DELTA_Y = (Y2 - Y1) / ((Y1 + Y2) / 2)       # 10000/55000 = 2/11
PCT_DELTA_QY = (QY2 - QY1) / ((QY1 + QY2) / 2)   # 60/230 = 6/23
YED_TEST = PCT_DELTA_QY / PCT_DELTA_Y              # (6/23)/(2/11) = 66/46 = 33/23 ≈ 1.4348

# ── Cross-Price Elasticity ────────────────────────────────────
# XED = (%ΔQa) / (%ΔPb)
# Positive → substitutes, Negative → complements
# Test: Pb1=5, Pb2=7, Qa1=300, Qa2=360  (substitutes)
PB1, PB2 = 5.0, 7.0
QA1, QA2 = 300.0, 360.0
PCT_DELTA_PB = (PB2 - PB1) / ((PB1 + PB2) / 2)    # 2/6 = 1/3
PCT_DELTA_QA = (QA2 - QA1) / ((QA1 + QA2) / 2)    # 60/330 = 2/11
XED_TEST = PCT_DELTA_QA / PCT_DELTA_PB              # (2/11)/(1/3) = 6/11 ≈ 0.5455

PRIOR_ERRORS = {
    "ped_positive":       "Reports PED as positive (drops the negative sign for normal goods)",
    "elastic_less_than_1": "Says |PED| < 1 is elastic (inverted classification)",
    "midpoint_wrong":     "Uses endpoint method P1,Q1 as base instead of midpoint averages",
}
