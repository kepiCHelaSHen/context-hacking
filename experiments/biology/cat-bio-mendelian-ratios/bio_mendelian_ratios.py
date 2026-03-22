"""Mendelian Ratios — CHP Biology Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from bio_mendelian_ratios_constants import MONO_GENOTYPE, MONO_PHENOTYPE, DI_PHENOTYPE


def monohybrid_ratio():
    """Genotype ratio for Aa × Aa: (P(AA), P(Aa), P(aa)) = (0.25, 0.50, 0.25)."""
    return MONO_GENOTYPE


def monohybrid_phenotype():
    """Phenotype ratio for Aa × Aa with complete dominance: (P(dom), P(rec)) = (0.75, 0.25)."""
    return MONO_PHENOTYPE


def dihybrid_phenotype():
    """Phenotype ratio for AaBb × AaBb: (9/16, 3/16, 3/16, 1/16)."""
    return DI_PHENOTYPE


def expected_counts(ratios, n):
    """Given a tuple of proportions and a sample size n, return expected counts."""
    return [r * n for r in ratios]


def punnett_2x2(alleles1, alleles2):
    """All combinations from two parents' gamete allele lists.

    For monohybrid: alleles1 = alleles2 = ['A', 'a'] → 4 combos.
    For dihybrid:   alleles1 = alleles2 = ['AB', 'Ab', 'aB', 'ab'] → 16 combos.
    Returns list of (gamete1, gamete2) tuples.
    """
    return [(a1, a2) for a1 in alleles1 for a2 in alleles2]


if __name__ == "__main__":
    print("Monohybrid genotype (AA:Aa:aa):", monohybrid_ratio())
    print("Monohybrid phenotype (dom:rec):", monohybrid_phenotype())
    print("Dihybrid phenotype (A_B_:A_bb:aaB_:aabb):", dihybrid_phenotype())
    print(f"Dihybrid expected counts (n=160): {expected_counts(dihybrid_phenotype(), 160)}")
    mono = punnett_2x2(["A", "a"], ["A", "a"])
    print(f"Monohybrid Punnett ({len(mono)} combos): {mono}")
    di = punnett_2x2(["AB", "Ab", "aB", "ab"], ["AB", "Ab", "aB", "ab"])
    print(f"Dihybrid Punnett ({len(di)} combos)")
