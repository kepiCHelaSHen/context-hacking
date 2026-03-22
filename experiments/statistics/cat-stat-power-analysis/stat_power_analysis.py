"""Power Analysis — sample size determination for a two-sample t-test.

Implements the classical normal-approximation formula from Cohen (1988).
The key step that LLMs frequently get wrong is *standardising* the effect
size: the formula requires Cohen's d = Delta / sigma, NOT the raw
difference Delta.
"""

import math


def cohens_d(delta: float, sigma: float) -> float:
    """Return the standardised effect size d = Delta / sigma_pooled.

    Parameters
    ----------
    delta : float
        Raw mean difference (mu1 - mu2).
    sigma : float
        Pooled standard deviation (must be > 0).

    Returns
    -------
    float
        Cohen's d (dimensionless).
    """
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    return delta / sigma


def sample_size_per_group(d: float, z_alpha2: float, z_beta: float) -> int:
    """Required n *per group* for a two-sample t-test (equal groups).

    Formula
    -------
    n = ceil( ((z_{alpha/2} + z_{beta})^2 * 2) / d^2 )

    Parameters
    ----------
    d : float
        Cohen's d (standardised effect size, must be > 0).
    z_alpha2 : float
        Critical z-value for the chosen alpha (two-tailed).
    z_beta : float
        z-value corresponding to the desired power.

    Returns
    -------
    int
        Sample size per group, rounded up to the next integer.
    """
    if d <= 0:
        raise ValueError("effect size d must be positive")
    return math.ceil(((z_alpha2 + z_beta) ** 2 * 2) / d ** 2)


def total_sample_size(n_per_group: int) -> int:
    """Total sample size for a two-group design.

    Parameters
    ----------
    n_per_group : int
        Sample size in each group.

    Returns
    -------
    int
        Total n across both groups.
    """
    return 2 * n_per_group


def effect_size_category(d: float) -> str:
    """Classify an absolute Cohen's d using Cohen's conventions.

    Returns
    -------
    str
        ``"small"`` if |d| < 0.5, ``"medium"`` if 0.5 <= |d| < 0.8,
        ``"large"`` if |d| >= 0.8.
    """
    abs_d = abs(d)
    if abs_d < 0.5:
        return "small"
    elif abs_d < 0.8:
        return "medium"
    else:
        return "large"
