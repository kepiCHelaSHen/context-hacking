"""cat-bio-hardy-weinberg — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_hardy_weinberg_constants import *
IMPL = Path(__file__).parent.parent / "bio_hardy_weinberg.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_heterozygote_is_2pq_not_pq(self):
        """The #1 LLM error: using pq instead of 2pq for heterozygotes."""
        m = _i()
        _, het, _ = m.genotype_frequencies(P)
        assert math.isclose(het, FREQ_Aa, rel_tol=1e-9), f"Het should be 2pq={FREQ_Aa}, got {het}"
        assert not math.isclose(het, WRONG_Aa), f"Got pq={WRONG_Aa} — missing factor of 2!"

    def test_frequencies_sum_to_one(self):
        """Genotype frequencies must always sum to 1.0."""
        m = _i()
        freqs = m.genotype_frequencies(P)
        assert math.isclose(sum(freqs), 1.0, rel_tol=1e-9), f"Sum={sum(freqs)}, expected 1.0"

class TestCorrectness:
    def test_genotype_frequencies_values(self):
        m = _i()
        aa, ab, bb = m.genotype_frequencies(P)
        assert math.isclose(aa, FREQ_AA, rel_tol=1e-9)
        assert math.isclose(ab, FREQ_Aa, rel_tol=1e-9)
        assert math.isclose(bb, FREQ_aa, rel_tol=1e-9)

    def test_allele_freq_back_calculation(self):
        """From genotype counts back to allele frequencies."""
        m = _i()
        # 100 individuals: 36 AA, 48 Aa, 16 aa → p=0.6, q=0.4
        p, q = m.allele_freq_from_genotypes(36, 48, 16)
        assert math.isclose(p, P, rel_tol=1e-9), f"p={p}, expected {P}"
        assert math.isclose(q, Q, rel_tol=1e-9), f"q={q}, expected {Q}"

    def test_hw_expected_counts(self):
        m = _i()
        exp = m.hw_expected(P, 100)
        assert math.isclose(exp[0], 36.0, rel_tol=1e-9)
        assert math.isclose(exp[1], 48.0, rel_tol=1e-9)
        assert math.isclose(exp[2], 16.0, rel_tol=1e-9)

    def test_is_equilibrium_exact(self):
        """Observed exactly equals expected → in equilibrium."""
        m = _i()
        obs = (36, 48, 16)
        exp = m.hw_expected(P, 100)
        assert m.is_equilibrium(obs, exp) is True

    def test_is_equilibrium_deviation(self):
        """Large deviation from expected → not in equilibrium."""
        m = _i()
        obs = (60, 20, 20)  # wildly off from (36, 48, 16)
        exp = m.hw_expected(P, 100)
        assert m.is_equilibrium(obs, exp) is False

    def test_symmetry_p_q(self):
        """genotype_frequencies(p) and genotype_frequencies(1-p) should give swapped AA/aa."""
        m = _i()
        aa1, ab1, bb1 = m.genotype_frequencies(0.3)
        aa2, ab2, bb2 = m.genotype_frequencies(0.7)
        assert math.isclose(aa1, bb2, rel_tol=1e-9)
        assert math.isclose(bb1, aa2, rel_tol=1e-9)
        assert math.isclose(ab1, ab2, rel_tol=1e-9)
