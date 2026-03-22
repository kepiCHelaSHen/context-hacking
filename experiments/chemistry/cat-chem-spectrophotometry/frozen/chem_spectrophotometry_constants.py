"""
Beer-Lambert — Frozen Constants
Source: NIST Chemistry WebBook, Sigma-Aldrich spectral library
DO NOT MODIFY.
"""

EPSILON = {
    "KMnO4_525":   2360,     # L mol-1 cm-1
    "CuSO4_800":   12.0,
    "NADH_340":    6220,
}

DNA_A260_FACTORS = {
    "dsDNA": 50.0,   # ug/mL per A260
    "RNA":   40.0,   # LLM prior for dsDNA
    "ssDNA": 33.0,
}

BEER_LAMBERT_BASE = "log10"   # NOT ln — frozen

PRIOR_ERRORS = {
    "uses_ln":        "A = -ln(T) not -log10(T) — off by 2.303x",
    "sign_error":     "A = log10(T) not -log10(T)",
    "no_path_length": "Ignores l in A=epsilon*c*l",
    "dna_rna_factor": "Uses 40 ug/mL (RNA) for dsDNA (should be 50)",
}
