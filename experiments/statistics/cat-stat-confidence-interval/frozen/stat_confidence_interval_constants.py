"""
Confidence Intervals — Frozen Constants
Source: Neyman 1937
DO NOT MODIFY.
"""
import math

# ── Frequentist interpretation ────────────────────────────────────────
# 95% CI means: if we repeated the experiment many times, 95% of the
# constructed intervals would contain the true parameter.
# It does NOT mean: "there is a 95% probability that μ is in [a, b]".
# The parameter is FIXED; the interval is RANDOM (varies by sample).

# ── CI width formula (large n, known σ) ──────────────────────────────
# CI = x̄ ± z_{α/2} · SE,  where SE = σ / √n
# Width = 2 · z_{α/2} · SE
# Wider CI → higher confidence, NOT more precision.

# ── Test scenario: n=36, x̄=50, σ=12 ─────────────────────────────────
N     = 36
XBAR  = 50.0
SIGMA = 12.0
SE    = SIGMA / math.sqrt(N)       # 12 / 6 = 2.0

# ── Critical z-values ────────────────────────────────────────────────
Z_95  = 1.96
Z_99  = 2.576

# ── 95% confidence interval ──────────────────────────────────────────
CI_95_LOWER = XBAR - Z_95 * SE     # 50 - 3.92  = 46.08
CI_95_UPPER = XBAR + Z_95 * SE     # 50 + 3.92  = 53.92

# ── 99% confidence interval ──────────────────────────────────────────
CI_99_LOWER = XBAR - Z_99 * SE     # 50 - 5.152 = 44.848
CI_99_UPPER = XBAR + Z_99 * SE     # 50 + 5.152 = 55.152

# ── Common LLM errors ────────────────────────────────────────────────
PRIOR_ERRORS = {
    "prob_parameter_in_ci":   "Says '95% chance μ is in this CI' — WRONG. "
                              "The parameter is fixed; the interval is random. "
                              "95% is the long-run coverage rate, not a posterior probability.",
    "wider_ci_more_precise":  "Thinks a wider CI is 'more precise' — WRONG. "
                              "Wider CI = higher confidence but LESS precision.",
    "ci_width_proportional_n": "Thinks CI width scales with n — WRONG. "
                               "Width scales with 1/√n (via SE = σ/√n).",
}
