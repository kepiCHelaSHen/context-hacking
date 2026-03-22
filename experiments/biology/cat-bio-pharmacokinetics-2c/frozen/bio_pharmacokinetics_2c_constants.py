"""Two-Compartment Pharmacokinetics — Frozen Constants. Source: Gibaldi & Perrier 1982. DO NOT MODIFY."""
import math
# C(t) = A*e^(-alpha*t) + B*e^(-beta*t)  (biexponential, two-compartment IV bolus)
# alpha = distribution rate constant (rapid, initial phase)
# beta  = elimination rate constant (slower, terminal phase)
# KEY: alpha > beta — distribution is FASTER than elimination
# Terminal half-life = ln(2)/beta  (NOT ln(2)/alpha!)
# Distribution half-life = ln(2)/alpha
#
# COMMON LLM ERRORS:
#   1. Swapping alpha/beta: using alpha for elimination, beta for distribution
#   2. Single exponential: C(t)=C0*e^(-ke*t) ignores biexponential nature
#   3. Terminal t½ = ln(2)/alpha (wrong — alpha is distribution, not elimination)
#
# Test: A=60, B=40, alpha=2.0 hr⁻¹, beta=0.2 hr⁻¹
#   C(0) = 60 + 40 = 100 mg/L
#   C(1) = 60*e^(-2) + 40*e^(-0.2) = 8.120 + 32.749 = 40.869 mg/L
#   C(5) = 60*e^(-10) + 40*e^(-1.0) = 0.003 + 14.715 = 14.718 mg/L
#     (distribution phase essentially done by t=5)
#   Terminal t½ = ln(2)/0.2 = 3.4657 hr
#   Wrong t½   = ln(2)/2.0 = 0.3466 hr  (using alpha instead of beta!)

A_COEFF = 60.0              # mg/L — distribution coefficient
B_COEFF = 40.0              # mg/L — elimination coefficient
ALPHA = 2.0                 # hr⁻¹ — distribution rate constant (fast phase)
BETA = 0.2                  # hr⁻¹ — elimination rate constant (slow phase)

assert ALPHA > BETA, "alpha must be > beta (distribution faster than elimination)"

C_AT_0 = A_COEFF + B_COEFF                                        # 100.0 mg/L
C_AT_1 = A_COEFF * math.exp(-ALPHA * 1) + B_COEFF * math.exp(-BETA * 1)   # 40.8693…
C_AT_5 = A_COEFF * math.exp(-ALPHA * 5) + B_COEFF * math.exp(-BETA * 5)   # 14.7179…

TERMINAL_HALF_LIFE = math.log(2) / BETA          # 3.465735902799726 hr (correct)
DISTRIBUTION_HALF_LIFE = math.log(2) / ALPHA     # 0.34657359027997264 hr
WRONG_TERMINAL_HALF_LIFE = math.log(2) / ALPHA   # using alpha instead of beta!

# Single-exponential wrong answer: using average ke = (alpha+beta)/2 = 1.1
SINGLE_EXP_KE = (ALPHA + BETA) / 2.0
C_AT_1_SINGLE_EXP = C_AT_0 * math.exp(-SINGLE_EXP_KE * 1)        # wrong: 33.29…

# ── Self-checks ──
assert math.isclose(C_AT_0, 100.0, rel_tol=1e-9), "C(0) must be A+B=100"
assert math.isclose(C_AT_1, 40.86934711731604, rel_tol=1e-9), "C(1) mismatch"
assert math.isclose(C_AT_5, 14.717901642643442, rel_tol=1e-9), "C(5) mismatch"
assert math.isclose(TERMINAL_HALF_LIFE, 3.465735902799726, rel_tol=1e-9), \
    "Terminal t½ must be ln(2)/beta"
assert not math.isclose(TERMINAL_HALF_LIFE, WRONG_TERMINAL_HALF_LIFE, rel_tol=0.01), \
    "Correct terminal t½ must differ from wrong (alpha-based) value"
assert not math.isclose(C_AT_1, C_AT_1_SINGLE_EXP, rel_tol=0.01), \
    "Biexponential C(1) must differ from single-exponential approximation"

PRIOR_ERRORS = {
    "alpha_beta_swap":        "Uses alpha for elimination instead of beta (swaps roles)",
    "single_exponential":     "Models with single exponential C0*e^(-ke*t), ignores biexponential",
    "terminal_half_life_wrong": "Computes terminal t½ as ln(2)/alpha instead of ln(2)/beta",
}
