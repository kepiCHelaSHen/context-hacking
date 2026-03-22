"""cat-bio-genetic-drift — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_genetic_drift_constants import *
IMPL = Path(__file__).parent.parent / "bio_genetic_drift.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_fixation_is_p0_not_1_over_2N(self):
        """The #1 LLM error: using 1/(2N) as fixation prob instead of p0."""
        m = _i()
        p_fix = m.fixation_probability(P0)
        assert math.isclose(p_fix, P_FIX, rel_tol=1e-9), (
            f"P(fix) should be p0={P_FIX}, got {p_fix}"
        )
        assert not math.isclose(p_fix, WRONG_P_FIX, rel_tol=1e-3), (
            f"Got 1/(2N)={WRONG_P_FIX} — that's only for a NEW single-copy mutation!"
        )

    def test_heterozygosity_decays_over_time(self):
        """Heterozygosity must decay under drift — it does NOT stay constant."""
        m = _i()
        H_now = m.heterozygosity(P0)
        H_later = m.het_after_t(H_now, N, T_TEST)
        assert H_later < H_now, (
            f"H must decay: H(0)={H_now}, H({T_TEST})={H_later} — drift erodes heterozygosity"
        )


class TestCorrectness:
    def test_fixation_probability(self):
        """P(fixation) = p0 for neutral allele."""
        m = _i()
        assert math.isclose(m.fixation_probability(P0), P0, rel_tol=1e-9)
        assert math.isclose(m.fixation_probability(0.5), 0.5, rel_tol=1e-9)
        assert math.isclose(m.fixation_probability(0.0), 0.0, rel_tol=1e-9)
        assert math.isclose(m.fixation_probability(1.0), 1.0, rel_tol=1e-9)

    def test_heterozygosity_H0(self):
        """H0 = 2*p*q = 2*0.3*0.7 = 0.42."""
        m = _i()
        assert math.isclose(m.heterozygosity(P0), H0, rel_tol=1e-9), (
            f"H0 should be {H0}, got {m.heterozygosity(P0)}"
        )

    def test_het_after_100_generations(self):
        """H(100) = 0.42 * 0.99^100 ≈ 0.1537."""
        m = _i()
        result = m.het_after_t(H0, N, T_TEST)
        assert math.isclose(result, H_AFTER_T, rel_tol=1e-6), (
            f"H({T_TEST}) should be ~{H_AFTER_T:.4f}, got {result:.4f}"
        )

    def test_drift_variance(self):
        """Var(delta_p) = p*(1-p)/(2N) = 0.3*0.7/100 = 0.0021."""
        m = _i()
        result = m.drift_variance(P0, N)
        assert math.isclose(result, VARIANCE, rel_tol=1e-9), (
            f"Variance should be {VARIANCE}, got {result}"
        )

    def test_heterozygosity_boundary(self):
        """Heterozygosity is 0 at fixation (p=0 or p=1)."""
        m = _i()
        assert math.isclose(m.heterozygosity(0.0), 0.0, abs_tol=1e-12)
        assert math.isclose(m.heterozygosity(1.0), 0.0, abs_tol=1e-12)

    def test_heterozygosity_max_at_half(self):
        """Maximum heterozygosity is at p=0.5: H = 2*0.5*0.5 = 0.5."""
        m = _i()
        assert math.isclose(m.heterozygosity(0.5), 0.5, rel_tol=1e-9)

    def test_drift_variance_zero_at_fixation(self):
        """Variance is 0 when allele is fixed or lost."""
        m = _i()
        assert math.isclose(m.drift_variance(0.0, N), 0.0, abs_tol=1e-12)
        assert math.isclose(m.drift_variance(1.0, N), 0.0, abs_tol=1e-12)
