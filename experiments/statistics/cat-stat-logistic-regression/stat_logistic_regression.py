"""Logistic Regression — CHP Statistics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_logistic_regression_constants import *


def logistic(z):
    """Logistic (sigmoid) function: p = 1 / (1 + e^(-z))."""
    return 1.0 / (1.0 + math.exp(-z))


def log_odds(p):
    """Log-odds (logit): ln(p / (1 - p))."""
    if p <= 0 or p >= 1:
        raise ValueError("p must be in (0, 1)")
    return math.log(p / (1.0 - p))


def odds(p):
    """Odds: p / (1 - p)."""
    if p < 0 or p >= 1:
        raise ValueError("p must be in [0, 1)")
    return p / (1.0 - p)


def odds_ratio(beta):
    """Odds ratio for a unit increase in x: OR = e^beta."""
    return math.exp(beta)


def predict_prob(beta0, beta1, x):
    """Predicted probability: logistic(beta0 + beta1 * x)."""
    return logistic(beta0 + beta1 * x)


if __name__ == "__main__":
    for x in range(0, 8):
        p = predict_prob(BETA0, BETA1, x)
        o = odds(p)
        print(f"x={x}  z={BETA0 + BETA1*x:+.2f}  p={p:.5f}  odds={o:.5f}")
    print(f"\nOdds ratio (e^beta1): {odds_ratio(BETA1):.10f}")
    print(f"Odds(x=4)/Odds(x=3): {odds(predict_prob(BETA0, BETA1, 4)) / odds(predict_prob(BETA0, BETA1, 3)):.10f}")
