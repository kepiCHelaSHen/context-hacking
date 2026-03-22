"""Mendelian Ratios — Frozen Constants. Source: Griffiths Introduction to Genetic Analysis 12th Ed. DO NOT MODIFY."""
# Monohybrid cross Aa × Aa → genotype ratio 1:2:1 (AA : Aa : aa)
MONO_GENOTYPE = (0.25, 0.50, 0.25)   # AA, Aa, aa
# Phenotypic ratio with complete dominance: 3:1 (dominant : recessive)
MONO_PHENOTYPE = (0.75, 0.25)         # dominant (AA+Aa), recessive (aa)

# Dihybrid cross AaBb × AaBb → phenotype ratio 9:3:3:1
# A_B_ : A_bb : aaB_ : aabb = 9/16 : 3/16 : 3/16 : 1/16
DI_PHENOTYPE = (9/16, 3/16, 3/16, 1/16)

# Punnett square sizes
MONO_COMBOS = 4    # 2×2 for one locus
DI_COMBOS   = 16   # 4×4 for two loci

# Test case: n=160 offspring from dihybrid cross
N_TEST = 160
DI_EXPECTED_160 = [90.0, 30.0, 30.0, 10.0]  # 160 × (9/16, 3/16, 3/16, 1/16)

# LLM prior errors — common mistakes large language models make
PRIOR_ERRORS = {
    "dihybrid_3_1_1_1":         "Uses 3:1:1:1 instead of 9:3:3:1 for dihybrid phenotype",
    "monohybrid_1_1":           "Ignores heterozygotes in genotype, gives 1:1 instead of 1:2:1",
    "wrong_total_combinations": "Uses 8 instead of 16 combinations for dihybrid Punnett square",
}
