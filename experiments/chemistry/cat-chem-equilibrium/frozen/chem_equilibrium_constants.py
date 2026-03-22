"""
Chemical Equilibrium — Frozen Constants
Source: NIST WebBook SRD 69, Atkins Physical Chemistry 11th Ed Appendix 2D
DO NOT MODIFY.
"""
import math

R_J    = 8.314462618    # J mol-1 K-1 (NIST 2018 CODATA)
R_ATM  = 0.082057366    # L atm mol-1 K-1

# Haber-Bosch: N2(g) + 3H2(g) = 2NH3(g) — Source: NIST Chem WebBook
HABER_Kp_298  = 6.77e5     # at 298.15 K
HABER_Kp_500  = 3.55e-2    # at 500 K
HABER_Kp_700  = 7.76e-5    # at 700 K
HABER_dH      = -92400.0   # J/mol (exothermic)
HABER_delta_n = -2         # 2 - (1+3) = -2

# H2 + I2 = 2HI at 700 K — Source: Atkins PC 11e Table 7C.1
HI_Kc_700K = 57.0          # LLM prior: 54 (698K value — wrong)
HI_Kc_298K = 794.0

# H2O autoionization — Source: NIST SRD 46
Kw_298 = 1.011e-14         # LLM prior: exactly 1e-14 (too rounded)
Kw_310 = 2.42e-14          # 37 C body temperature
Kw_373 = 5.13e-13          # 100 C boiling point

VAN_T_HOFF_SIGN = -1       # LLM prior: +1 (sign error)

PRIOR_ERRORS = {
    "kp_kc_same":       "LLM treats Kp=Kc, ignores delta_n",
    "van_t_hoff_sign":  "LLM writes +(dH/R) not -(dH/R)",
    "kw_temperature":   "LLM says pH=7 at all temperatures",
    "hi_kc_value":      "LLM uses 54 (698K) not 57 (700K)",
}
