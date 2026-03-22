"""cat-bio-codon-table — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_codon_table_constants import *
IMPL = Path(__file__).parent.parent / "bio_codon_table.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Guard against known LLM errors from PRIOR_ERRORS."""

    def test_exactly_3_stop_codons(self):
        """wrong_stop_count: must be exactly 3 stop codons (UAA, UAG, UGA)."""
        m = _i()
        stops = [c for c, aa in CODON_TABLE.items() if aa == "*"]
        assert len(stops) == 3
        assert set(stops) == {"UAA", "UAG", "UGA"}
        # Also verify via function
        for sc in ("UAA", "UAG", "UGA"):
            assert m.is_stop_codon(sc)

    def test_only_AUG_is_start(self):
        """extra_start_codons: AUG is the ONLY standard eukaryotic start codon."""
        m = _i()
        assert m.is_start_codon("AUG")
        # These are NOT start codons in the standard eukaryotic code
        for non_start in ("GUG", "UUG", "CUG", "AUA", "AUU", "AUC"):
            assert not m.is_start_codon(non_start), f"{non_start} should NOT be a start codon"

    def test_UGA_is_stop_not_trp(self):
        """uga_not_stop: UGA is a stop codon, NOT tryptophan."""
        m = _i()
        assert m.is_stop_codon("UGA")
        assert m.codon_to_aa("UGA") == "*", "UGA must map to stop (*), not W"
        # Trp is ONLY UGG
        assert m.codon_to_aa("UGG") == "W"
        assert not m.is_stop_codon("UGG")


class TestCorrectness:
    """Verify core translation and counting logic."""

    def test_translate_aug_cuu_uaa(self):
        """AUG-CUU-UAA → Met-Leu-Stop → 'ML'"""
        m = _i()
        assert m.translate("AUGCUUUAA") == "ML"

    def test_codon_to_aa_samples(self):
        """Spot-check several codon-to-amino-acid mappings."""
        m = _i()
        checks = {
            "AUG": "M",  # Met (start)
            "UUU": "F",  # Phe
            "UUC": "F",  # Phe (degenerate)
            "CUU": "L",  # Leu
            "UGG": "W",  # Trp (only codon)
            "GAU": "D",  # Asp
            "AAA": "K",  # Lys
            "GGG": "G",  # Gly
            "UAA": "*",  # Stop (ochre)
            "UAG": "*",  # Stop (amber)
            "UGA": "*",  # Stop (opal)
        }
        for codon, expected in checks.items():
            assert m.codon_to_aa(codon) == expected, f"{codon} should map to {expected}"

    def test_61_sense_codons(self):
        """Standard genetic code has exactly 61 sense codons."""
        m = _i()
        assert m.count_sense_codons() == 61

    def test_leucine_has_6_codons(self):
        """Leu is encoded by 6 codons: UUA, UUG, CUU, CUC, CUA, CUG."""
        m = _i()
        leu_codons = [c for c, aa in CODON_TABLE.items() if aa == "L"]
        assert len(leu_codons) == 6
        assert set(leu_codons) == {"UUA", "UUG", "CUU", "CUC", "CUA", "CUG"}

    def test_total_64_codons(self):
        """Codon table must have exactly 64 entries."""
        assert len(CODON_TABLE) == 64

    def test_translate_stops_at_stop(self):
        """Translation should halt at the first stop codon."""
        m = _i()
        # AUG-UGG-UAG-GGG → Met-Trp-Stop → "MW" (GGG never read)
        assert m.translate("AUGUGGUAGGGG") == "MW"
