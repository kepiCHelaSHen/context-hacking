"""IS-LM Model — Frozen Constants. Source: Blanchard Macroeconomics 8th Ed Ch 5. DO NOT MODIFY."""
# IS curve: r = (A - Y*(1 - c*(1-t))) / b   — slopes DOWN in (Y,r) space
# LM curve: r = (kY - M/P) / h              — slopes UP in (Y,r) space
# Equilibrium: Y* = (hA + bM/P) / (h*(1-c(1-t)) + bk)

# Parameters
A = 400       # autonomous spending (C0 + I0 + G)
c = 0.8       # marginal propensity to consume
t = 0.25      # tax rate
b = 25        # investment sensitivity to interest rate
k = 0.25      # income sensitivity of money demand
h = 50        # interest sensitivity of money demand
M_P = 200     # real money supply (M/P)

# Derived slopes
IS_SLOPE = -(1 - c * (1 - t)) / b    # = -0.016 (negative — IS slopes DOWN)
LM_SLOPE = k / h                       # = 0.005  (positive — LM slopes UP)

# Test: equilibrium
Y_STAR = (h * A + b * M_P) / (h * (1 - c * (1 - t)) + b * k)  # ≈ 952.381
R_STAR = (k * Y_STAR - M_P) / h                                  # ≈ 0.7619

# IS curve values at test points
IS_AT_0    = A / b                                  # r = 16.0  (Y=0)
IS_AT_1000 = (A - 1000 * (1 - c * (1 - t))) / b   # r = 0.0   (Y=1000)

# LM curve values at test points
LM_AT_0    = -M_P / h                # r = -4.0  (Y=0)
LM_AT_1000 = (k * 1000 - M_P) / h   # r = 1.0   (Y=1000)

PRIOR_ERRORS = {
    "is_slopes_up":             "Claims IS slopes upward in (Y,r) — it slopes DOWN (dr/dY < 0)",
    "lm_slopes_down":           "Claims LM slopes downward in (Y,r) — it slopes UP (dr/dY > 0)",
    "equilibrium_formula_wrong": "Wrong algebraic solution for IS-LM intersection",
}
