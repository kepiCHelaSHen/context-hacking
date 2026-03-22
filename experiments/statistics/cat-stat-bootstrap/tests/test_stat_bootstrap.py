"""cat-stat-bootstrap — Bootstrap Gate Tests"""
import sys, math, statistics
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_bootstrap_constants import *
IMPL = Path(__file__).parent.parent / "stat_bootstrap.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_resampling_is_with_replacement(self):
        """Bootstrap resamples must be drawn WITH replacement.

        If sampling were without replacement, every resample would be a
        permutation of the original — no element could appear twice.
        We generate many resamples and confirm at least some contain repeats.
        """
        m = _i()
        import random
        rng = random.Random(123)
        data = list(DATA)
        has_repeat = False
        for _ in range(50):
            resample = m.bootstrap_resample(data, rng=rng)
            if len(set(resample)) < len(resample):
                has_repeat = True
                break
        assert has_repeat, (
            "No resample in 50 draws contained a repeat — "
            "sampling appears to be WITHOUT replacement (permutation)"
        )

    def test_p_repeat_for_n5(self):
        """P(any repeat) for n=5 must match the frozen constant 0.9616.

        With 96 % of resamples containing repeats, using without-replacement
        sampling would be obviously wrong (0 % repeats).
        """
        m = _i()
        result = m.p_any_repeat(N)
        assert abs(result - P_ANY_REPEAT) < 1e-4, (
            f"p_any_repeat({N}) = {result}, expected {P_ANY_REPEAT}"
        )

    def test_empirical_repeat_rate_matches_theory(self):
        """Empirical fraction of resamples with repeats should be near 96 %."""
        m = _i()
        import random
        rng = random.Random(999)
        data = list(DATA)
        B = 5000
        repeats = sum(
            1 for _ in range(B)
            if len(set(m.bootstrap_resample(data, rng=rng))) < len(data)
        )
        empirical = repeats / B
        # Should be close to 0.9616 — allow generous margin for randomness
        assert 0.93 < empirical < 0.99, (
            f"Empirical repeat rate {empirical:.4f} far from theoretical {P_ANY_REPEAT}"
        )


class TestCorrectness:
    def test_resample_length_matches_original(self):
        """Every bootstrap resample must have the same length as the original."""
        m = _i()
        import random
        rng = random.Random(42)
        data = list(DATA)
        for _ in range(100):
            resample = m.bootstrap_resample(data, rng=rng)
            assert len(resample) == len(data), (
                f"Resample length {len(resample)} ≠ original length {len(data)}"
            )

    def test_bootstrap_se_positive_and_reasonable(self):
        """Bootstrap SE of the mean should be positive and close to the
        theoretical SE (σ/√n ≈ 2.1213).
        """
        m = _i()
        boot = m.bootstrap_stat(list(DATA), statistics.mean, B=10000, seed=42)
        se = m.bootstrap_se(boot)
        assert se > 0, "Bootstrap SE must be positive"
        # Allow a generous window around the theoretical value
        assert 1.0 < se < 4.0, (
            f"Bootstrap SE = {se:.4f}, expected near {THEORETICAL_SE}"
        )

    def test_bootstrap_ci_contains_original_mean(self):
        """95 % percentile CI from bootstrap should contain the original mean."""
        m = _i()
        boot = m.bootstrap_stat(list(DATA), statistics.mean, B=10000, seed=42)
        lo, hi = m.bootstrap_ci_percentile(boot, alpha=0.05)
        assert lo <= ORIGINAL_MEAN <= hi, (
            f"CI [{lo:.4f}, {hi:.4f}] does not contain original mean {ORIGINAL_MEAN}"
        )

    def test_p_any_repeat_formula(self):
        """p_any_repeat must match 1 − n!/n^n for several values of n."""
        m = _i()
        for n in [2, 3, 5, 10]:
            expected = 1.0 - math.factorial(n) / (n ** n)
            result = m.p_any_repeat(n)
            assert abs(result - expected) < 1e-12, (
                f"p_any_repeat({n}) = {result}, expected {expected}"
            )

    def test_n_distinct_bootstrap_samples(self):
        """Number of distinct bootstrap samples for n=5 must be C(9,5)=126."""
        assert N_DISTINCT_BOOTSTRAP == 126

    def test_bootstrap_stat_returns_B_values(self):
        """bootstrap_stat must return exactly B statistics."""
        m = _i()
        B = 500
        boot = m.bootstrap_stat(list(DATA), statistics.mean, B=B, seed=7)
        assert len(boot) == B
