"""
Frozen constants for cat-bio-membrane-potential.

Nernst Equation: E_ion = (RT / zF) * ln([ion]_out / [ion]_in)

At body temperature (37 C = 310.15 K), RT/F ~ 26.73 mV.
The valence z carries a sign: z = +1 for K+ and Na+, z = -1 for Cl-.
Using z = -1 for Cl- flips the sign of the equilibrium potential.

KEY TRAP: Many LLMs use z = +1 for all ions, producing the wrong sign
for anions like Cl-.  Others swap [out]/[in] or forget Kelvin conversion.
"""

import math

# ── Physical constants ──────────────────────────────────────────────
R = 8.314          # J/(mol*K), gas constant
F = 96485          # C/mol, Faraday constant
T = 310.15         # K, body temperature (37 C)

RT_OVER_F = R * T / F  # ~ 0.026725 V

# ── Physiological ion concentrations (mM) ──────────────────────────
K_OUT  = 4.0       # [K+] extracellular
K_IN   = 140.0     # [K+] intracellular
NA_OUT = 145.0     # [Na+] extracellular
NA_IN  = 12.0      # [Na+] intracellular
CL_OUT = 120.0     # [Cl-] extracellular
CL_IN  = 4.0       # [Cl-] intracellular

# ── Ion valences ────────────────────────────────────────────────────
Z_K  = +1
Z_NA = +1
Z_CL = -1          # CRITICAL: negative valence for chloride

# ── Reference equilibrium potentials (mV) ──────────────────────────
#   E = (RT / zF) * ln(out / in) * 1000
E_K  = (RT_OVER_F / Z_K)  * math.log(K_OUT  / K_IN)  * 1000  # ~ -95.0 mV
E_NA = (RT_OVER_F / Z_NA) * math.log(NA_OUT / NA_IN) * 1000  # ~ +66.6 mV
E_CL = (RT_OVER_F / Z_CL) * math.log(CL_OUT / CL_IN) * 1000  # ~ -90.9 mV

# ── Catalogue of prior LLM errors ──────────────────────────────────
PRIOR_ERRORS = {
    "z_always_1": "Uses z=1 for Cl-, producing +90.9 mV instead of -90.9 mV",
    "wrong_ratio_direction": "Uses [in]/[out] instead of [out]/[in]",
    "celsius_not_kelvin": "Uses T=37 instead of T=310.15 K in RT/F",
}
