"""cat-bio-predator-functional-response — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_predator_functional_response_constants import *
IMPL = Path(__file__).parent.parent / "bio_predator_functional_response.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_type_III_is_sigmoidal_not_hyperbolic(self):
        """Type III must ACCELERATE at low N (sigmoid shape, not hyperbolic).

        If Type III uses aN/(1+ahN) instead of aN²/(1+ahN²), the curve will
        always decelerate — this is the #1 LLM error.
        """
        m = _i()
        # Compute slopes at low prey density
        f1 = m.type_III(A, H, 1)
        f2 = m.type_III(A, H, 2)
        f3 = m.type_III(A, H, 3)
        slope_12 = f2 - f1
        slope_23 = f3 - f2
        assert slope_23 > slope_12, (
            f"Type III must accelerate at low N: slope(2→3)={slope_23:.6f} "
            f"should be > slope(1→2)={slope_12:.6f}. "
            f"If decelerating, Type III was likely given the wrong formula (aN/(1+ahN) instead of aN²/(1+ahN²))"
        )

    def test_type_III_differs_from_type_II_at_low_N(self):
        """Type III and Type II must give DIFFERENT values at low prey density.

        If they give the same values, Type III was probably implemented with the
        wrong formula (same as Type II, without N²).
        """
        m = _i()
        f2_at_3 = m.type_II(A, H, 3)
        f3_at_3 = m.type_III(A, H, 3)
        assert not math.isclose(f2_at_3, f3_at_3, rel_tol=0.01), (
            f"Type III at N=3 ({f3_at_3:.6f}) must differ from Type II at N=3 ({f2_at_3:.6f}). "
            f"Same value means Type III uses aN/(1+ahN) — should be aN²/(1+ahN²)"
        )

    def test_type_III_uses_N_squared(self):
        """Direct check that Type III uses N² — compare against hand-computed value.

        Type III at N=3: a*9/(1+a*h*9) = 0.9/1.45 ≈ 0.6207
        If N were used instead of N²: a*3/(1+a*h*3) = 0.3/1.15 ≈ 0.2609
        """
        m = _i()
        f3 = m.type_III(A, H, 3)
        # Correct (N²): 0.9/1.45 = 0.62069
        assert math.isclose(f3, TYPE_III_AT_N3, rel_tol=1e-6), (
            f"Type III at N=3 = {f3:.6f}, expected {TYPE_III_AT_N3:.6f} (a*N²/(1+ahN²))"
        )
        # Reject wrong formula (N instead of N²): 0.3/1.15 = 0.26087
        wrong_value = A * 3 / (1 + A * H * 3)
        assert not math.isclose(f3, wrong_value, rel_tol=0.01), (
            f"Type III at N=3 matches the WRONG formula aN/(1+ahN) = {wrong_value:.6f}"
        )


class TestCorrectness:
    def test_type_II_at_N10(self):
        m = _i()
        f = m.type_II(A, H, 10)
        assert math.isclose(f, TYPE_II_AT_N10, rel_tol=1e-9), (
            f"Type II at N=10: got {f}, expected {TYPE_II_AT_N10}"
        )

    def test_type_II_at_N100(self):
        m = _i()
        f = m.type_II(A, H, 100)
        assert math.isclose(f, TYPE_II_AT_N100, rel_tol=1e-9), (
            f"Type II at N=100: got {f}, expected {TYPE_II_AT_N100}"
        )

    def test_type_III_at_N10(self):
        m = _i()
        f = m.type_III(A, H, 10)
        assert math.isclose(f, TYPE_III_AT_N10, rel_tol=1e-9), (
            f"Type III at N=10: got {f}, expected {TYPE_III_AT_N10}"
        )

    def test_type_III_at_N3(self):
        m = _i()
        f = m.type_III(A, H, 3)
        assert math.isclose(f, TYPE_III_AT_N3, rel_tol=1e-9), (
            f"Type III at N=3: got {f}, expected {TYPE_III_AT_N3}"
        )

    def test_max_consumption_rate(self):
        m = _i()
        rate = m.max_consumption_rate(H)
        assert math.isclose(rate, MAX_RATE, rel_tol=1e-9), (
            f"Max rate = 1/h: got {rate}, expected {MAX_RATE}"
        )

    def test_type_I_linearity(self):
        m = _i()
        f5 = m.type_I(A, 5)
        f10 = m.type_I(A, 10)
        assert math.isclose(f5, TYPE_I_AT_N5, rel_tol=1e-9), (
            f"Type I at N=5: got {f5}, expected {TYPE_I_AT_N5}"
        )
        assert math.isclose(f10, TYPE_I_AT_N10, rel_tol=1e-9), (
            f"Type I at N=10: got {f10}, expected {TYPE_I_AT_N10}"
        )
        # Linearity check: doubling N should double f
        assert math.isclose(f10, 2 * f5, rel_tol=1e-9), (
            f"Type I should be linear: f(10)={f10} should be 2*f(5)={2*f5}"
        )

    def test_type_I_capping(self):
        """Type I should cap at N_max when provided."""
        m = _i()
        capped = m.type_I(A, 100, N_max=5.0)
        assert math.isclose(capped, 5.0, rel_tol=1e-9), (
            f"Type I capped at N_max=5.0: got {capped}"
        )

    def test_type_II_approaches_max_rate(self):
        """Type II at very high N should approach but not exceed 1/h."""
        m = _i()
        f_huge = m.type_II(A, H, 1_000_000)
        assert f_huge < MAX_RATE, (
            f"Type II should be below max rate at finite N; got {f_huge}, max={MAX_RATE}"
        )
        assert f_huge > MAX_RATE * 0.999, (
            f"Type II at huge N should be nearly max rate; got {f_huge}"
        )

    def test_type_III_approaches_max_rate(self):
        """Type III at very high N should approach but not exceed 1/h."""
        m = _i()
        f_huge = m.type_III(A, H, 1_000_000)
        assert f_huge < MAX_RATE, (
            f"Type III should be below max rate at finite N; got {f_huge}, max={MAX_RATE}"
        )
        assert f_huge > MAX_RATE * 0.999, (
            f"Type III at huge N should be nearly max rate; got {f_huge}"
        )

    def test_type_II_monotonically_increasing(self):
        """Type II consumption must increase monotonically with prey density."""
        m = _i()
        prev = 0
        for n in [0.1, 1, 3, 10, 50, 100, 1000]:
            f = m.type_II(A, H, n)
            assert f > prev, f"Type II at N={n}: {f} should be > {prev}"
            prev = f

    def test_type_III_monotonically_increasing(self):
        """Type III consumption must increase monotonically with prey density."""
        m = _i()
        prev = 0
        for n in [0.1, 1, 3, 10, 50, 100, 1000]:
            f = m.type_III(A, H, n)
            assert f > prev, f"Type III at N={n}: {f} should be > {prev}"
            prev = f
