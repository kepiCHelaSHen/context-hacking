"""cat-eng-feedback-stability — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_feedback_stability_constants import *
IMPL = Path(__file__).parent.parent / "eng_feedback_stability.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Tests targeting the 3 known LLM failure modes."""

    def test_sign_changes_counted_correctly_stable(self):
        """LLM error: miscounts sign changes. Stable column [1,2,1,4] has 0."""
        m = _i()
        assert m.count_sign_changes(STABLE_FIRST_COL) == STABLE_SIGN_CHANGES

    def test_sign_changes_counted_correctly_unstable(self):
        """LLM error: miscounts sign changes. [1,1,-6,8] has exactly 2."""
        m = _i()
        assert m.count_sign_changes(UNSTABLE_FIRST_COL) == UNSTABLE_SIGN_CHANGES

    def test_routh_array_intermediate_row_stable(self):
        """LLM error: wrong Routh row computation. Verify (a2*a1-a3*a0)/a2."""
        m = _i()
        fc = m.routh_array_3rd(STABLE_COEFFS)
        for i in range(4):
            assert abs(fc[i] - STABLE_FIRST_COL[i]) < 1e-10, \
                f"First column[{i}]: got {fc[i]}, expected {STABLE_FIRST_COL[i]}"

    def test_routh_array_intermediate_row_unstable(self):
        """LLM error: wrong Routh row computation. Row 1 must be -6."""
        m = _i()
        fc = m.routh_array_3rd(UNSTABLE_COEFFS)
        for i in range(4):
            assert abs(fc[i] - UNSTABLE_FIRST_COL[i]) < 1e-10, \
                f"First column[{i}]: got {fc[i]}, expected {UNSTABLE_FIRST_COL[i]}"

    def test_necessary_not_sufficient(self):
        """LLM error: claims all-positive-coefficients implies stability.
        s³+s²+2s+8 has all positive coefficients but is UNSTABLE."""
        m = _i()
        # Necessary condition passes (all coeffs positive)
        assert m.necessary_condition(UNSTABLE_COEFFS) is UNSTABLE_NECESSARY_PASSES
        # But the full Routh test says UNSTABLE
        assert m.is_stable_routh(UNSTABLE_COEFFS) is UNSTABLE_IS_STABLE


class TestRouthArray:
    def test_stable_first_column(self):
        m = _i()
        fc = m.routh_array_3rd(STABLE_COEFFS)
        assert fc == STABLE_FIRST_COL

    def test_unstable_first_column(self):
        m = _i()
        fc = m.routh_array_3rd(UNSTABLE_COEFFS)
        assert fc == UNSTABLE_FIRST_COL

    def test_stable2_first_column(self):
        m = _i()
        fc = m.routh_array_3rd(STABLE2_COEFFS)
        for i in range(4):
            assert abs(fc[i] - STABLE2_FIRST_COL[i]) < 1e-10

    def test_row1_formula_explicit(self):
        """Directly verify: row1 = (a2*a1 - a3*a0) / a2."""
        m = _i()
        a3, a2, a1, a0 = UNSTABLE_COEFFS
        expected_row1 = (a2 * a1 - a3 * a0) / a2
        fc = m.routh_array_3rd(UNSTABLE_COEFFS)
        assert abs(fc[2] - expected_row1) < 1e-10


class TestSignChanges:
    def test_all_positive(self):
        m = _i()
        assert m.count_sign_changes([1, 2, 3, 4]) == 0

    def test_two_changes(self):
        m = _i()
        assert m.count_sign_changes([1, 1, -6, 8]) == 2

    def test_one_change(self):
        m = _i()
        assert m.count_sign_changes([1, -1, -2, -3]) == 1

    def test_alternating_signs(self):
        """[1, -1, 1, -1] → 3 sign changes."""
        m = _i()
        assert m.count_sign_changes([1, -1, 1, -1]) == 3

    def test_single_element(self):
        m = _i()
        assert m.count_sign_changes([5]) == 0


class TestStability:
    def test_stable_system(self):
        m = _i()
        assert m.is_stable_routh(STABLE_COEFFS) is True

    def test_unstable_system(self):
        m = _i()
        assert m.is_stable_routh(UNSTABLE_COEFFS) is False

    def test_stable2_system(self):
        m = _i()
        assert m.is_stable_routh(STABLE2_COEFFS) is True


class TestNecessaryCondition:
    def test_all_positive_passes(self):
        m = _i()
        assert m.necessary_condition(STABLE_COEFFS) is True

    def test_negative_coeff_fails(self):
        m = _i()
        assert m.necessary_condition(NEG_COEFF_COEFFS) is False

    def test_unstable_with_positive_coeffs(self):
        """Key insight: [1,1,2,8] passes necessary but fails Routh."""
        m = _i()
        assert m.necessary_condition(UNSTABLE_COEFFS) is True
        assert m.is_stable_routh(UNSTABLE_COEFFS) is False
