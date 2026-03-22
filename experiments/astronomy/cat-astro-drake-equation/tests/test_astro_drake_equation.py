"""cat-astro-drake-equation — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_drake_equation_constants import *
IMPL = Path(__file__).parent.parent / "astro_drake_equation.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Tests that catch the known LLM errors."""

    def test_fp_not_low(self):
        """f_p should be ~1.0 (Kepler), NOT 0.1-0.5 (pre-Kepler)."""
        m = _i()
        fp = m.modern_f_p()
        assert fp >= 0.9, f"f_p = {fp} — should be ~1.0 (Kepler: nearly all stars have planets)"
        assert fp <= 1.1, f"f_p = {fp} — should be ~1.0, not >1"

    def test_fp_old_value_changes_result(self):
        """Using f_p=0.2 (old wrong value) gives 5x lower N than f_p=1.0."""
        m = _i()
        N_correct = m.drake_equation(f_p=1.0)
        N_wrong = m.drake_equation(f_p=F_P_OLD_WRONG)
        assert N_correct / N_wrong == pytest.approx(1.0 / F_P_OLD_WRONG, rel=0.01)

    def test_n_not_definite(self):
        """Drake Equation does NOT give a definite answer — range spans orders of magnitude."""
        m = _i()
        opt = m.optimistic_estimate()
        pess = m.pessimistic_estimate()
        ratio = opt["N"] / pess["N"]
        assert ratio > 1e6, f"Optimistic/pessimistic ratio = {ratio} — should be >1e6 (orders of magnitude)"

    def test_factors_not_all_well_known(self):
        """f_l, f_i, f_c, L span orders of magnitude — not narrowly constrained."""
        # Verify the frozen constants capture the enormous uncertainty
        assert F_L_HIGH / F_L_LOW >= 100, "f_l range should be >= 100x"
        assert F_I_HIGH / F_I_LOW >= 100, "f_i range should be >= 100x"
        assert F_C_HIGH / F_C_LOW >= 20, "f_c range should be >= 20x"
        assert L_HIGH / L_LOW >= 1e6, "L range should be >= 1e6"


class TestCorrectness:
    """Core correctness tests for Drake Equation functions."""

    def test_drake_equation_basic(self):
        """N = R* x f_p x n_e x f_l x f_i x f_c x L with all factors = 1."""
        m = _i()
        N = m.drake_equation(R_star=1, f_p=1, n_e=1, f_l=1, f_i=1, f_c=1, L=1)
        assert N == pytest.approx(1.0)

    def test_drake_equation_scaling(self):
        """Doubling any single factor should double N."""
        m = _i()
        N_base = m.drake_equation(R_star=1, f_p=1, n_e=1, f_l=1, f_i=1, f_c=1, L=1)
        N_double_R = m.drake_equation(R_star=2, f_p=1, n_e=1, f_l=1, f_i=1, f_c=1, L=1)
        assert N_double_R == pytest.approx(2.0 * N_base)

    def test_optimistic_estimate(self):
        """Optimistic: 2 * 1.0 * 0.2 * 1.0 * 0.5 * 0.1 * 10000 = 200."""
        m = _i()
        opt = m.optimistic_estimate()
        assert opt["N"] == pytest.approx(OPTIMISTIC_N, rel=1e-6)
        assert opt["R_star"] == pytest.approx(OPTIMISTIC_R_STAR)
        assert opt["f_p"] == pytest.approx(OPTIMISTIC_F_P)
        assert opt["n_e"] == pytest.approx(OPTIMISTIC_N_E)
        assert opt["f_l"] == pytest.approx(OPTIMISTIC_F_L)
        assert opt["f_i"] == pytest.approx(OPTIMISTIC_F_I)
        assert opt["f_c"] == pytest.approx(OPTIMISTIC_F_C)
        assert opt["L"] == pytest.approx(OPTIMISTIC_L)

    def test_pessimistic_estimate(self):
        """Pessimistic: 1.5 * 1.0 * 0.1 * 0.01 * 0.01 * 0.01 * 1000 = 0.00015."""
        m = _i()
        pess = m.pessimistic_estimate()
        assert pess["N"] == pytest.approx(PESSIMISTIC_N, rel=1e-6)
        assert pess["R_star"] == pytest.approx(PESSIMISTIC_R_STAR)
        assert pess["f_p"] == pytest.approx(PESSIMISTIC_F_P)

    def test_modern_fp(self):
        """modern_f_p() should return ~1.0."""
        m = _i()
        assert m.modern_f_p() == pytest.approx(F_P_MODERN)

    def test_drake_equation_optimistic_manual(self):
        """Manually compute the optimistic case via drake_equation()."""
        m = _i()
        N = m.drake_equation(
            R_star=OPTIMISTIC_R_STAR, f_p=OPTIMISTIC_F_P, n_e=OPTIMISTIC_N_E,
            f_l=OPTIMISTIC_F_L, f_i=OPTIMISTIC_F_I, f_c=OPTIMISTIC_F_C,
            L=OPTIMISTIC_L
        )
        assert N == pytest.approx(OPTIMISTIC_N, rel=1e-6)

    def test_drake_equation_pessimistic_manual(self):
        """Manually compute the pessimistic case via drake_equation()."""
        m = _i()
        N = m.drake_equation(
            R_star=PESSIMISTIC_R_STAR, f_p=PESSIMISTIC_F_P, n_e=PESSIMISTIC_N_E,
            f_l=PESSIMISTIC_F_L, f_i=PESSIMISTIC_F_I, f_c=PESSIMISTIC_F_C,
            L=PESSIMISTIC_L
        )
        assert N == pytest.approx(PESSIMISTIC_N, rel=1e-6)

    def test_drake_zero_factor(self):
        """If any factor is zero, N = 0."""
        m = _i()
        assert m.drake_equation(f_l=0) == 0.0
        assert m.drake_equation(L=0) == 0.0

    def test_optimistic_vs_pessimistic_order(self):
        """Optimistic N should be much greater than pessimistic N."""
        m = _i()
        opt = m.optimistic_estimate()
        pess = m.pessimistic_estimate()
        assert opt["N"] > pess["N"]
        log_ratio = math.log10(opt["N"] / pess["N"])
        assert log_ratio > 6, f"Should span >6 orders of magnitude, got {log_ratio:.1f}"

    def test_drake_defaults_use_modern_fp(self):
        """Default f_p in drake_equation should be ~1.0 (modern Kepler value)."""
        m = _i()
        # Call with just R_star to check that f_p defaults to modern value
        N_default = m.drake_equation(R_star=1, n_e=1, f_l=1, f_i=1, f_c=1, L=1)
        # With f_p=1.0, this should equal 1.0
        assert N_default == pytest.approx(1.0, rel=0.1)
