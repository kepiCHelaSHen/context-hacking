"""Goodwin Oscillator (Circadian Rhythm) — Frozen Constants. Source: Goodwin 1965, Griffith 1968. DO NOT MODIFY."""
import math

# Goodwin 3-variable negative feedback loop:
#   dX/dt = k1 * K^n / (K^n + Z^n) - k2 * X   (mRNA, Hill-repressed by Z)
#   dY/dt = k3 * X - k4 * Y                      (protein translation)
#   dZ/dt = k5 * Y - k6 * Z                      (nuclear effector)
#
# Hill repression function: h(Z) = K^n / (K^n + Z^n)
#   h(0) = 1 (no repressor → max transcription)
#   h(K) = 0.5 (half-repression at Z=K)
#   h(∞) → 0 (full repression)
#
# KEY INSIGHT: For sustained oscillations in the BASIC 3-variable Goodwin model,
#   the Hill coefficient n must be STRICTLY GREATER THAN 8.
#   - n = 1,2,3,...,8: damped oscillations only (stable spiral → fixed point)
#   - n ≥ 9 (integer): sustained limit-cycle oscillations
#   Theoretical threshold: n > 8 (Griffith 1968, rigorous Hopf bifurcation analysis)
#   Practical minimum integer: n = 9
#
# COMMON CONFUSION:
#   - The repressilator (Elowitz & Leibler 2000) has 3 GENES each repressing the next,
#     and needs n ≥ 2 for oscillation — but that is a DIFFERENT model (9 variables, not 3).
#   - Modified Goodwin models (with additional nonlinearities, delays, or more variables)
#     can oscillate with smaller n, but the BASIC 3-variable model cannot.

# --- Test parameters (symmetric for clarity) ---
K1 = 1.0   # max transcription rate
K2 = 0.1   # mRNA degradation rate
K3 = 1.0   # translation rate
K4 = 0.1   # protein degradation rate
K5 = 1.0   # modification/nuclear entry rate
K6 = 0.1   # effector degradation rate
K  = 1.0   # Hill repression half-max constant

# Hill coefficient threshold
HILL_THRESHOLD = 8       # n must be STRICTLY greater than this
MIN_HILL_INTEGER = 9     # smallest integer n giving sustained oscillations

# Test Hill coefficients
N_NO_OSCILLATION = 2     # n=2: damped only (common LLM error claims this works)
N_OSCILLATION = 10       # n=10: sustained limit cycle

# --- Hill repression reference values ---
# h(Z, K, n) = K^n / (K^n + Z^n)
# With K=1:
#   h(0, 1, n) = 1.0           (any n)
#   h(1, 1, n) = 0.5           (any n, since K^n = Z^n)
#   h(2, 1, 10) = 1 / (1 + 2^10) = 1 / 1025
HILL_AT_Z0 = 1.0
HILL_AT_ZK = 0.5
HILL_AT_Z2_N10 = K ** N_OSCILLATION / (K ** N_OSCILLATION + 2.0 ** N_OSCILLATION)

# --- Steady-state (fixed point) for symmetric params ---
# At steady state: dX=dY=dZ=0
# X* = (k1/k2) * h(Z*), Y* = (k3/k4)*X*, Z* = (k5/k6)*Y*
# With k1=k3=k5=1, k2=k4=k6=0.1, K=1:
#   Z* = (k5/k6)*(k3/k4)*(k1/k2)*h(Z*) = 1000 * h(Z*)
#   Z* = 1000 * K^n / (K^n + Z*^n)
#   For large n, fixed point is near Z* ≈ K = 1 (since 1000*h(1)=500, need to solve numerically)

# --- Derivative reference at (X,Y,Z) = (1,1,1) with n=10 ---
# dX/dt = k1 * 1^10/(1^10+1^10) - k2*1 = 1.0 * 0.5 - 0.1 = 0.4
# dY/dt = k3 * 1 - k4 * 1 = 1.0 - 0.1 = 0.9
# dZ/dt = k5 * 1 - k6 * 1 = 1.0 - 0.1 = 0.9
DERIV_REF_X = K1 * 0.5 - K2 * 1.0    # 0.4
DERIV_REF_Y = K3 * 1.0 - K4 * 1.0    # 0.9
DERIV_REF_Z = K5 * 1.0 - K6 * 1.0    # 0.9

assert math.isclose(DERIV_REF_X, 0.4, rel_tol=1e-9), f"dX ref should be 0.4, got {DERIV_REF_X}"
assert math.isclose(DERIV_REF_Y, 0.9, rel_tol=1e-9), f"dY ref should be 0.9, got {DERIV_REF_Y}"
assert math.isclose(DERIV_REF_Z, 0.9, rel_tol=1e-9), f"dZ ref should be 0.9, got {DERIV_REF_Z}"
assert math.isclose(HILL_AT_Z0, 1.0), "h(0) must be 1"
assert math.isclose(HILL_AT_ZK, 0.5), "h(K) must be 0.5"
assert HILL_AT_Z2_N10 < 0.01, f"h(2,1,10) should be tiny, got {HILL_AT_Z2_N10}"
assert MIN_HILL_INTEGER > HILL_THRESHOLD, "Min integer Hill must exceed threshold"
assert not (N_NO_OSCILLATION > HILL_THRESHOLD), "n=2 must NOT exceed threshold"

PRIOR_ERRORS = {
    "n_geq_2_sufficient":       "Claims n>=2 gives sustained oscillations in basic 3-var Goodwin (WRONG: need n>8)",
    "confuses_with_repressilator": "Confuses Goodwin (1 gene, 3 vars) with repressilator (3 genes, n>=2 suffices)",
    "forgets_hill_in_repression": "Omits Hill function from repression term (uses linear or Michaelis-Menten instead)",
}
