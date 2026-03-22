"""
Normal Distribution — Frozen Constants
Source: NIST/Abramowitz & Stegun, values via math.erf (IEEE 754 double precision)
DO NOT MODIFY.
"""
import math

# ── Standard normal PDF: φ(z) = (1/√(2π)) · e^(−z²/2) ──────────────
ONE_OVER_SQRT2PI = 1.0 / math.sqrt(2 * math.pi)  # 0.39894228...

# ── Standard normal CDF: Φ(z) = 0.5 · (1 + erf(z/√2)) ─────────────
# Precise CDF values at key z-scores
CDF_Z1   = 0.5 * (1 + math.erf(1.0 / math.sqrt(2)))   # 0.84134474...
CDF_Z1_5 = 0.5 * (1 + math.erf(1.5 / math.sqrt(2)))   # 0.93319280...
CDF_Z196 = 0.5 * (1 + math.erf(1.96 / math.sqrt(2)))  # 0.97500210...
CDF_Z2   = 0.5 * (1 + math.erf(2.0 / math.sqrt(2)))   # 0.97724987...
CDF_Z3   = 0.5 * (1 + math.erf(3.0 / math.sqrt(2)))   # 0.99865010...

# ── Symmetric intervals: P(−z < Z < z) = 2·Φ(z) − 1 ────────────────
# The 68-95-99.7 rule is an APPROXIMATION; true values below:
P_WITHIN_1SIGMA = 2 * CDF_Z1 - 1  # 0.68268949... (not 0.68)
P_WITHIN_2SIGMA = 2 * CDF_Z2 - 1  # 0.95449974... (not 0.95)
P_WITHIN_3SIGMA = 2 * CDF_Z3 - 1  # 0.99730020... (not 0.997)

# ── Test scenario: x = 85, μ = 70, σ = 10 ───────────────────────────
# z = (x − μ)/σ = (85 − 70)/10 = 1.5
X_TEST  = 85.0
MU_TEST = 70.0
SIGMA_TEST = 10.0
Z_TEST  = (X_TEST - MU_TEST) / SIGMA_TEST            # 1.5
CDF_Z_TEST = 0.5 * (1 + math.erf(Z_TEST / math.sqrt(2)))  # 0.93319280...

PRIOR_ERRORS = {
    "rule_689599_exact":  "Treats 68-95-99.7 as exact rather than approximate "
                          "(true ±3σ = 99.7300%, not 99.7%)",
    "z_sign_flip":        "Computes z = (μ−x)/σ instead of (x−μ)/σ, flipping sign",
    "pdf_not_probability": "Interprets PDF value φ(z) as a probability "
                           "(PDF can exceed 1 for narrow σ; it is a density)",
    "cdf_symmetry_error":  "Computes P(Z < −z) as 1 − Φ(z) instead of Φ(−z) = 1 − Φ(z) "
                           "(correct identity, but then applies it backwards)",
}
