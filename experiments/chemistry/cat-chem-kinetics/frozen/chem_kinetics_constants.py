"""
Reaction Kinetics — Frozen Constants
Source: Moelwyn-Hughes (1971), JPL Publication 19-5 (2019)
DO NOT MODIFY.
"""

R = 8.314462618           # J mol-1 K-1

# H2 + I2 -> 2HI — Source: Moelwyn-Hughes (1971)
H2I2_Ea   = 165000.0    # J/mol — LLM prior: 165 (kJ not J)
H2I2_A    = 1.65e13     # s-1
H2I2_k700 = 1.65e-3     # L mol-1 s-1 at 700K (published)

K_RELATIVE_TOLERANCE = 0.20

PRIOR_ERRORS = {
    "ea_in_kj":        "Uses 165 instead of 165000 — kJ not J",
    "sign_in_ea_calc": "Ea = +R*ln(k2/k1)/(1/T2-1/T1) — wrong sign",
    "second_order":    "Uses C0 - kt (zero-order) for second-order",
}
