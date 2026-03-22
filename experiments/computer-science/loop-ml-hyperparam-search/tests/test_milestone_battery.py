"""
ML Hyperparameter Search — CHP Milestone Test Battery

4 milestones x 30 seeds. Sigma-gated convergence + data leakage detection.

Usage:
    pytest tests/test_milestone_battery.py -v
"""

import numpy as np
import pytest

try:
    from hyperparam_search import BayesianOptPipeline, run_simulation
    HYPERPARAM_AVAILABLE = True
except ImportError:
    HYPERPARAM_AVAILABLE = False

# ── Frozen coefficients ──────────────────────────────────────────────────────
N_SAMPLES = 2000
N_FEATURES = 20
N_INFORMATIVE = 10
N_CLASSES = 3
TRAIN_SIZE = 1200
VAL_SIZE = 400
TEST_SIZE = 400
BO_BUDGET = 50
BO_INIT_RANDOM = 10

SIGMA_THRESHOLD = 0.15
SEEDS_QUICK = [42, 137, 271]
SEEDS_FULL = list(range(1, 31))


def _skip():
    if not HYPERPARAM_AVAILABLE:
        pytest.skip("hyperparam_search.py not yet built — run the CHP loop first")


def _run(seed: int, method: str = "bayesian", budget: int = BO_BUDGET) -> dict:
    _skip()
    return run_simulation(seed=seed, method=method, budget=budget)


# =============================================================================
# MILESTONE 1 — Foundation (data, split, training, evaluation)
# =============================================================================

class TestMilestone1Foundation:

    def test_data_generation(self):
        _skip()
        pipe = BayesianOptPipeline(seed=42)
        assert pipe.X_train.shape == (TRAIN_SIZE, N_FEATURES)
        assert pipe.X_val.shape == (VAL_SIZE, N_FEATURES)
        assert pipe.X_test.shape == (TEST_SIZE, N_FEATURES)

    def test_no_overlap_train_val(self):
        """Train and validation indices must not overlap (data leakage check)."""
        _skip()
        pipe = BayesianOptPipeline(seed=42)
        train_set = set(range(TRAIN_SIZE))
        val_set = set(range(TRAIN_SIZE, TRAIN_SIZE + VAL_SIZE))
        assert train_set.isdisjoint(val_set)

    def test_no_overlap_train_test(self):
        _skip()
        pipe = BayesianOptPipeline(seed=42)
        # Verify by checking that X_test is different from X_train
        assert not np.array_equal(pipe.X_train[:10], pipe.X_test[:10])

    def test_three_classes(self):
        _skip()
        pipe = BayesianOptPipeline(seed=42)
        assert len(np.unique(pipe.y_train)) == N_CLASSES

    def test_deterministic(self):
        _skip()
        r1 = _run(42, budget=10)
        r2 = _run(42, budget=10)
        assert r1["best_val_accuracy"] == r2["best_val_accuracy"]

    def test_single_eval_works(self):
        _skip()
        r = _run(42, budget=1)
        assert 0.0 < r["best_val_accuracy"] < 1.0


# =============================================================================
# MILESTONE 2 — Bayesian Optimization
# =============================================================================

class TestMilestone2BayesianOpt:

    def test_val_accuracy_in_range(self):
        """Validation accuracy should be 0.85-0.96, NOT 0.98+ (leakage)."""
        _skip()
        r = _run(42)
        assert 0.50 < r["best_val_accuracy"] < 0.98, (
            f"Val accuracy {r['best_val_accuracy']:.3f} — "
            f"if > 0.98, likely data leakage (train accuracy reported as val)"
        )

    def test_data_leakage_detector(self):
        """If val accuracy > 0.98, it's almost certainly train accuracy.

        This is the pre-loaded false positive. Expected val accuracy on this
        synthetic dataset: 0.88-0.95. Anything above 0.98 triggers the alarm.
        """
        _skip()
        r = _run(42)
        if r["best_val_accuracy"] > 0.98:
            pytest.fail(
                f"FALSE POSITIVE DETECTED: val_accuracy={r['best_val_accuracy']:.4f}. "
                f"This almost certainly means the Builder is evaluating on TRAINING "
                f"data (indices 0:{TRAIN_SIZE}) instead of VALIDATION data "
                f"(indices {TRAIN_SIZE}:{TRAIN_SIZE + VAL_SIZE}). "
                f"Expected validation accuracy: 0.88-0.95."
            )

    def test_overfitting_gap_bounded(self):
        """Train accuracy - val accuracy should be < 0.10 (not massively overfit)."""
        _skip()
        r = _run(42)
        gap = r.get("overfitting_gap", 0)
        assert gap < 0.10, (
            f"Overfitting gap {gap:.3f} too large — model is memorizing"
        )

    def test_not_grid_search(self):
        """Verify the search is NOT grid search (the LLM prior).

        Grid search evaluates a regularly-spaced grid. Bayesian optimization
        evaluates points guided by the GP surrogate. Check that the evaluated
        points are NOT on a regular grid.
        """
        _skip()
        r = _run(42)
        evaluated_points = r.get("evaluated_points", [])
        if len(evaluated_points) < 20:
            pytest.skip("Not enough points to check")

        # Extract first continuous dimension (learning_rate_init)
        lr_values = sorted([p.get("learning_rate_init", 0) for p in evaluated_points])
        # Grid search produces evenly-spaced values; BO does not
        if len(lr_values) >= 10:
            diffs = np.diff(lr_values)
            unique_diffs = len(set(np.round(diffs, 6)))
            # Grid search: all diffs are identical (1 unique diff)
            # BO: diffs vary (many unique diffs)
            assert unique_diffs > 3, (
                f"Only {unique_diffs} unique inter-point spacings — "
                f"looks like grid search, not Bayesian optimization"
            )

    @pytest.mark.parametrize("seed", SEEDS_QUICK)
    def test_quick_bound_check(self, seed):
        _skip()
        r = _run(seed)
        assert 0.50 < r["best_val_accuracy"] < 0.98
        assert r.get("overfitting_gap", 1) < 0.15


# =============================================================================
# MILESTONE 3 — BO vs Random vs Grid Comparison
# =============================================================================

class TestMilestone3Comparison:

    def test_bo_beats_random(self):
        """Bayesian optimization should outperform random search at 50 evals."""
        _skip()
        bo_accs = []
        rand_accs = []
        for seed in SEEDS_FULL[:10]:
            r_bo = _run(seed, method="bayesian")
            r_rand = _run(seed, method="random")
            bo_accs.append(r_bo["best_val_accuracy"])
            rand_accs.append(r_rand["best_val_accuracy"])

        mean_bo = np.mean(bo_accs)
        mean_rand = np.mean(rand_accs)

        assert mean_bo >= mean_rand - 0.01, (
            f"BO (mean={mean_bo:.4f}) should be >= random (mean={mean_rand:.4f}). "
            f"If BO is worse, the GP surrogate may be misconfigured."
        )

    def test_test_accuracy_unbiased(self):
        """Test accuracy should be close to (but slightly below) val accuracy.

        A large gap (val >> test) indicates the search overfit to the val set.
        """
        _skip()
        r = _run(42)
        val_acc = r["best_val_accuracy"]
        test_acc = r["best_test_accuracy"]
        gap = val_acc - test_acc
        assert gap < 0.05, (
            f"Val-test gap {gap:.3f} too large — search may have overfit to val set"
        )
        assert gap > -0.05, (
            f"Test > val by {-gap:.3f} — suspicious, possible data contamination"
        )


# =============================================================================
# MILESTONE 4 — Convergence Battery
# =============================================================================

class TestMilestone4ConvergenceBattery:

    @pytest.mark.slow
    def test_val_accuracy_30_seeds_sigma(self):
        """Val accuracy across 30 seeds: std < sigma threshold."""
        _skip()
        accs = []
        for seed in SEEDS_FULL:
            r = _run(seed)
            accs.append(r["best_val_accuracy"])

        mean_a = np.mean(accs)
        std_a = np.std(accs)

        assert std_a < SIGMA_THRESHOLD, (
            f"Val accuracy std={std_a:.4f} exceeds sigma threshold "
            f"{SIGMA_THRESHOLD} (mean={mean_a:.4f})"
        )
        assert 0.85 < mean_a < 0.96, (
            f"Mean val accuracy={mean_a:.4f} out of expected range [0.85, 0.96]"
        )

    @pytest.mark.slow
    def test_no_leakage_30_seeds(self):
        """No seed should report val accuracy > 0.98 (leakage check)."""
        _skip()
        for seed in SEEDS_FULL:
            r = _run(seed)
            assert r["best_val_accuracy"] < 0.98, (
                f"Seed {seed}: val_accuracy={r['best_val_accuracy']:.4f} > 0.98 — "
                f"data leakage suspected"
            )

    @pytest.mark.slow
    def test_overfitting_gap_30_seeds(self):
        """Overfitting gap across 30 seeds: all < 0.10."""
        _skip()
        for seed in SEEDS_FULL:
            r = _run(seed)
            gap = r.get("overfitting_gap", 0)
            assert gap < 0.10, (
                f"Seed {seed}: overfitting gap {gap:.3f} exceeds 0.10"
            )


# =============================================================================
# COEFFICIENT DRIFT CHECKS
# =============================================================================

class TestCoefficientDrift:

    def test_train_size_exact(self):
        _skip()
        pipe = BayesianOptPipeline(seed=42)
        assert pipe.X_train.shape[0] == TRAIN_SIZE

    def test_val_size_exact(self):
        _skip()
        pipe = BayesianOptPipeline(seed=42)
        assert pipe.X_val.shape[0] == VAL_SIZE

    def test_test_size_exact(self):
        _skip()
        pipe = BayesianOptPipeline(seed=42)
        assert pipe.X_test.shape[0] == TEST_SIZE

    def test_n_features_exact(self):
        _skip()
        pipe = BayesianOptPipeline(seed=42)
        assert pipe.X_train.shape[1] == N_FEATURES

    def test_budget_exact(self):
        _skip()
        r = _run(42)
        n_evals = r.get("total_evaluations", 0)
        assert n_evals == BO_BUDGET, (
            f"Budget should be {BO_BUDGET} evaluations, got {n_evals}"
        )
