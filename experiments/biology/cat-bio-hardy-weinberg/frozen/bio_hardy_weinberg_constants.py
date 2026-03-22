"""Hardy-Weinberg Equilibrium — Frozen Constants. Source: Hardy 1908, Weinberg 1908. DO NOT MODIFY."""
import math
# p + q = 1 (two alleles in a population)
# Genotype frequencies: p², 2pq, q² for AA, Aa, aa
# KEY: heterozygote frequency is 2pq, NOT pq
# Test: p=0.6, q=0.4
#   AA: p²=0.36, Aa: 2pq=0.48, aa: q²=0.16
#   Sum = 0.36 + 0.48 + 0.16 = 1.0 ✓
#   WRONG: if you use pq instead of 2pq → Aa=0.24, sum=0.76 ≠ 1
# Three-allele extension: p+q+r=1, freq(AB)=2pq (also 2× for each heterozygote)
P = 0.6
Q = 0.4
FREQ_AA = P ** 2                # 0.36
FREQ_Aa = 2 * P * Q            # 0.48
FREQ_aa = Q ** 2                # 0.16
WRONG_Aa = P * Q               # 0.24 (the common LLM mistake)
assert math.isclose(FREQ_AA + FREQ_Aa + FREQ_aa, 1.0), "HW frequencies must sum to 1"
assert not math.isclose(FREQ_AA + WRONG_Aa + FREQ_aa, 1.0), "Wrong het must NOT sum to 1"
PRIOR_ERRORS = {
    "het_pq_not_2pq":           "Uses pq instead of 2pq for heterozygotes",
    "sum_not_one":              "Genotype frequencies don't sum to 1",
    "allele_freq_from_genotype":"Wrong back-calculation of p from genotypes",
}
