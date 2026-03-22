"""cat-bio-population-age — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_population_age_constants import *
IMPL = Path(__file__).parent.parent / "bio_population_age.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_lambda_is_not_r(self):
        """The #1 LLM error: confusing λ (finite growth rate) with r=ln(λ)."""
        m = _i()
        lam = m.growth_rate_numerical(LESLIE_MATRIX, N0, steps=200)
        r = math.log(lam)
        # λ and r must be meaningfully different
        assert not math.isclose(lam, r, rel_tol=0.01), \
            f"λ={lam:.6f} and r={r:.6f} should differ — they are distinct quantities"
        # λ must be close to known dominant eigenvalue
        assert math.isclose(lam, LAMBDA_DOMINANT, rel_tol=1e-4), \
            f"λ={lam:.6f}, expected {LAMBDA_DOMINANT:.6f}"

    def test_leslie_fecundity_in_first_row(self):
        """Leslie matrix must have fecundity in first row, not survival."""
        # Fecundity values in first row
        assert LESLIE_MATRIX[0] == FECUNDITY, \
            "First row of Leslie matrix must be fecundity values"
        # Sub-diagonal has survival probabilities (each ≤ 1)
        assert LESLIE_MATRIX[1][0] == SURVIVAL[0] and LESLIE_MATRIX[1][0] <= 1.0, \
            "Sub-diagonal element L[1][0] must be survival probability S1"
        assert LESLIE_MATRIX[2][1] == SURVIVAL[1] and LESLIE_MATRIX[2][1] <= 1.0, \
            "Sub-diagonal element L[2][1] must be survival probability S2"

    def test_eigenvalue_is_not_eigenvector(self):
        """Growth rate is the dominant eigenvalue (scalar), not the eigenvector (vector)."""
        m = _i()
        lam = m.growth_rate_numerical(LESLIE_MATRIX, N0, steps=200)
        # Growth rate must be a scalar (float), not a vector/list
        assert isinstance(lam, float), \
            f"Growth rate should be a scalar float, got {type(lam).__name__}"
        # It must be close to LAMBDA_DOMINANT, not to the stable age distribution
        assert math.isclose(lam, LAMBDA_DOMINANT, rel_tol=1e-4), \
            f"Growth rate λ={lam}, expected {LAMBDA_DOMINANT}"


class TestCorrectness:
    def test_one_step_projection(self):
        """L × n0 must match hand-computed result."""
        m = _i()
        n1 = m.leslie_multiply(LESLIE_MATRIX, N0)
        for i in range(3):
            assert math.isclose(n1[i], N1_EXPECTED[i], rel_tol=1e-9), \
                f"n1[{i}]={n1[i]}, expected {N1_EXPECTED[i]}"

    def test_project_length(self):
        """project() returns steps+1 vectors (including initial)."""
        m = _i()
        history = m.project(LESLIE_MATRIX, N0, 10)
        assert len(history) == 11, f"Expected 11 vectors, got {len(history)}"
        # First entry is initial condition
        for i in range(3):
            assert math.isclose(history[0][i], N0[i], rel_tol=1e-9)

    def test_growth_rate_converges(self):
        """Numerical growth rate must converge to dominant eigenvalue."""
        m = _i()
        lam = m.growth_rate_numerical(LESLIE_MATRIX, N0, steps=200)
        assert math.isclose(lam, LAMBDA_DOMINANT, rel_tol=1e-4), \
            f"Growth rate {lam:.8f} did not converge to λ={LAMBDA_DOMINANT:.8f}"

    def test_is_growing_true(self):
        """λ > 1 means growing population."""
        m = _i()
        assert m.is_growing(LAMBDA_DOMINANT) is True, \
            f"λ={LAMBDA_DOMINANT} > 1, population should be growing"

    def test_is_growing_false(self):
        """λ < 1 means declining population."""
        m = _i()
        assert m.is_growing(0.95) is False, "λ=0.95 < 1, population should be declining"

    def test_is_growing_boundary(self):
        """λ = 1 exactly means stable, not growing."""
        m = _i()
        assert m.is_growing(1.0) is False, "λ=1.0 is stable, not growing"
