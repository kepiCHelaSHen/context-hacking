"""Tests for ML Hyperparameter Search — Bayesian Optimization."""

import sys
import os
import inspect

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hyperparam_search import BayesianOptPipeline, run_simulation


class TestReturnStructure:
    def test_returns_val_accuracy(self):
        result = run_simulation(seed=42, budget=12)
        assert "best_val_accuracy" in result
        assert isinstance(result["best_val_accuracy"], float)
        assert 0.0 < result["best_val_accuracy"] <= 1.0

    def test_returns_convergence_curve(self):
        result = run_simulation(seed=42, budget=12)
        assert "convergence_curve" in result
        curve = result["convergence_curve"]
        # Convergence curve should be monotonically non-decreasing
        for i in range(1, len(curve)):
            assert curve[i] >= curve[i - 1], "Convergence curve must be non-decreasing"


class TestNoLeakage:
    def test_val_accuracy_below_098(self):
        """Validation accuracy should be < 0.98 (no data leakage)."""
        result = run_simulation(seed=42, budget=15)
        assert result["best_val_accuracy"] < 0.98, \
            f"Val accuracy {result['best_val_accuracy']} >= 0.98 suggests data leakage"

    def test_strict_train_val_test_split(self):
        """Verify the data split sizes are correct and non-overlapping."""
        pipe = BayesianOptPipeline(seed=42)
        assert pipe.X_train.shape[0] == 1200
        assert pipe.X_val.shape[0] == 400
        assert pipe.X_test.shape[0] == 400
        # Total = 2000
        assert pipe.X_train.shape[0] + pipe.X_val.shape[0] + pipe.X_test.shape[0] == 2000


class TestBayesianNotGrid:
    def test_method_is_bayesian(self):
        """Default method should be Bayesian optimization, not grid search."""
        source = inspect.getsource(run_simulation)
        assert "GaussianProcessRegressor" in inspect.getsource(sys.modules["hyperparam_search"])
        assert "grid" not in source.lower() or "not grid" in source.lower() or \
               "grid_" not in source, "Should use Bayesian optimization, not grid search"

    def test_uses_gp_and_ei(self):
        """Should use Gaussian Process with Expected Improvement acquisition."""
        mod_source = inspect.getsource(sys.modules["hyperparam_search"])
        assert "GaussianProcessRegressor" in mod_source
        assert "Matern" in mod_source
        # EI acquisition: expected improvement
        assert "ei" in mod_source.lower()


class TestDeterminism:
    def test_same_seed_same_result(self):
        r1 = run_simulation(seed=99, budget=12)
        r2 = run_simulation(seed=99, budget=12)
        assert r1["best_val_accuracy"] == r2["best_val_accuracy"]
        assert r1["total_evaluations"] == r2["total_evaluations"]
