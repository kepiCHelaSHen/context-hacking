"""cat-bio-mendelian-ratios — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_mendelian_ratios_constants import *
IMPL = Path(__file__).parent.parent / "bio_mendelian_ratios.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Tests that catch known LLM mistakes."""

    def test_dihybrid_is_9_3_3_1_not_3_1_1_1(self):
        """Dihybrid phenotype must be 9:3:3:1, not 3:1:1:1."""
        m = _i()
        ratios = m.dihybrid_phenotype()
        assert abs(ratios[0] - 9/16) < 1e-9, "First class should be 9/16, not 3/16"
        assert abs(sum(ratios) - 1.0) < 1e-9

    def test_dihybrid_not_equal_split(self):
        """Dihybrid phenotype must NOT be a uniform 4:4:4:4 split."""
        m = _i()
        ratios = m.dihybrid_phenotype()
        assert ratios[0] != ratios[3], "9/16 ≠ 1/16 — classes are not equal"

    def test_punnett_dihybrid_has_16_combinations(self):
        """Dihybrid Punnett must have 4×4 = 16 combinations, not 8."""
        m = _i()
        combos = m.punnett_2x2(["AB", "Ab", "aB", "ab"], ["AB", "Ab", "aB", "ab"])
        assert len(combos) == DI_COMBOS, f"Expected {DI_COMBOS}, got {len(combos)}"

    def test_monohybrid_genotype_not_1_1(self):
        """Monohybrid genotype ratio is 1:2:1, not 1:1 (must include heterozygotes)."""
        m = _i()
        ratios = m.monohybrid_ratio()
        assert len(ratios) == 3, "Must have 3 genotype classes (AA, Aa, aa)"
        assert abs(ratios[1] - 0.50) < 1e-9, "Heterozygote Aa should be 0.50"


class TestCorrectness:
    """Tests for numerical correctness."""

    def test_monohybrid_genotype_ratios(self):
        m = _i()
        ratios = m.monohybrid_ratio()
        assert abs(ratios[0] - MONO_GENOTYPE[0]) < 1e-9  # AA = 0.25
        assert abs(ratios[1] - MONO_GENOTYPE[1]) < 1e-9  # Aa = 0.50
        assert abs(ratios[2] - MONO_GENOTYPE[2]) < 1e-9  # aa = 0.25
        assert abs(sum(ratios) - 1.0) < 1e-9

    def test_monohybrid_phenotype_ratios(self):
        m = _i()
        ratios = m.monohybrid_phenotype()
        assert abs(ratios[0] - MONO_PHENOTYPE[0]) < 1e-9  # dominant = 0.75
        assert abs(ratios[1] - MONO_PHENOTYPE[1]) < 1e-9  # recessive = 0.25

    def test_dihybrid_expected_counts_n160(self):
        m = _i()
        counts = m.expected_counts(m.dihybrid_phenotype(), N_TEST)
        for got, want in zip(counts, DI_EXPECTED_160):
            assert abs(got - want) < 1e-9, f"Expected {want}, got {got}"

    def test_punnett_monohybrid_has_4_combinations(self):
        m = _i()
        combos = m.punnett_2x2(["A", "a"], ["A", "a"])
        assert len(combos) == MONO_COMBOS

    def test_expected_counts_sum(self):
        m = _i()
        counts = m.expected_counts(m.dihybrid_phenotype(), N_TEST)
        assert abs(sum(counts) - N_TEST) < 1e-9, "Expected counts must sum to n"
