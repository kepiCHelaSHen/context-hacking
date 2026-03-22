"""Survival Analysis — CHP Statistics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_survival_analysis_constants import *


def at_risk(n, censored_before):
    """Adjust number at risk by subtracting censored observations before this event time."""
    return n - censored_before


def kaplan_meier(times, events):
    """Compute Kaplan-Meier survival curve.

    Parameters
    ----------
    times : list[int|float]
        Observation times (must be sorted ascending).
    events : list[int]
        1 = event (death), 0 = censored.

    Returns
    -------
    list[tuple[int|float, float]]
        List of (time, survival_probability) for each observation time.
        Censored times are included with the same S as before (no drop).
    """
    n = len(times)
    survival = 1.0
    curve = []
    at_risk_count = n  # everyone starts at risk

    for i in range(n):
        t = times[i]
        e = events[i]
        if e == 1:
            # Event: S drops
            survival *= (1 - 1 / at_risk_count)
            curve.append((t, survival))
            at_risk_count -= 1
        else:
            # Censored: S stays the same, but one fewer at risk going forward
            curve.append((t, survival))
            at_risk_count -= 1

    return curve


def survival_at_time(km_curve, t):
    """Look up S(t) from a Kaplan-Meier curve.

    Returns the survival probability at the latest event time <= t.
    If t is before the first observation, returns 1.0.
    """
    s = 1.0
    for time_i, surv_i in km_curve:
        if time_i <= t:
            s = surv_i
        else:
            break
    return s


if __name__ == "__main__":
    curve = kaplan_meier(TIMES, EVENTS)
    print("Kaplan-Meier survival curve:")
    for t, s in curve:
        tag = "" if EVENTS[TIMES.index(t)] == 1 else " (censored)"
        print(f"  t={t}: S(t) = {s:.5f}{tag}")
