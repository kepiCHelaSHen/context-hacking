"""
Radioactive Decay — Frozen Constants
Source: NNDC BNL Nuclear Data Center (ENSDF database)
DO NOT MODIFY.
"""
import math
LN2 = math.log(2)

U238_HALF_LIFE  = 4.468e9    # years
TH234_HALF_LIFE = 0.06617    # years = 24.10 days
RA226_HALF_LIFE = 1600.0     # years (exact as published)

C14_HALF_LIFE       = 5730.0   # years (Godwin 1962 — modern standard)
C14_LIBBY_WRONG     = 5568.0   # years (outdated — DO NOT USE)

PRIOR_ERRORS = {
    "libby_half_life":  "Uses 5568 (Libby, outdated) not 5730 (Godwin)",
    "secular_eq_atoms": "Says N1=N2 at secular equilibrium (wrong — A1=A2)",
}
