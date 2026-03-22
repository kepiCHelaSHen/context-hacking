"""
Shannon Diversity Index — species diversity calculations.

Ecology convention uses the NATURAL logarithm (ln), not log base 2.
Information theory uses log₂ (bits).  The two give different numbers.

Functions
---------
shannon_index(counts)   -> H'  using natural log  (ecology standard)
max_diversity(S)        -> H'_max = ln(S)
evenness(H, H_max)     -> J = H / H_max,  Pielou's evenness [0, 1]
shannon_log2(counts)    -> H   using log base 2   (information theory)
"""

from __future__ import annotations

import math
from typing import Sequence


def shannon_index(counts: Sequence[int | float]) -> float:
    """Compute Shannon-Wiener diversity index H' using natural log (ln).

    H' = -SUM(p_i * ln(p_i))

    Parameters
    ----------
    counts : sequence of non-negative numbers
        Abundance of each species.  Zero-count species are skipped
        (0 * ln(0) is taken as 0 by convention).

    Returns
    -------
    float  H' >= 0
    """
    total = sum(counts)
    if total <= 0:
        raise ValueError("Total abundance must be positive")
    H = 0.0
    for c in counts:
        if c < 0:
            raise ValueError(f"Counts must be non-negative, got {c}")
        if c == 0:
            continue
        p = c / total
        H -= p * math.log(p)          # natural log
    return H


def max_diversity(S: int) -> float:
    """Maximum possible Shannon diversity for S species.

    H'_max = ln(S)

    Parameters
    ----------
    S : int > 0
        Number of species.

    Returns
    -------
    float
    """
    if S <= 0:
        raise ValueError("Number of species must be positive")
    return math.log(S)                 # natural log


def evenness(H: float, H_max: float) -> float:
    """Pielou's evenness index J = H' / H'_max.

    Result is in [0, 1] when H' and H'_max use the same log base.

    Parameters
    ----------
    H : float
        Observed Shannon diversity.
    H_max : float
        Maximum Shannon diversity (ln S).

    Returns
    -------
    float in [0, 1]
    """
    if H_max <= 0:
        raise ValueError("H_max must be positive")
    J = H / H_max
    if J > 1.0 + 1e-9:
        raise ValueError(
            f"Evenness J = {J:.6f} > 1; check that H and H_max use the "
            "same logarithm base"
        )
    return min(J, 1.0)                # clamp tiny float overshoot


def shannon_log2(counts: Sequence[int | float]) -> float:
    """Compute Shannon index using log base 2 (information-theory convention).

    H = -SUM(p_i * log₂(p_i))

    This is provided for *comparison only*.  Ecology papers use ln.

    Parameters
    ----------
    counts : sequence of non-negative numbers

    Returns
    -------
    float  H >= 0
    """
    total = sum(counts)
    if total <= 0:
        raise ValueError("Total abundance must be positive")
    H = 0.0
    for c in counts:
        if c < 0:
            raise ValueError(f"Counts must be non-negative, got {c}")
        if c == 0:
            continue
        p = c / total
        H -= p * math.log2(p)         # log base 2
    return H
