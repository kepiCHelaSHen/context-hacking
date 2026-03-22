"""Holling's Functional Response — Frozen Constants. Source: Holling 1959. DO NOT MODIFY."""
import math

# ── Holling's Functional Response Types ──────────────────────────────
# Type I:  f(N) = a*N             (linear, capped at N_max)
# Type II: f(N) = a*N / (1+a*h*N)  (hyperbolic, decelerating — Michaelis-Menten-like)
# Type III: f(N) = a*N² / (1+a*h*N²) (SIGMOIDAL, accelerating then decelerating)
#
# KEY DISTINCTION:
#   Type II  uses N   in numerator and denominator → hyperbolic (always decelerating)
#   Type III uses N²  in numerator and denominator → sigmoidal  (accelerating at low N,
#                                                                 decelerating at high N)
#
# At low prey density N:
#   Type II:  f ≈ a*N    (linear, slope = a)
#   Type III: f ≈ a*N²   (quadratic, ACCELERATING — this gives the sigmoid shape)
#
# At high prey density N:
#   Both types saturate at max consumption rate = 1/h
#
# The sigmoid shape of Type III arises because predators "learn" or "switch"
# to a prey species only once it becomes common (density-dependent attack rate).

# ── Test parameters ──────────────────────────────────────────────────
A = 0.1     # attack rate (area searched per unit time)
H = 0.5     # handling time per prey item

MAX_RATE = 1.0 / H  # = 2.0 — maximum consumption rate for both Type II and III

# ── Pre-computed Type II values: f(N) = a*N / (1 + a*h*N) ──────────
TYPE_II_AT_N10  = A * 10  / (1 + A * H * 10)    # 1.0/1.5   = 0.66667
TYPE_II_AT_N100 = A * 100 / (1 + A * H * 100)   # 10.0/6.0  = 1.66667

assert math.isclose(TYPE_II_AT_N10,  1.0 / 1.5,  rel_tol=1e-9)
assert math.isclose(TYPE_II_AT_N100, 10.0 / 6.0, rel_tol=1e-9)
assert TYPE_II_AT_N100 < MAX_RATE, "Type II must be below max rate at finite N"

# ── Pre-computed Type III values: f(N) = a*N² / (1 + a*h*N²) ───────
TYPE_III_AT_N10 = A * 100 / (1 + A * H * 100)   # 10.0/6.0  = 1.66667
TYPE_III_AT_N3  = A * 9   / (1 + A * H * 9)     # 0.9/1.45  = 0.62069

assert math.isclose(TYPE_III_AT_N10, 10.0 / 6.0,  rel_tol=1e-9)
assert math.isclose(TYPE_III_AT_N3,  0.9 / 1.45,  rel_tol=1e-9)
assert TYPE_III_AT_N10 < MAX_RATE, "Type III must be below max rate at finite N"

# ── Verify Type III is sigmoidal: accelerating at low N ─────────────
# The second derivative of Type III is positive at low N (concave up = accelerating).
# Simple check: slope from N=1→2 should be LESS than slope from N=2→3.
_f3_1 = A * 1  / (1 + A * H * 1)    # f(1) = 0.1/1.05
_f3_2 = A * 4  / (1 + A * H * 4)    # f(2) = 0.4/1.2
_f3_3 = A * 9  / (1 + A * H * 9)    # f(3) = 0.9/1.45
_slope_12 = _f3_2 - _f3_1   # slope from N=1 to N=2
_slope_23 = _f3_3 - _f3_2   # slope from N=2 to N=3

assert _slope_23 > _slope_12, (
    f"Type III must ACCELERATE at low N (slope_23={_slope_23:.4f} > slope_12={_slope_12:.4f})"
)

# ── Verify Type II is NOT sigmoidal: always decelerating ────────────
_f2_1 = A * 1  / (1 + A * H * 1)    # f(1)
_f2_2 = A * 2  / (1 + A * H * 2)    # f(2)
_f2_3 = A * 3  / (1 + A * H * 3)    # f(3)
_slope2_12 = _f2_2 - _f2_1
_slope2_23 = _f2_3 - _f2_2

assert _slope2_23 < _slope2_12, (
    f"Type II must DECELERATE (slope_23={_slope2_23:.4f} < slope_12={_slope2_12:.4f})"
)

# ── Type III ≠ Type II at low prey density ──────────────────────────
# At N=3, Type III and Type II give DIFFERENT values (Type III is sigmoidal)
TYPE_II_AT_N3 = A * 3 / (1 + A * H * 3)   # 0.3/1.15 = 0.26087
assert not math.isclose(TYPE_III_AT_N3, TYPE_II_AT_N3, rel_tol=0.01), (
    "Type III at N=3 must differ from Type II at N=3 — they have different shapes!"
)

# ── Type I linearity ────────────────────────────────────────────────
TYPE_I_AT_N5  = A * 5    # = 0.5
TYPE_I_AT_N10 = A * 10   # = 1.0
assert math.isclose(TYPE_I_AT_N5, 0.5, rel_tol=1e-9)
assert math.isclose(TYPE_I_AT_N10, 1.0, rel_tol=1e-9)

PRIOR_ERRORS = {
    "type3_hyperbolic": "Gives Type III same formula as Type II — aN/(1+ahN) instead of aN²/(1+ahN²)",
    "type3_no_squared": "Forgets N² in Type III formula — uses N instead of N²",
    "max_rate_wrong":   "Wrong saturation level — max consumption rate is 1/h for both Type II and III",
}
