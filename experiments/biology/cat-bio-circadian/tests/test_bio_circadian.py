"""cat-bio-circadian — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_circadian_constants import *
IMPL = Path(__file__).parent.parent / "bio_circadian.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_n2_cannot_oscillate_basic_goodwin(self):
        """n=2 must NOT produce sustained oscillations in basic 3-var Goodwin.
        This is the most common LLM error — confusing with repressilator or
        modified Goodwin models where n>=2 suffices.
        """
        m = _i()
        assert not m.can_oscillate(N_NO_OSCILLATION), \
            f"n={N_NO_OSCILLATION} must NOT permit oscillation in basic Goodwin"

    def test_minimum_hill_exceeds_8(self):
        """Basic Goodwin requires n > 8 for sustained oscillations (Griffith 1968)."""
        m = _i()
        min_n = m.min_hill_for_oscillation()
        assert min_n > 8, \
            f"Minimum Hill coefficient must be > 8, got {min_n}"
        assert min_n == MIN_HILL_INTEGER, \
            f"Expected min integer Hill = {MIN_HILL_INTEGER}, got {min_n}"

    def test_small_n_all_damped(self):
        """n = 1,2,3,...,8 must all give damped oscillations (no sustained cycle)."""
        m = _i()
        for n in range(1, 9):
            assert not m.can_oscillate(n), \
                f"n={n} should NOT oscillate in basic Goodwin"

    def test_hill_repression_not_linear(self):
        """The repression term must use Hill function K^n/(K^n+Z^n), not linear decay.
        At Z=0, repression = 1 (max transcription). At Z=K, repression = 0.5.
        """
        m = _i()
        h0 = m.hill_repression(0.0, K, N_OSCILLATION)
        hK = m.hill_repression(K, K, N_OSCILLATION)
        assert math.isclose(h0, 1.0, rel_tol=1e-9), \
            f"h(0) should be 1.0 (max transcription), got {h0}"
        assert math.isclose(hK, 0.5, rel_tol=1e-9), \
            f"h(K) should be 0.5, got {hK}"


class TestCorrectness:
    def test_hill_repression_at_zero(self):
        """h(0, K, n) = 1.0 for any K, n."""
        m = _i()
        for n in [1, 2, 5, 10]:
            h = m.hill_repression(0.0, K, n)
            assert math.isclose(h, HILL_AT_Z0, rel_tol=1e-9), \
                f"h(0, K={K}, n={n}) should be {HILL_AT_Z0}, got {h}"

    def test_hill_repression_at_K(self):
        """h(K, K, n) = 0.5 for any n."""
        m = _i()
        for n in [1, 2, 5, 10]:
            h = m.hill_repression(K, K, n)
            assert math.isclose(h, HILL_AT_ZK, rel_tol=1e-9), \
                f"h(K, K, n={n}) should be {HILL_AT_ZK}, got {h}"

    def test_hill_repression_at_Z2_n10(self):
        """h(2, 1, 10) = 1/1025 ≈ 0.000976."""
        m = _i()
        h = m.hill_repression(2.0, K, N_OSCILLATION)
        assert math.isclose(h, HILL_AT_Z2_N10, rel_tol=1e-9), \
            f"h(2, 1, 10) should be {HILL_AT_Z2_N10:.6e}, got {h:.6e}"

    def test_hill_repression_monotone_decreasing(self):
        """Hill repression must decrease as Z increases."""
        m = _i()
        prev = 1.0
        for z in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
            h = m.hill_repression(z, K, N_OSCILLATION)
            assert h < prev, f"h({z}) = {h} should be < h(prev) = {prev}"
            prev = h

    def test_derivatives_at_111(self):
        """Check derivatives at (X,Y,Z)=(1,1,1) with n=10."""
        m = _i()
        dX, dY, dZ = m.goodwin_derivatives(
            1, 1, 1, K1, K2, K3, K4, K5, K6, K, N_OSCILLATION
        )
        assert math.isclose(dX, DERIV_REF_X, rel_tol=1e-9), \
            f"dX at (1,1,1) should be {DERIV_REF_X}, got {dX}"
        assert math.isclose(dY, DERIV_REF_Y, rel_tol=1e-9), \
            f"dY at (1,1,1) should be {DERIV_REF_Y}, got {dY}"
        assert math.isclose(dZ, DERIV_REF_Z, rel_tol=1e-9), \
            f"dZ at (1,1,1) should be {DERIV_REF_Z}, got {dZ}"

    def test_derivatives_at_origin(self):
        """At (0,0,0): dX = k1*1 - 0 = k1, dY = 0, dZ = 0."""
        m = _i()
        dX, dY, dZ = m.goodwin_derivatives(
            0, 0, 0, K1, K2, K3, K4, K5, K6, K, N_OSCILLATION
        )
        assert math.isclose(dX, K1, rel_tol=1e-9), \
            f"dX at origin should be k1={K1}, got {dX}"
        assert math.isclose(dY, 0.0, abs_tol=1e-15), \
            f"dY at origin should be 0, got {dY}"
        assert math.isclose(dZ, 0.0, abs_tol=1e-15), \
            f"dZ at origin should be 0, got {dZ}"

    def test_can_oscillate_true_for_large_n(self):
        """n=9,10,20,50 must permit oscillation."""
        m = _i()
        for n in [9, 10, 20, 50]:
            assert m.can_oscillate(n), \
                f"n={n} should permit oscillation in basic Goodwin"

    def test_can_oscillate_false_at_boundary(self):
        """n=8 must NOT oscillate (boundary: need n > 8, not n >= 8)."""
        m = _i()
        assert not m.can_oscillate(8), \
            "n=8 should NOT oscillate (threshold is strictly > 8)"
        assert m.can_oscillate(9), \
            "n=9 should oscillate (first integer > 8)"

    def test_min_hill_returns_9(self):
        """Minimum integer Hill coefficient for basic Goodwin is 9."""
        m = _i()
        assert m.min_hill_for_oscillation() == 9
