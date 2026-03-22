"""
Electrochemistry — Frozen Constants
Source: NIST SRD 20, Atkins PC 11e Appendix 2B
DO NOT MODIFY.
"""

F    = 96485.33212    # C mol-1 (CODATA 2018)
R    = 8.314462618
T298 = 298.15

E0 = {
    "F2/F-":       +2.866,
    "Cl2/Cl-":     +1.358,
    "O2/H2O":      +1.229,
    "Cu2+/Cu":     +0.3419,
    "H+/H2":        0.0000,   # SHE — exactly zero by definition
    "Fe2+/Fe":     -0.4402,
    "Zn2+/Zn":     -0.7618,
    "Al3+/Al":     -1.676,
    "Li+/Li":      -3.0401,
}

RT_F_298 = R * T298 / F    # 0.025693 V

PRIOR_ERRORS = {
    "nernst_sign":   "E = E0 + (RT/nF)*ln(Q) — should be MINUS",
    "cell_reversed": "E = E_anode - E_cathode — should be cathode minus anode",
    "deltaG_sign":   "deltaG = +nFE0 — should be MINUS",
}
