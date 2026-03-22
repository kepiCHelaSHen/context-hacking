"""
Thermochemistry — Frozen Constants
Source: NIST WebBook, Atkins PC 11e Appendix 2A (kJ/mol at 298.15K, 1 bar)
DO NOT MODIFY.
"""

DHF = {
    "H2(g)":       0.0,
    "O2(g)":       0.0,
    "C(graphite)": 0.0,
    "H2O(l)":    -285.830,
    "H2O(g)":    -241.826,    # LLM uses -285 for gas — WRONG
    "CO2(g)":    -393.509,
    "CO(g)":     -110.527,
    "CH4(g)":     -74.87,
    "C2H4(g)":    +52.47,     # POSITIVE — LLM often gives negative
    "NO(g)":      +90.29,     # POSITIVE — LLM often gives negative
    "NO2(g)":     +33.20,
    "SO2(g)":    -296.83,
    "NH3(g)":     -45.90,
}

BOND_ENTHALPY = {
    "C-H": 414, "C-C": 347, "C=C": 614,
    "O-H": 463, "O=O": 498,
    "N#N": 945, "H-H": 436, "H-Cl": 432,
}

PRIOR_ERRORS = {
    "h2o_gas_liquid": "Uses H2O(l) dHf=-285 for H2O(g)",
    "c2h4_sign":      "Gives negative dHf for C2H4(g) — should be +52.47",
    "no_sign":        "Gives negative dHf for NO(g) — should be +90.29",
    "hess_reversed":  "Uses reactants - products not products - reactants",
    "bond_direction": "Bond formation absorbs energy (wrong)",
}
