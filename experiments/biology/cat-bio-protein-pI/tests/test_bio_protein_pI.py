"""cat-bio-protein-pI — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_protein_pI_constants import *
IMPL = Path(__file__).parent.parent / "bio_protein_pI.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_asp_pI_uses_two_lowest_pKa(self):
        """Asp pI must use the two LOWEST pKa values (pKa1 + pKaR), not (pKa1 + pKa2)."""
        m = _i()
        result = m.pI_acidic(ASP_PKA1, ASP_PKAR)
        assert math.isclose(result, ASP_PI, rel_tol=1e-9), (
            f"Asp pI should be (pKa1+pKaR)/2 = {ASP_PI}, got {result}"
        )
        # Must NOT match the wrong answer: (pKa1 + pKa2)/2
        assert not math.isclose(result, ASP_PI_WRONG, rel_tol=0.01), (
            f"Asp pI must NOT equal (pKa1+pKa2)/2 = {ASP_PI_WRONG} — "
            "that's the wrong pKa pair!"
        )

    def test_lys_pI_uses_two_highest_pKa(self):
        """Lys pI must use the two HIGHEST pKa values (pKa2 + pKaR), not (pKa1 + pKa2)."""
        m = _i()
        result = m.pI_basic(LYS_PKA2, LYS_PKAR)
        assert math.isclose(result, LYS_PI, rel_tol=1e-9), (
            f"Lys pI should be (pKa2+pKaR)/2 = {LYS_PI}, got {result}"
        )
        # Must NOT match the wrong answer: (pKa1 + pKa2)/2
        assert not math.isclose(result, LYS_PI_WRONG, rel_tol=0.01), (
            f"Lys pI must NOT equal (pKa1+pKa2)/2 = {LYS_PI_WRONG} — "
            "that's the wrong pKa pair!"
        )

    def test_acidic_pI_is_low(self):
        """Acidic amino acid pI must be well below 7 (typically 2.5-3.5)."""
        m = _i()
        result = m.pI_acidic(ASP_PKA1, ASP_PKAR)
        assert result < 4.0, (
            f"Acidic amino acid pI should be < 4.0, got {result}. "
            "Are you using the correct pKa pair?"
        )

    def test_basic_pI_is_high(self):
        """Basic amino acid pI must be well above 7 (typically 9-11)."""
        m = _i()
        result = m.pI_basic(LYS_PKA2, LYS_PKAR)
        assert result > 7.0, (
            f"Basic amino acid pI should be > 7.0, got {result}. "
            "Are you using the correct pKa pair?"
        )


class TestCorrectness:
    def test_gly_pI(self):
        """Glycine pI = (2.34 + 9.60) / 2 = 5.97."""
        m = _i()
        result = m.pI_simple(GLY_PKA1, GLY_PKA2)
        assert math.isclose(result, GLY_PI, rel_tol=1e-9), (
            f"Gly pI should be {GLY_PI}, got {result}"
        )

    def test_asp_pI(self):
        """Aspartate pI = (2.09 + 3.86) / 2 = 2.975."""
        m = _i()
        result = m.pI_acidic(ASP_PKA1, ASP_PKAR)
        assert math.isclose(result, ASP_PI, rel_tol=1e-9), (
            f"Asp pI should be {ASP_PI}, got {result}"
        )

    def test_lys_pI(self):
        """Lysine pI = (8.95 + 10.53) / 2 = 9.74."""
        m = _i()
        result = m.pI_basic(LYS_PKA2, LYS_PKAR)
        assert math.isclose(result, LYS_PI, rel_tol=1e-9), (
            f"Lys pI should be {LYS_PI}, got {result}"
        )

    def test_classify_neutral(self):
        """Amino acid with no ionizable side chain → neutral."""
        m = _i()
        assert m.classify_amino_acid(None, GLY_PKA1, GLY_PKA2) == "neutral"

    def test_classify_acidic(self):
        """Asp (pKaR < pKa2) → acidic."""
        m = _i()
        assert m.classify_amino_acid(ASP_PKAR, ASP_PKA1, ASP_PKA2) == "acidic"

    def test_classify_basic(self):
        """Lys (pKaR > pKa2) → basic."""
        m = _i()
        assert m.classify_amino_acid(LYS_PKAR, LYS_PKA1, LYS_PKA2) == "basic"

    def test_simple_pI_is_average(self):
        """pI_simple must return the arithmetic mean of pKa1 and pKa2."""
        m = _i()
        # Use arbitrary values to confirm formula
        result = m.pI_simple(2.0, 10.0)
        assert math.isclose(result, 6.0, rel_tol=1e-9), (
            f"pI_simple(2.0, 10.0) should be 6.0, got {result}"
        )

    def test_acidic_pI_is_average_of_two_lowest(self):
        """pI_acidic must return the arithmetic mean of the two lowest pKa values."""
        m = _i()
        result = m.pI_acidic(2.0, 4.0)
        assert math.isclose(result, 3.0, rel_tol=1e-9), (
            f"pI_acidic(2.0, 4.0) should be 3.0, got {result}"
        )

    def test_basic_pI_is_average_of_two_highest(self):
        """pI_basic must return the arithmetic mean of the two highest pKa values."""
        m = _i()
        result = m.pI_basic(9.0, 11.0)
        assert math.isclose(result, 10.0, rel_tol=1e-9), (
            f"pI_basic(9.0, 11.0) should be 10.0, got {result}"
        )
