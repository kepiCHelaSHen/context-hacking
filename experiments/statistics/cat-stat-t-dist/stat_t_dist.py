"""Student's t-Distribution — CHP Statistics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_t_dist_constants import *

def standard_error(s, n): return s / math.sqrt(n)
def degrees_of_freedom(n): return n - 1
def confidence_interval(xbar, s, n, t_crit):
    se = standard_error(s, n)
    return (round(xbar - t_crit * se, 3), round(xbar + t_crit * se, 3))
def t_statistic(xbar, mu0, s, n): return (xbar - mu0) / standard_error(s, n)

if __name__ == "__main__":
    se = standard_error(S_SAMPLE, N_SAMPLE)
    df = degrees_of_freedom(N_SAMPLE)
    ci = confidence_interval(XBAR, S_SAMPLE, N_SAMPLE, T_CRIT_24)
    print(f"n={N_SAMPLE}, df={df}, SE={se:.1f}")
    print(f"95% CI (df={df}): ({ci[0]:.3f}, {ci[1]:.3f})")
    t = t_statistic(XBAR, 95.0, S_SAMPLE, N_SAMPLE)
    print(f"t-stat vs mu0=95: {t:.4f}")
