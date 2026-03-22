"""Phillips Curve — Frozen Constants. Source: Blanchard Macroeconomics 8th Ed, Friedman 1968 AER. DO NOT MODIFY."""
# Short-run Phillips curve: π = πᵉ - β(u - uₙ)
#   π   = actual inflation rate (%)
#   πᵉ  = expected inflation rate (%)
#   β   = slope parameter (responsiveness of inflation to unemployment gap)
#   u   = actual unemployment rate (%)
#   uₙ  = natural rate of unemployment (NAIRU)
#
# Long-run: when u = uₙ, π = πᵉ  →  NO tradeoff!  Curve is VERTICAL.
# LLM prior: assumes stable long-run tradeoff (Friedman/Phelps proved this WRONG in 1968)

# Test parameters
BETA = 0.5       # slope of short-run Phillips curve
U_N = 5.0        # natural rate of unemployment (NAIRU), %
PI_E = 2.0       # expected inflation, %

# Test cases: π = πᵉ - β(u - uₙ) = 2 - 0.5*(u - 5)
# u=3%: π = 2 - 0.5*(3-5) = 2 - (-1) = 3%  (below NAIRU → higher inflation)
PI_AT_U3 = PI_E - BETA * (3.0 - U_N)   # = 3.0
# u=5%: π = 2 - 0.5*(5-5) = 2%              (at NAIRU → inflation = expected)
PI_AT_U5 = PI_E - BETA * (5.0 - U_N)   # = 2.0
# u=7%: π = 2 - 0.5*(7-5) = 2 - 1 = 1%     (above NAIRU → lower inflation)
PI_AT_U7 = PI_E - BETA * (7.0 - U_N)   # = 1.0

# Long-run equilibrium: at u=uₙ, inflation = expected inflation
LONG_RUN_PI = PI_E  # = 2.0 (just returns πᵉ)

PRIOR_ERRORS = {
    "stable_long_run_tradeoff": "Claims permanent inflation-unemployment tradeoff exists (WRONG — long-run curve is vertical at uₙ)",
    "nairu_is_zero":            "Claims natural rate of unemployment = 0 (WRONG — NAIRU ≈ 4-6% in most economies)",
    "expectations_ignored":     "Omits πᵉ term from Phillips curve (WRONG — expectations-augmented form is essential)",
}
