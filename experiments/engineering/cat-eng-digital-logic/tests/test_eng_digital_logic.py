"""cat-eng-digital-logic — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_digital_logic_constants import *
IMPL = Path(__file__).parent.parent / "eng_digital_logic.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Guard against known LLM mistakes."""

    def test_demorgan_nand_correct(self):
        """NOT(A AND B) must equal (NOT A) OR (NOT B), not AND."""
        m = _i()
        a, b = DEMORGAN_NAND_TEST["a"], DEMORGAN_NAND_TEST["b"]
        assert m.demorgan_nand(a, b) == DEMORGAN_NAND_TEST["correct"]

    def test_demorgan_nand_not_wrong(self):
        """Catch the classic error: NOT(A AND B) != NOT(A) AND NOT(B)."""
        m = _i()
        a, b = DEMORGAN_NAND_TEST["a"], DEMORGAN_NAND_TEST["b"]
        wrong_answer = (not a) and (not b)
        correct = m.demorgan_nand(a, b)
        assert correct != wrong_answer, "De Morgan NAND matches the WRONG formula!"

    def test_demorgan_nor_correct(self):
        """NOT(A OR B) must equal (NOT A) AND (NOT B)."""
        m = _i()
        a, b = DEMORGAN_NOR_TEST["a"], DEMORGAN_NOR_TEST["b"]
        assert m.demorgan_nor(a, b) == DEMORGAN_NOR_TEST["correct"]

    def test_dont_care_not_forced(self):
        """Don't-cares are optional — verify simplification works without forcing them."""
        m = _i()
        # Our function has no don't-cares, so simplify should still find single var
        result = m.simplify_single_var(MINTERMS, N_VARS)
        assert result == SIMPLIFIED, f"Expected '{SIMPLIFIED}', got '{result}'"

    def test_sop_evaluation_matches_truth_table(self):
        """SOP evaluator must match the frozen truth table exactly."""
        m = _i()
        for inputs, expected in TRUTH_TABLE.items():
            assert m.evaluate_sop(MINTERMS, N_VARS, inputs) == bool(expected), \
                f"SOP mismatch at {inputs}: got {not bool(expected)}, expected {bool(expected)}"


class TestCorrectness:
    """Verify core logic functions."""

    def test_simplify_to_single_variable(self):
        m = _i()
        assert m.simplify_single_var(MINTERMS, N_VARS) == SIMPLIFIED

    def test_sop_all_minterms_true(self):
        """Every minterm in the set must evaluate to True."""
        m = _i()
        for mt in MINTERMS:
            bits = tuple((mt >> (N_VARS - 1 - i)) & 1 for i in range(N_VARS))
            assert m.evaluate_sop(MINTERMS, N_VARS, bits) is True, f"Minterm {mt} ({bits}) should be True"

    def test_sop_non_minterms_false(self):
        """All non-minterms must evaluate to False."""
        m = _i()
        all_terms = set(range(1 << N_VARS))
        non_minterms = all_terms - set(MINTERMS)
        for mt in non_minterms:
            bits = tuple((mt >> (N_VARS - 1 - i)) & 1 for i in range(N_VARS))
            assert m.evaluate_sop(MINTERMS, N_VARS, bits) is False, f"Non-minterm {mt} ({bits}) should be False"

    def test_demorgan_nand_all_combos(self):
        """NAND De Morgan across all 4 input combos."""
        m = _i()
        for a in (True, False):
            for b in (True, False):
                assert m.demorgan_nand(a, b) == (not (a and b)), f"NAND failed for ({a},{b})"

    def test_demorgan_nor_all_combos(self):
        """NOR De Morgan across all 4 input combos."""
        m = _i()
        for a in (True, False):
            for b in (True, False):
                assert m.demorgan_nor(a, b) == (not (a or b)), f"NOR failed for ({a},{b})"

    def test_non_single_var_returns_none(self):
        """A function that doesn't reduce to one variable should return None."""
        m = _i()
        # F(A,B,C) = Σm(0,1) — depends on A AND B, not single var
        result = m.simplify_single_var((0, 1), 3)
        # m0=000, m1=001: A=0,B=0 always — NOT a single variable function
        assert result is None or result.startswith("NOT"), \
            f"Expected None for multi-var function, got '{result}'"
