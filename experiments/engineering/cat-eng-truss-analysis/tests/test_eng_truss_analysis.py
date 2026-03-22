"""cat-eng-truss-analysis — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_truss_analysis_constants import *
IMPL = Path(__file__).parent.parent / "eng_truss_analysis.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the known LLM failure modes."""

    def test_diagonal_is_compression(self):
        """Diagonal members must be in COMPRESSION (negative), NOT tension."""
        m = _i(); F = m.diagonal_force_equilateral(P_REF)
        assert F < 0, f"Diagonal force should be negative (compression), got {F}"
        assert m.is_compression(F), "is_compression should return True for diagonal"

    def test_diagonal_not_swapped_sign(self):
        """Diagonal must NOT have swapped sign (the #1 LLM error)."""
        m = _i(); F = m.diagonal_force_equilateral(P_REF)
        assert abs(F - F_DIAG_WRONG_SIGN) > 1.0, \
            f"Got {F}, which matches the WRONG (swapped) sign {F_DIAG_WRONG_SIGN}"

    def test_horizontal_is_tension(self):
        """Horizontal member must be in TENSION (positive), NOT compression."""
        m = _i(); F = m.horizontal_force_equilateral(P_REF)
        assert F > 0, f"Horizontal force should be positive (tension), got {F}"
        assert m.is_tension(F), "is_tension should return True for horizontal"

    def test_horizontal_not_swapped_sign(self):
        """Horizontal must NOT have swapped sign."""
        m = _i(); F = m.horizontal_force_equilateral(P_REF)
        assert abs(F - F_HORIZ_WRONG_SIGN) > 1.0, \
            f"Got {F}, which matches the WRONG (swapped) sign {F_HORIZ_WRONG_SIGN}"

    def test_reactions_are_half_load(self):
        """Reactions must be P/2, NOT P (common error: forgets to split)."""
        m = _i(); R_l, R_r = m.support_reactions_symmetric(P_REF)
        assert abs(R_l - R_LEFT_REF) < 1e-12, f"R_left should be {R_LEFT_REF}, got {R_l}"
        assert abs(R_r - R_RIGHT_REF) < 1e-12, f"R_right should be {R_RIGHT_REF}, got {R_r}"
        assert abs(R_l - R_WRONG_FULL_LOAD) > 1.0, "Using R = P instead of P/2!"

    def test_diagonal_not_from_wrong_reaction(self):
        """Diagonal force must not come from wrong reaction R=P."""
        m = _i(); F = m.diagonal_force_equilateral(P_REF)
        assert abs(F - F_DIAG_WRONG_REACTION) > 1.0, \
            f"Got {F}, which matches the result from wrong reaction (R=P)"


class TestCorrectness:
    """Verify numerical accuracy of all functions."""

    def test_reaction_values(self):
        m = _i(); R_l, R_r = m.support_reactions_symmetric(P_REF)
        assert abs(R_l - 5.0) < 1e-12
        assert abs(R_r - 5.0) < 1e-12

    def test_reactions_sum_to_load(self):
        """Both reactions must sum to applied load P."""
        m = _i(); R_l, R_r = m.support_reactions_symmetric(P_REF)
        assert abs(R_l + R_r - P_REF) < 1e-12

    def test_diagonal_force_value(self):
        m = _i(); F = m.diagonal_force_equilateral(P_REF)
        assert abs(F - F_DIAG_REF) / abs(F_DIAG_REF) < 1e-9, \
            f"Expected {F_DIAG_REF:.6f}, got {F:.6f}"

    def test_diagonal_equals_neg_P_over_sqrt3(self):
        """F_diag = -P/√3 for equilateral triangle."""
        m = _i(); F = m.diagonal_force_equilateral(P_REF)
        expected = -P_REF / math.sqrt(3)
        assert abs(F - expected) < 1e-9

    def test_horizontal_force_value(self):
        m = _i(); F = m.horizontal_force_equilateral(P_REF)
        assert abs(F - F_HORIZ_REF) / abs(F_HORIZ_REF) < 1e-9, \
            f"Expected {F_HORIZ_REF:.6f}, got {F:.6f}"

    def test_horizontal_equals_P_over_2sqrt3(self):
        """F_horiz = P/(2√3) for equilateral triangle."""
        m = _i(); F = m.horizontal_force_equilateral(P_REF)
        expected = P_REF / (2.0 * math.sqrt(3))
        assert abs(F - expected) < 1e-9

    def test_equilibrium_Fy_at_left_joint(self):
        """ΣFy = 0 at left support: R_left + F_diag * sin(60°) = 0."""
        m = _i()
        R_l, _ = m.support_reactions_symmetric(P_REF)
        F_d = m.diagonal_force_equilateral(P_REF)
        Fy = R_l + F_d * math.sin(math.radians(60.0))
        assert abs(Fy) < 1e-10, f"ΣFy should be 0, got {Fy}"

    def test_equilibrium_Fx_at_left_joint(self):
        """ΣFx = 0 at left support: F_horiz + F_diag * cos(60°) = 0."""
        m = _i()
        F_d = m.diagonal_force_equilateral(P_REF)
        F_h = m.horizontal_force_equilateral(P_REF)
        Fx = F_h + F_d * math.cos(math.radians(60.0))
        assert abs(Fx) < 1e-10, f"ΣFx should be 0, got {Fx}"

    def test_is_tension_positive(self):
        m = _i()
        assert m.is_tension(1.0) is True
        assert m.is_tension(-1.0) is False
        assert m.is_tension(0.0) is False

    def test_is_compression_negative(self):
        m = _i()
        assert m.is_compression(-1.0) is True
        assert m.is_compression(1.0) is False
        assert m.is_compression(0.0) is False

    def test_diagonal_proportional_to_load(self):
        """Doubling P should double diagonal force magnitude."""
        m = _i()
        F1 = m.diagonal_force_equilateral(P_REF)
        F2 = m.diagonal_force_equilateral(2.0 * P_REF)
        assert abs(F2 / F1 - 2.0) < 1e-12

    def test_horizontal_proportional_to_load(self):
        """Doubling P should double horizontal force."""
        m = _i()
        F1 = m.horizontal_force_equilateral(P_REF)
        F2 = m.horizontal_force_equilateral(2.0 * P_REF)
        assert abs(F2 / F1 - 2.0) < 1e-12

    def test_different_angle_45(self):
        """For 45° angle: F_diag = -P/(2 sin 45°), F_horiz = P/(2 tan 45°) = P/2."""
        m = _i()
        P = 10.0
        F_d = m.diagonal_force_equilateral(P, angle_deg=45.0)
        F_h = m.horizontal_force_equilateral(P, angle_deg=45.0)
        expected_d = -P / (2.0 * math.sin(math.radians(45.0)))
        expected_h = P / (2.0 * math.tan(math.radians(45.0)))
        assert abs(F_d - expected_d) < 1e-9
        assert abs(F_h - expected_h) < 1e-9
        assert abs(F_h - 5.0) < 1e-9, "At 45°, F_horiz should be P/2"
