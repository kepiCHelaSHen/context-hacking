"""
Buffer Chemistry — Frozen Constants
Source: CRC Handbook 103rd Ed Table 5-88, NIST SRD 46
DO NOT MODIFY.
"""

ACETIC_pKa       = 4.756     # LLM prior: 4.74 or 4.76
ACETIC_Ka        = 1.754e-5
PHOSPHATE_pKa2   = 7.198     # LLM prior: 7.2
CARBONIC_pKa1    = 6.352     # apparent (CO2 + H2O) — LLM prior: 3.6 (true H2CO3)
BUFFER_LN10      = 2.302585093   # must appear in buffer capacity formula

PRIOR_ERRORS = {
    "hh_inverted":    "log([HA]/[A-]) instead of log([A-]/[HA])",
    "natural_log":    "uses ln() instead of log10()",
    "missing_ln10":   "omits 2.303 from buffer capacity",
    "true_h2co3":     "uses pKa=3.6 (true H2CO3) not 6.352 (apparent CO2)",
}
