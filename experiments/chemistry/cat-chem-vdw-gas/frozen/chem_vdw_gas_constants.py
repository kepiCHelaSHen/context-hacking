"""
Van der Waals — Frozen Constants
Source: Atkins PC 11e Table 1C.3
DO NOT MODIFY.
"""

R_ATM = 0.082057366    # L atm mol-1 K-1

VDW = {
    "H2":  {"a": 0.2476, "b": 0.02661},
    "N2":  {"a": 1.370,  "b": 0.03870},
    "CO2": {"a": 3.640,  "b": 0.04267},
    "H2O": {"a": 5.536,  "b": 0.03049},
    "NH3": {"a": 4.225,  "b": 0.03707},
}

PRIOR_ERRORS = {
    "ideal_always":     "Uses PV=nRT for CO2 at high pressure",
    "wrong_Tc_formula": "Tc = a/(Rb) not 8a/(27Rb)",
    "wrong_Pc_formula": "Pc = a/b^2 not a/(27b^2)",
    "missing_n2_term":  "Writes a/V^2 not n^2*a/V^2",
}
