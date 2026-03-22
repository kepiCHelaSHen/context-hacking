"""F-Distribution / One-Way ANOVA — CHP Statistics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_f_dist_constants import *


def ss_between(group_means, overall_mean, n_per_group):
    """SSB = n * sum((mean_i - overall_mean)^2)"""
    return n_per_group * sum((m - overall_mean) ** 2 for m in group_means)


def ss_within_from_total(ss_total, ss_between):
    """SSW = SST - SSB"""
    return ss_total - ss_between


def ms(ss, df):
    """Mean Square = SS / df"""
    return ss / df


def f_statistic(msb, msw):
    """F = MSB / MSW  (between over within, NOT inverted)"""
    return msb / msw


def anova_df(k, N):
    """Return (df_between, df_within) = (k-1, N-k)"""
    return (k - 1, N - k)


if __name__ == "__main__":
    ssb = ss_between(GROUP_MEANS, OVERALL_MEAN, N_PER_GROUP)
    df_b, df_w = anova_df(K_GROUPS, N_TOTAL)
    msb = ms(ssb, df_b)
    msw = ms(SSW, df_w)
    F = f_statistic(msb, msw)
    print(f"SSB={ssb:.1f}  df_between={df_b}  df_within={df_w}")
    print(f"MSB={msb:.1f}  MSW={msw:.1f}  F={F:.2f}")
    print(f"F_crit(0.05,{df_b},{df_w})={F_CRIT_005}  -> {'Reject' if F > F_CRIT_005 else 'Fail to reject'} H0")
