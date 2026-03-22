"""Gompertz Growth Model — Frozen Constants. Source: Gompertz 1825, Laird 1964. DO NOT MODIFY."""
import math
# N(t) = K * exp(ln(N₀/K) * exp(-α*t))  [growth rate form]
# Equivalent: N(t) = K * exp(-exp(-b*(t - t_inflection)))
# KEY: Gompertz inflection at N = K/e ≈ 0.3679*K (NOT K/2 like logistic!)
# Gompertz is asymmetric: slow approach to K from above K/e, faster growth below K/e
# Growth rate: dN/dt = -α*N*ln(N/K) (note the ln term — NOT α*N*(1-N/K))
# Test: K=1000, α=0.1, N₀=1
#   N(t) = 1000*exp(ln(1/1000)*exp(-0.1t)) = 1000*exp(-6.9078*exp(-0.1t))
#   N(0) = 1000*exp(-6.9078) = 1.0 ✓
#   N(20) = 1000*exp(-6.9078*0.13534) = 1000*exp(-0.93483) = 392.83
#   N(50) = 1000*exp(-6.9078*0.006738) = 1000*exp(-0.04654) = 954.54
#   Inflection at N = K/e = 367.88
K = 1000
ALPHA = 0.1
N0 = 1.0
LN_N0_OVER_K = math.log(N0 / K)  # ln(1/1000) = -6.907755...
INFLECTION_N = K / math.e         # 367.8794... (NOT K/2 = 500!)
WRONG_INFLECTION = K / 2          # 500.0 — the common LLM mistake
N_20 = K * math.exp(LN_N0_OVER_K * math.exp(-ALPHA * 20))  # ≈ 392.83
N_50 = K * math.exp(LN_N0_OVER_K * math.exp(-ALPHA * 50))  # ≈ 954.54
# Verify frozen values
assert math.isclose(K * math.exp(LN_N0_OVER_K), N0, rel_tol=1e-9), "N(0) must equal N0"
assert math.isclose(INFLECTION_N, K / math.e, rel_tol=1e-9), "Inflection must be K/e"
assert not math.isclose(INFLECTION_N, WRONG_INFLECTION, rel_tol=0.01), "Inflection must NOT be K/2"
PRIOR_ERRORS = {
    "inflection_at_k_half":   "Uses K/2 as inflection instead of K/e",
    "logistic_symmetry":      "Assumes symmetric sigmoid (logistic), but Gompertz is asymmetric",
    "growth_rate_missing_ln": "Omits ln(N/K) term in growth rate, using α*N*(1-N/K) instead",
}
