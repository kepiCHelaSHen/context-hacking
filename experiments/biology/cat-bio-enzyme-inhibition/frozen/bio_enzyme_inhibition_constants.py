"""Enzyme Inhibition — Frozen Constants. Source: Segel 1975, Cornish-Bowden 2012. DO NOT MODIFY."""
import math

# ── Uninhibited Michaelis-Menten ──────────────────────────────────────────
# v = Vmax * [S] / (Km + [S])

# ── Competitive inhibition ────────────────────────────────────────────────
# Inhibitor binds free enzyme only (competes with substrate for active site)
# v = Vmax * [S] / (Km*(1 + [I]/Ki) + [S])
# Apparent Km increases:  Km_app = Km * (1 + [I]/Ki)
# Vmax unchanged
# Lineweaver-Burk: slope changes, y-intercept (1/Vmax) UNCHANGED, x-intercept changes

# ── Uncompetitive inhibition ──────────────────────────────────────────────
# Inhibitor binds ES complex only (cannot bind free enzyme)
# v = Vmax * [S] / (Km + [S]*(1 + [I]/Ki))
# Apparent Km DECREASES:  Km_app = Km / (1 + [I]/Ki)
# Apparent Vmax decreases: Vmax_app = Vmax / (1 + [I]/Ki)
# Lineweaver-Burk: slope UNCHANGED, y-intercept changes, x-intercept changes

# ── Noncompetitive inhibition ─────────────────────────────────────────────
# Inhibitor binds both free enzyme and ES complex equally
# v = Vmax * [S] / ((Km + [S]) * (1 + [I]/Ki))
# Km unchanged
# Vmax decreases: Vmax_app = Vmax / (1 + [I]/Ki)
# Lineweaver-Burk: slope changes, y-intercept changes, x-intercept UNCHANGED

# ── Test parameters ───────────────────────────────────────────────────────
VMAX = 100.0   # μmol/min
KM   = 5.0     # mM
KI   = 10.0    # mM (inhibitor dissociation constant)
I    = 10.0    # mM (inhibitor concentration)

# Inhibition factor: alpha = 1 + [I]/Ki = 1 + 10/10 = 2
ALPHA = 1.0 + I / KI   # 2.0
assert math.isclose(ALPHA, 2.0, rel_tol=1e-9)

# ── Competitive: apparent Km = Km * alpha, Vmax unchanged ────────────────
COMPETITIVE_KM_APP  = KM * ALPHA           # 10.0
COMPETITIVE_VMAX    = VMAX                  # 100.0 (unchanged!)

# v_comp = Vmax*[S] / (Km_app + [S]) = 100*[S] / (10 + [S])
V_COMPETITIVE_AT_5  = VMAX * 5.0 / (COMPETITIVE_KM_APP + 5.0)   # 100*5/15 = 33.333...
V_COMPETITIVE_AT_10 = VMAX * 10.0 / (COMPETITIVE_KM_APP + 10.0) # 100*10/20 = 50.0
V_COMPETITIVE_AT_20 = VMAX * 20.0 / (COMPETITIVE_KM_APP + 20.0) # 100*20/30 = 66.667

assert math.isclose(COMPETITIVE_KM_APP, 10.0, rel_tol=1e-9)
assert math.isclose(V_COMPETITIVE_AT_5, 100.0 / 3.0, rel_tol=1e-9)
assert math.isclose(V_COMPETITIVE_AT_10, 50.0, rel_tol=1e-9)

# ── Uncompetitive: apparent Km = Km / alpha, apparent Vmax = Vmax / alpha ─
UNCOMPETITIVE_KM_APP   = KM / ALPHA        # 2.5  (DECREASES — common LLM error!)
UNCOMPETITIVE_VMAX_APP = VMAX / ALPHA      # 50.0

# v_uncomp = Vmax_app*[S] / (Km_app + [S]) = 50*[S] / (2.5 + [S])
V_UNCOMPETITIVE_AT_5  = VMAX * 5.0 / (KM + 5.0 * ALPHA)        # 100*5/(5+10) = 33.333...
V_UNCOMPETITIVE_AT_10 = VMAX * 10.0 / (KM + 10.0 * ALPHA)      # 100*10/(5+20) = 40.0
V_UNCOMPETITIVE_AT_20 = VMAX * 20.0 / (KM + 20.0 * ALPHA)      # 100*20/(5+40) = 44.444...

assert math.isclose(UNCOMPETITIVE_KM_APP, 2.5, rel_tol=1e-9)
assert math.isclose(UNCOMPETITIVE_VMAX_APP, 50.0, rel_tol=1e-9)
assert UNCOMPETITIVE_KM_APP < KM, "Uncompetitive Km_app must DECREASE (not increase!)"
assert math.isclose(V_UNCOMPETITIVE_AT_5, 100.0 / 3.0, rel_tol=1e-9)
assert math.isclose(V_UNCOMPETITIVE_AT_10, 40.0, rel_tol=1e-9)

# ── Noncompetitive: Km unchanged, apparent Vmax = Vmax / alpha ────────────
NONCOMPETITIVE_KM      = KM               # 5.0 (unchanged)
NONCOMPETITIVE_VMAX_APP = VMAX / ALPHA     # 50.0

# v_noncomp = Vmax_app*[S] / (Km + [S]) = 50*[S] / (5 + [S])
V_NONCOMPETITIVE_AT_5  = VMAX * 5.0 / ((KM + 5.0) * ALPHA)     # 100*5/(10*2) = 25.0
V_NONCOMPETITIVE_AT_10 = VMAX * 10.0 / ((KM + 10.0) * ALPHA)   # 100*10/(15*2) = 33.333...
V_NONCOMPETITIVE_AT_20 = VMAX * 20.0 / ((KM + 20.0) * ALPHA)   # 100*20/(25*2) = 40.0

assert math.isclose(NONCOMPETITIVE_KM, KM, rel_tol=1e-9)
assert math.isclose(NONCOMPETITIVE_VMAX_APP, 50.0, rel_tol=1e-9)
assert math.isclose(V_NONCOMPETITIVE_AT_5, 25.0, rel_tol=1e-9)
assert math.isclose(V_NONCOMPETITIVE_AT_10, 100.0 / 3.0, rel_tol=1e-9)

# ── Uninhibited baseline for comparison ───────────────────────────────────
V_UNINHIBITED_AT_5  = VMAX * 5.0 / (KM + 5.0)    # 50.0
V_UNINHIBITED_AT_10 = VMAX * 10.0 / (KM + 10.0)  # 66.667

assert math.isclose(V_UNINHIBITED_AT_5, 50.0, rel_tol=1e-9)

# ── Lineweaver-Burk properties ────────────────────────────────────────────
# Uninhibited:    slope = Km/Vmax,           y-int = 1/Vmax,       x-int = -1/Km
# Competitive:    slope = Km*alpha/Vmax,     y-int = 1/Vmax,       x-int = -1/(Km*alpha)
# Uncompetitive:  slope = Km/Vmax (same!),   y-int = alpha/Vmax,   x-int = -alpha/Km
# Noncompetitive: slope = Km*alpha/Vmax,     y-int = alpha/Vmax,   x-int = -1/Km (same!)

LB_UNINHIBITED_SLOPE = KM / VMAX                        # 0.05
LB_UNINHIBITED_YINT  = 1.0 / VMAX                       # 0.01
LB_UNINHIBITED_XINT  = -1.0 / KM                        # -0.2

LB_COMPETITIVE_SLOPE = KM * ALPHA / VMAX                # 0.10 (changes)
LB_COMPETITIVE_YINT  = 1.0 / VMAX                       # 0.01 (same!)
LB_COMPETITIVE_XINT  = -1.0 / (KM * ALPHA)              # -0.10 (changes)

LB_UNCOMPETITIVE_SLOPE = KM / VMAX                      # 0.05 (same!)
LB_UNCOMPETITIVE_YINT  = ALPHA / VMAX                   # 0.02 (changes)
LB_UNCOMPETITIVE_XINT  = -ALPHA / KM                    # -0.40 (changes)

LB_NONCOMPETITIVE_SLOPE = KM * ALPHA / VMAX             # 0.10 (changes)
LB_NONCOMPETITIVE_YINT  = ALPHA / VMAX                  # 0.02 (changes)
LB_NONCOMPETITIVE_XINT  = -1.0 / KM                     # -0.20 (same!)

assert math.isclose(LB_COMPETITIVE_SLOPE, 0.10, rel_tol=1e-9)
assert math.isclose(LB_COMPETITIVE_YINT, LB_UNINHIBITED_YINT, rel_tol=1e-9), \
    "Competitive: y-intercept must be UNCHANGED"
assert math.isclose(LB_UNCOMPETITIVE_SLOPE, LB_UNINHIBITED_SLOPE, rel_tol=1e-9), \
    "Uncompetitive: slope must be UNCHANGED"
assert math.isclose(LB_NONCOMPETITIVE_XINT, LB_UNINHIBITED_XINT, rel_tol=1e-9), \
    "Noncompetitive: x-intercept must be UNCHANGED"

# ── Prior LLM errors ─────────────────────────────────────────────────────
PRIOR_ERRORS = {
    "competitive_changes_vmax":   "Claims competitive inhibition changes Vmax (it does NOT — only Km changes)",
    "uncompetitive_increases_km": "Claims uncompetitive inhibition increases Km (it actually DECREASES apparent Km)",
    "lb_intercepts_swapped":      "Swaps which L-B intercepts change for competitive vs uncompetitive inhibition",
}
