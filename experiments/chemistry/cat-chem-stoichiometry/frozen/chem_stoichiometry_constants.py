"""
Stoichiometry — Frozen Atomic Weights
Source: IUPAC 2021 Table of Standard Atomic Weights
Pure and Applied Chemistry Vol 93 No 6 2021
DO NOT MODIFY.
"""

AW = {
    "H":  1.008,   "C":  12.011,  "N":  14.007,
    "O":  15.999,  "F":  18.998,  "Na": 22.990,
    "Mg": 24.305,  "Al": 26.982,  "Si": 28.085,
    "P":  30.974,  "S":  32.06,   "Cl": 35.45,
    "K":  39.098,  "Ca": 40.078,  "Fe": 55.845,
    "Cu": 63.546,  "Zn": 65.38,   "Ag": 107.87,
    "I":  126.90,  "Au": 196.97,  "Pb": 207.2,
}

AVOGADRO = 6.02214076e23   # mol-1 (CODATA 2018)

PRIOR_ERRORS = {
    "integer_masses":        "H=1, C=12, N=14, O=16 — loses precision",
    "avogadro_3sf":          "6.022e23 — drops 5 significant figures",
    "no_limiting_reagent":   "Uses all of each reagent without finding limit",
}
