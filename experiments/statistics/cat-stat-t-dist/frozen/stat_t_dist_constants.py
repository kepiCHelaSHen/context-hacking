"""Student's t-Distribution — Frozen Constants. Source: NIST/Gosset 1908. DO NOT MODIFY."""
import math
# t-distribution: df = n - 1 for one-sample t-test (NOT n)
# For n=25 sample: df = 24
# Critical t-values (two-tailed alpha=0.05, i.e. each tail alpha/2=0.025):
#   t_{0.025, 24} = 2.0639   (correct, df = n-1 = 24)
#   t_{0.025, 25} = 2.0595   (wrong — uses df = n = 25)
# Test scenario: sample mean=100, s=15, n=25 -> SE = s/sqrt(n) = 15/5 = 3.0
#   95% CI = xbar +/- t_crit * SE
#   Correct (df=24): 100 +/- 2.0639*3 = (93.8083, 106.1917)
#   Wrong   (df=25): 100 +/- 2.0595*3 = (93.8215, 106.1785)
N_SAMPLE = 25
XBAR = 100.0
S_SAMPLE = 15.0
SE = S_SAMPLE / math.sqrt(N_SAMPLE)  # = 3.0
DF_CORRECT = N_SAMPLE - 1            # = 24
DF_WRONG = N_SAMPLE                  # = 25 (common LLM error)
T_CRIT_24 = 2.0639                   # t_{0.025, 24}
T_CRIT_25 = 2.0595                   # t_{0.025, 25}
CI_LOWER = round(XBAR - T_CRIT_24 * SE, 3)   # 93.808
CI_UPPER = round(XBAR + T_CRIT_24 * SE, 3)   # 106.192
PRIOR_ERRORS = {
    "df_n_not_n_minus_1":  "Uses df=n instead of df=n-1 for one-sample t-test",
    "z_instead_of_t":      "Uses z=1.96 instead of t-critical for small n",
    "se_uses_n_not_sqrt_n": "Divides s by n instead of sqrt(n) for standard error",
}
