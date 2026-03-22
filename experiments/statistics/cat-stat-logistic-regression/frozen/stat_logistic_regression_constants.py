"""Logistic Regression — Frozen Constants. Source: Hosmer & Lemeshow. DO NOT MODIFY."""
import math

# Logistic function:  p = 1 / (1 + e^(-z))   where z = beta0 + beta1 * x
# Odds   = p / (1 - p)
# Log-odds = ln(p / (1 - p)) = z
# Odds ratio for a unit increase in x:  OR = e^(beta1)
#   NOT beta1 itself, NOT the probability ratio P(x+1)/P(x).

# --- Test parameters ---
BETA0 = -2.0
BETA1 = 0.5

# --- Worked example at x = 3 ---
# z = -2 + 0.5 * 3 = -0.5
# p = 1 / (1 + e^(0.5)) = 0.37754066879814546
# odds = p / (1-p) = 0.6065306597633104
# log_odds = ln(odds) = z = -0.5
Z_AT_X3 = -0.5
P_AT_X3 = 1.0 / (1.0 + math.exp(0.5))       # 0.37754066879814546
ODDS_AT_X3 = P_AT_X3 / (1.0 - P_AT_X3)      # 0.6065306597633104

# --- Worked example at x = 4 ---
# z = -2 + 0.5 * 4 = 0
# p = 1 / (1 + e^0) = 0.5
# odds = 0.5 / 0.5 = 1.0
Z_AT_X4 = 0.0
P_AT_X4 = 0.5
ODDS_AT_X4 = 1.0

# --- Odds ratio ---
# OR = e^(beta1) = e^0.5 = 1.6487212707001282
# Verification: ODDS_AT_X4 / ODDS_AT_X3 = 1.0 / 0.60653... = e^0.5  ✓
# Each unit increase in x MULTIPLIES the odds by OR = 1.649.
# It does NOT increase the probability by 0.5.
ODDS_RATIO = math.exp(BETA1)                  # 1.6487212707001282

# --- Common LLM errors this experiment targets ---
PRIOR_ERRORS = {
    "or_is_prob_ratio":       "Thinks OR = P(x+1) / P(x).  The probability ratio "
                              "at x=3→4 is 0.5/0.37754 = 1.3238, NOT e^0.5 = 1.6487.  "
                              "OR is the *odds* ratio, not the probability ratio.",
    "beta_is_prob_change":    "Treats beta1 as a probability change per unit x.  "
                              "Probability is non-linear in x; beta1=0.5 does NOT mean "
                              "each unit of x adds 0.5 to the probability.",
    "or_less_than_1_protective": "Does not understand that OR < 1 corresponds to a "
                                 "negative beta (protective factor), not an error.",
}
