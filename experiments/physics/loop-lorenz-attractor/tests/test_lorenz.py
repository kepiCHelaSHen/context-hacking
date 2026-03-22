"""Tests for Lorenz Attractor simulation."""

import sys
import os
import inspect

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
from lorenz import LorenzSystem, run_simulation


class TestReturnStructure:
    def test_returns_x_y_z_arrays(self):
        result = run_simulation(t_end=5.0, n_points=500)
        assert "x" in result
        assert "y" in result
        assert "z" in result
        assert isinstance(result["x"], list)
        assert isinstance(result["y"], list)
        assert isinstance(result["z"], list)
        assert len(result["x"]) == 500
        assert len(result["y"]) == 500
        assert len(result["z"]) == 500


class TestIntegrationMethod:
    def test_uses_solve_ivp_not_euler(self):
        """The source must use solve_ivp (adaptive RK45), not Euler or fixed-step."""
        import lorenz as mod
        source = inspect.getsource(mod)
        assert "solve_ivp" in source, "Must use scipy.integrate.solve_ivp"
        # Should not contain a hand-rolled Euler loop
        assert "euler" not in source.lower() or "not euler" in source.lower(), \
            "Should not use Euler integration"


class TestAttractorBounded:
    def test_attractor_bounded_flag(self):
        result = run_simulation(t_end=50.0, n_points=10000)
        assert result["attractor_bounded"] is True

    def test_x_y_z_within_bounds(self):
        result = run_simulation(t_end=50.0, n_points=10000)
        x = np.array(result["x"])
        y = np.array(result["y"])
        z = np.array(result["z"])
        assert np.all(np.abs(x) < 25), "x should be bounded within [-25, 25]"
        assert np.all(np.abs(y) < 30), "y should be bounded within [-30, 30]"
        assert np.all(np.abs(z) < 55), "z should be bounded within [-55, 55]"


class TestChaotic:
    def test_not_fixed_point(self):
        result = run_simulation(t_end=50.0, n_points=10000)
        assert result["not_fixed_point"] is True

    def test_tail_has_variance(self):
        """The tail of the trajectory should show chaotic oscillation, not convergence."""
        result = run_simulation(t_end=50.0, n_points=10000)
        x_tail = np.array(result["x"][-1000:])
        std = np.std(x_tail)
        assert std > 1.0, f"Tail std(x) = {std}, expected > 1.0 for chaotic behavior"

    def test_positive_lyapunov(self):
        result = run_simulation(t_end=50.0, n_points=10000)
        assert result["lyapunov_exponent"] > 0, \
            f"Lyapunov exponent = {result['lyapunov_exponent']}, expected > 0 for chaos"
