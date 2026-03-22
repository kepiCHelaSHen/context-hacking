"""Survival Analysis — Frozen Constants. Source: Kaplan & Meier 1958. DO NOT MODIFY."""
import math
# Kaplan-Meier estimator: S(t) = Π_{t_i≤t} (1 - d_i / n_i)
#   d_i = number of events (deaths) at time t_i
#   n_i = number at risk just before t_i
# Censored observations reduce n_i at the NEXT event time but are NOT events (d_i=0).

# Test dataset: (time, event) — event=1 death, event=0 censored
TIMES  = [1, 2, 3, 4, 5, 6, 8]
EVENTS = [1, 0, 1, 1, 0, 1, 1]
# 7 subjects total
#   t=1: n=7, d=1, S = 6/7                   ≈ 0.85714
#   t=2: censored — n drops from 6→5, no change to S
#   t=3: n=5, d=1, S = (6/7)*(4/5)           = 24/35 ≈ 0.68571
#   t=4: n=4, d=1, S = (24/35)*(3/4)         = 18/35 ≈ 0.51429
#   t=5: censored — n drops from 3→2, no change to S
#   t=6: n=2, d=1, S = (18/35)*(1/2)         = 9/35  ≈ 0.25714
#   t=8: n=1, d=1, S = (9/35)*(0/1)          = 0.0

S_AT_1 = 6 / 7                        # 0.8571428571428571
S_AT_3 = (6 / 7) * (4 / 5)           # 0.6857142857142857
S_AT_4 = (6 / 7) * (4 / 5) * (3 / 4) # 0.5142857142857142
S_AT_6 = (6 / 7) * (4 / 5) * (3 / 4) * (1 / 2)  # 0.2571428571428571
S_AT_8 = 0.0

# Wrong value if censored observations are treated as events
# t=2 WRONG: n=6, d=1(wrong!), S = (6/7)*(5/6) = 5/7 ≈ 0.71429
S_WRONG_AT_2 = (6 / 7) * (5 / 6)     # 0.7142857142857143

PRIOR_ERRORS = {
    "censored_as_events": "Treats censored subjects as having the event (d_i=1 instead of 0)",
    "wrong_at_risk":      "Doesn't reduce n_i after censoring (keeps n too high at later times)",
    "naive_proportion":   "Uses 1 - d/N instead of product-limit estimator",
}
