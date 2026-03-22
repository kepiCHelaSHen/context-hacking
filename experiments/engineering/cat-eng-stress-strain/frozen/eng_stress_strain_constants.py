"""Stress-Strain — Frozen Constants. Source: Dowling, Mechanical Behavior of Materials, 5th Ed. DO NOT MODIFY."""
import math

# Engineering stress: sigma_eng = F / A0          (original cross-section area)
# True stress:        sigma_true = F / A = sigma_eng * (1 + eps_eng)  (for uniform deformation)
# Engineering strain: eps_eng = dL / L0
# True strain:        eps_true = ln(1 + eps_eng)  (NOT equal to dL/L0!)
# Young's modulus:    E = sigma / epsilon          (elastic region only)

# LLM priors:
#   "true_equals_engineering" — treats sigma_true = sigma_eng (ignores area reduction)
#   "true_strain_linear"     — uses dL/L0 for true strain instead of ln(1 + eps_eng)
#   "modulus_wrong_region"   — computes E in plastic region where it is meaningless

# Reference test case: F=50 kN, A0=100 mm^2=1e-4 m^2, dL=0.5 mm, L0=100 mm
F_REF = 50000.0       # 50 kN in N
A0_REF = 1e-4          # 100 mm^2 in m^2
DL_REF = 0.5e-3        # 0.5 mm in m
L0_REF = 0.1           # 100 mm in m

# Engineering stress: 50000 / 1e-4 = 500e6 Pa = 500 MPa
SIGMA_ENG_REF = F_REF / A0_REF                          # 500_000_000.0 Pa

# Engineering strain: 0.5e-3 / 0.1 = 0.005 (dimensionless)
EPS_ENG_REF = DL_REF / L0_REF                           # 0.005

# True stress: 500e6 * (1 + 0.005) = 502.5e6 Pa = 502.5 MPa  (HIGHER than engineering!)
SIGMA_TRUE_REF = SIGMA_ENG_REF * (1.0 + EPS_ENG_REF)   # 502_500_000.0 Pa

# True strain: ln(1.005) = 0.004987541... (LOWER than engineering strain!)
EPS_TRUE_REF = math.log(1.0 + EPS_ENG_REF)              # 0.00498754...

# Young's modulus: 500e6 / 0.005 = 100e9 Pa = 100 GPa
E_REF = SIGMA_ENG_REF / EPS_ENG_REF                     # 100_000_000_000.0 Pa

# Wrong values that LLMs produce
SIGMA_TRUE_WRONG = SIGMA_ENG_REF              # LLM error: true stress = engineering stress
EPS_TRUE_WRONG   = EPS_ENG_REF                # LLM error: true strain = engineering strain

PRIOR_ERRORS = {
    "true_equals_engineering": "Treats sigma_true = sigma_eng, ignoring cross-section reduction under load",
    "true_strain_linear":     "Uses dL/L0 for true strain instead of ln(1 + eps_eng) — equal only at infinitesimal strain",
    "modulus_wrong_region":   "Computes Young's modulus using plastic-region data where stress-strain is nonlinear",
}
