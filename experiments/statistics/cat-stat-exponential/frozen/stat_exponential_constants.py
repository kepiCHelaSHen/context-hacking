"""Exponential Distribution — Frozen Constants. Source: NIST. DO NOT MODIFY."""
import math
# Exponential PDF:  f(x) = lam * e^(-lam*x)   for x >= 0
# Exponential CDF:  F(x) = 1 - e^(-lam*x)
# Mean = 1/lam  (NOT lam!)
# Variance = 1/lam^2
# Memoryless property: P(X > s+t | X > s) = P(X > t)
#
# Test scenario: lam = 0.5 (rate parameter)
#   mean = 1/0.5 = 2.0  (NOT 0.5 — the most common LLM error)
#   variance = 1/0.25 = 4.0
#   P(X <= 1) = 1 - e^(-0.5)  = 0.393469340287367
#   P(X <= 2) = 1 - e^(-1.0)  = 0.632120558828558
#   P(X >  3) = e^(-1.5)      = 0.223130160148430
#   Memoryless: P(X>5 | X>2)  = P(X>5)/P(X>2) = e^(-2.5)/e^(-1.0)
#                              = e^(-1.5) = P(X>3) = 0.223130160148430
LAMBDA = 0.5
MEAN = 1.0 / LAMBDA                              # 2.0
VARIANCE = 1.0 / LAMBDA**2                       # 4.0
PDF_1 = LAMBDA * math.exp(-LAMBDA * 1)           # 0.303265329856317
PDF_2 = LAMBDA * math.exp(-LAMBDA * 2)           # 0.183939720585721
CDF_1 = 1.0 - math.exp(-LAMBDA * 1)             # 0.393469340287367
CDF_2 = 1.0 - math.exp(-LAMBDA * 2)             # 0.632120558828558
SURV_3 = math.exp(-LAMBDA * 3)                   # 0.223130160148430
# Memoryless test:  P(X>5 | X>2) = P(X>3)
MEMORYLESS_S = 2.0
MEMORYLESS_T = 3.0
MEMORYLESS_COND = math.exp(-LAMBDA * MEMORYLESS_T)  # e^(-1.5) = 0.223130...
# Wrong answers that LLMs commonly produce
MEAN_WRONG = LAMBDA                              # 0.5 — wrong: confuses rate with mean
VARIANCE_WRONG = LAMBDA                          # 0.5 — wrong: confuses rate with variance
PRIOR_ERRORS = {
    "mean_is_lambda":   "Claims mean = lam instead of 1/lam (confuses rate and mean)",
    "variance_is_lambda": "Claims variance = lam instead of 1/lam^2",
    "memoryless_wrong": "Computes P(X>5|X>2) != P(X>3); violates memoryless property",
}
