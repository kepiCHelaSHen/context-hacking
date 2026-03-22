"""Binomial Distribution — Frozen Constants. Source: NIST. DO NOT MODIFY."""
import math

# P(X=k) = C(n,k) * p^k * (1-p)^(n-k)
# Mean = n*p, Variance = n*p*(1-p)
# Normal approximation valid when np >= 5 AND n(1-p) >= 5

# ── Scenario 1 (valid normal approx): n=100, p=0.5, k=55 ──
# np = 50, n(1-p) = 50 — both >= 5 ✓
N1, P1, K1 = 100, 0.5, 55
MEAN1 = N1 * P1                          # = 50.0
VAR1 = N1 * P1 * (1 - P1)               # = 25.0
EXACT_P_55 = math.comb(N1, K1) * P1**K1 * (1 - P1)**(N1 - K1)
# = 0.048474296626430755

# ── Scenario 2 (INVALID normal approx): n=10, p=0.01 ──
# np = 0.1 < 5 ✗  — normal approximation gives garbage here
N2, P2 = 10, 0.01
MEAN2 = N2 * P2                          # = 0.1
VAR2 = N2 * P2 * (1 - P2)               # = 0.099
EXACT_P_X0 = (1 - P2) ** N2             # 0.99^10 = 0.9043820750088044
EXACT_P_X1 = math.comb(N2, 1) * P2 * (1 - P2) ** (N2 - 1)
# = 10 * 0.01 * 0.99^9 = 0.09135172474836409

PRIOR_ERRORS = {
    "normal_approx_small_np": "Uses normal approx when np < 5 (invalid)",
    "forgets_complement":     "Computes P(X>=k) as 1-P(X<=k) with off-by-one",
    "comb_overflow":          "Numerical issues with large C(n,k) instead of using math.comb",
}
