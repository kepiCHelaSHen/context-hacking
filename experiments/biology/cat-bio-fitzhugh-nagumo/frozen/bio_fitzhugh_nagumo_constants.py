"""FitzHugh-Nagumo Model — Frozen Constants. Source: FitzHugh 1961, Nagumo 1962. DO NOT MODIFY."""
import math

# dv/dt = v - v^3/3 - w + I_ext   (fast variable, voltage-like)
# dw/dt = eps*(v + a - b*w)        (slow variable, recovery)
#
# v-nullcline: w = v - v^3/3 + I_ext   (CUBIC — key fact)
# w-nullcline: w = (v + a) / b         (LINEAR)
#
# Fixed point lies at the intersection of the two nullclines.
# KEY: the v-nullcline is CUBIC, not linear or parabolic.
# KEY: epsilon (eps) must appear in the w-equation — it sets the timescale separation.

A = 0.7           # offset parameter
B = 0.8           # recovery damping
EPS = 0.08        # timescale separation (epsilon)
I_EXT = 0.0       # external current (default)

# --- Fixed-point calculation (I_ext=0) ---
# Solve v - v^3/3 = (v + a)/b  =>  0.8(v - v^3/3) = v + 0.7
# =>  0.8v^3/3 + 0.2v + 0.7 = 0
# Numerical solution:
V_FP = -1.199408    # approximate fixed point v
W_FP = -0.624260    # approximate fixed point w = (v + a)/b

# Verify fixed point sits on both nullclines
_w_from_v_null = V_FP - V_FP**3 / 3 + I_EXT
_w_from_w_null = (V_FP + A) / B
assert math.isclose(_w_from_v_null, W_FP, abs_tol=1e-4), \
    f"v-nullcline mismatch: {_w_from_v_null} vs {W_FP}"
assert math.isclose(_w_from_w_null, W_FP, abs_tol=1e-4), \
    f"w-nullcline mismatch: {_w_from_w_null} vs {W_FP}"

# Verify dv/dt ~ 0 and dw/dt ~ 0 at fixed point
_dv = V_FP - V_FP**3 / 3 - W_FP + I_EXT
_dw = EPS * (V_FP + A - B * W_FP)
assert abs(_dv) < 1e-3, f"dv/dt at fixed point not ~0: {_dv}"
assert abs(_dw) < 1e-3, f"dw/dt at fixed point not ~0: {_dw}"

# --- v-nullcline reference values (CUBIC check) ---
# Evaluate w = v - v^3/3 at several v values
V_NULL_POINTS = {
    -2.0:  -2.0 - (-2.0)**3 / 3,   #  0.66667
    -1.0:  -1.0 - (-1.0)**3 / 3,   # -0.66667
     0.0:   0.0,                     #  0.0
     1.0:   1.0 - 1.0 / 3,          #  0.66667
     2.0:   2.0 - 8.0 / 3,          # -0.66667
}
# Cubic proof: v-nullcline has odd symmetry about origin when I=0: w(-v) = -w(v)
assert math.isclose(V_NULL_POINTS[-2.0], -V_NULL_POINTS[2.0], abs_tol=1e-9), \
    "v-nullcline should have odd-function symmetry (w(-v) = -w(v)) when I=0"
# Cubic proof: v-nullcline is NOT linear — check that second differences are nonzero
_vals = [V_NULL_POINTS[v] for v in [-2.0, -1.0, 0.0, 1.0, 2.0]]
_d1 = [_vals[i + 1] - _vals[i] for i in range(4)]
_d2 = [_d1[i + 1] - _d1[i] for i in range(3)]
assert any(abs(d) > 0.1 for d in _d2), \
    f"v-nullcline second differences too small — should be cubic, not linear: {_d2}"

PRIOR_ERRORS = {
    "v_nullcline_linear":  "Wrongly makes v-nullcline linear instead of cubic w = v - v^3/3",
    "wrong_cubic_sign":    "Gets v^3/3 sign wrong in v-nullcline (should be v - v^3/3, not v + v^3/3)",
    "epsilon_missing":     "Forgets epsilon in dw/dt (should be eps*(v + a - b*w), not just v + a - b*w)",
}
