"""Bayes' Theorem — CHP Statistics Sprint.  All constants from frozen spec."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_bayes_theorem_constants import *


def prior_times_likelihood(prior, likelihood):
    """Numerator of Bayes' theorem: P(B|A) · P(A).

    This is NOT the posterior — it must still be divided by P(B).
    """
    return prior * likelihood


def total_probability(p_b_given_a, p_a, p_b_given_not_a):
    """Law of total probability (binary partition):
    P(B) = P(B|A)·P(A) + P(B|¬A)·P(¬A).
    """
    p_not_a = 1.0 - p_a
    return p_b_given_a * p_a + p_b_given_not_a * p_not_a


def posterior(prior, likelihood, p_evidence):
    """Bayes' theorem: P(A|B) = P(B|A)·P(A) / P(B).

    Parameters
    ----------
    prior      : P(A)
    likelihood : P(B|A)
    p_evidence : P(B)  — the normalizing constant
    """
    return (likelihood * prior) / p_evidence


def bayes_full(p_a, p_b_given_a, p_b_given_not_a):
    """Full posterior computation from priors and likelihoods.

    1. Compute P(B) via total_probability.
    2. Apply Bayes' theorem.
    """
    p_b = total_probability(p_b_given_a, p_a, p_b_given_not_a)
    return posterior(p_a, p_b_given_a, p_b)


if __name__ == "__main__":
    print("Bayes' Theorem — Medical Screening Demo\n")
    print(f"  P(D)   = {P_DISEASE}")
    print(f"  P(+|D) = {SENSITIVITY}   (sensitivity)")
    print(f"  P(+|¬D)= {FPR}          (false-positive rate)")
    p_pos = total_probability(SENSITIVITY, P_DISEASE, FPR)
    print(f"\n  P(+)   = {p_pos:.4f}")
    post = bayes_full(P_DISEASE, SENSITIVITY, FPR)
    print(f"  P(D|+) = {post:.10f}  (correct posterior)")
    wrong = prior_times_likelihood(P_DISEASE, SENSITIVITY)
    print(f"  Unnorm = {wrong:.10f}  (numerator only — WRONG)")
    print(f"\n  Ratio correct/wrong = {post / wrong:.2f}×")
