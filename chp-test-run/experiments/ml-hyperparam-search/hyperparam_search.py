"""
ML Hyperparameter Search — Bayesian Optimization with GP + EI.
Frozen spec: frozen/hyperparam_rules.md

Strict train/val/test split (60/20/20). NO data leakage.
Objective: VALIDATION accuracy. NOT train. NOT test.
Method: Bayesian optimization. NOT grid search.
Budget: 50 evaluations (10 random + 40 GP-guided).
"""

from __future__ import annotations

import logging

import numpy as np
from sklearn.datasets import make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern

_log = logging.getLogger(__name__)

N_SAMPLES = 2000
N_FEATURES = 20
N_INFORMATIVE = 10
N_REDUNDANT = 5
N_CLASSES = 3
TRAIN_SIZE = 1200
VAL_SIZE = 400
TEST_SIZE = 400
BO_BUDGET = 50
BO_INIT_RANDOM = 10


class BayesianOptPipeline:
    """Bayesian optimization for MLP hyperparameters."""

    def __init__(self, seed: int = 42) -> None:
        self.rng = np.random.default_rng(seed)
        X, y = make_classification(
            n_samples=N_SAMPLES, n_features=N_FEATURES,
            n_informative=N_INFORMATIVE, n_redundant=N_REDUNDANT,
            n_classes=N_CLASSES, random_state=seed,
        )
        # Strict split — NO shuffling after split
        self.X_train = X[:TRAIN_SIZE]
        self.y_train = y[:TRAIN_SIZE]
        self.X_val = X[TRAIN_SIZE:TRAIN_SIZE + VAL_SIZE]
        self.y_val = y[TRAIN_SIZE:TRAIN_SIZE + VAL_SIZE]
        self.X_test = X[TRAIN_SIZE + VAL_SIZE:]
        self.y_test = y[TRAIN_SIZE + VAL_SIZE:]

    def evaluate(self, params: dict) -> float:
        """Train MLP with params, return VALIDATION accuracy (NOT train)."""
        clf = MLPClassifier(
            hidden_layer_sizes=(params["layer_1"], params["layer_2"]),
            learning_rate_init=params["lr"],
            alpha=params["alpha"],
            batch_size=params["batch_size"],
            activation=params["activation"],
            max_iter=500, early_stopping=True, validation_fraction=0.15,
            random_state=42,
        )
        clf.fit(self.X_train, self.y_train)

        # VALIDATION accuracy — NOT train, NOT test
        val_acc = float(clf.score(self.X_val, self.y_val))
        train_acc = float(clf.score(self.X_train, self.y_train))

        return val_acc, train_acc

    def sample_random_params(self) -> dict:
        return {
            "layer_1": int(self.rng.integers(32, 257)),
            "layer_2": int(self.rng.integers(16, 129)),
            "lr": float(10 ** self.rng.uniform(-4, -1)),
            "alpha": float(10 ** self.rng.uniform(-5, -1)),
            "batch_size": int(self.rng.integers(16, 129)),
            "activation": self.rng.choice(["relu", "tanh"]),
        }

    def params_to_vector(self, p: dict) -> np.ndarray:
        return np.array([
            p["layer_1"] / 256, p["layer_2"] / 128,
            np.log10(p["lr"]) / 4 + 1, np.log10(p["alpha"]) / 5 + 1,
            p["batch_size"] / 128, 1.0 if p["activation"] == "relu" else 0.0,
        ])


def run_simulation(
    seed: int = 42, method: str = "bayesian", budget: int = BO_BUDGET,
) -> dict:
    pipe = BayesianOptPipeline(seed=seed)

    evaluated_points: list[dict] = []
    val_accs: list[float] = []
    train_accs: list[float] = []

    best_val = 0.0
    best_params = None

    if method == "bayesian":
        # Phase 1: random init
        X_observed = []
        y_observed = []
        for i in range(min(BO_INIT_RANDOM, budget)):
            params = pipe.sample_random_params()
            val_acc, train_acc = pipe.evaluate(params)
            evaluated_points.append(params)
            val_accs.append(val_acc)
            train_accs.append(train_acc)
            X_observed.append(pipe.params_to_vector(params))
            y_observed.append(val_acc)
            if val_acc > best_val:
                best_val = val_acc
                best_params = params

        # Phase 2: GP-guided
        for i in range(budget - BO_INIT_RANDOM):
            if len(X_observed) >= 2:
                gp = GaussianProcessRegressor(
                    kernel=Matern(nu=2.5), random_state=42, normalize_y=True,
                )
                gp.fit(np.array(X_observed), np.array(y_observed))

                # EI acquisition: sample candidates, pick best EI
                best_ei = -1
                best_candidate = None
                for _ in range(100):
                    candidate = pipe.sample_random_params()
                    x_cand = pipe.params_to_vector(candidate).reshape(1, -1)
                    mu, sigma = gp.predict(x_cand, return_std=True)
                    if sigma[0] > 0:
                        z = (mu[0] - best_val) / sigma[0]
                        from scipy.stats import norm
                        ei = (mu[0] - best_val) * norm.cdf(z) + sigma[0] * norm.pdf(z)
                    else:
                        ei = 0.0
                    if ei > best_ei:
                        best_ei = ei
                        best_candidate = candidate

                params = best_candidate or pipe.sample_random_params()
            else:
                params = pipe.sample_random_params()

            val_acc, train_acc = pipe.evaluate(params)
            evaluated_points.append(params)
            val_accs.append(val_acc)
            train_accs.append(train_acc)
            X_observed.append(pipe.params_to_vector(params))
            y_observed.append(val_acc)
            if val_acc > best_val:
                best_val = val_acc
                best_params = params

    else:  # random baseline
        for _ in range(budget):
            params = pipe.sample_random_params()
            val_acc, train_acc = pipe.evaluate(params)
            evaluated_points.append(params)
            val_accs.append(val_acc)
            train_accs.append(train_acc)
            if val_acc > best_val:
                best_val = val_acc
                best_params = params

    # Final test evaluation (ONCE — per frozen spec)
    if best_params:
        test_acc, _ = pipe.evaluate(best_params)
        # Actually evaluate on test set
        clf = MLPClassifier(
            hidden_layer_sizes=(best_params["layer_1"], best_params["layer_2"]),
            learning_rate_init=best_params["lr"],
            alpha=best_params["alpha"],
            batch_size=best_params["batch_size"],
            activation=best_params["activation"],
            max_iter=500, early_stopping=True, random_state=42,
        )
        clf.fit(pipe.X_train, pipe.y_train)
        test_acc = float(clf.score(pipe.X_test, pipe.y_test))
        best_train = float(clf.score(pipe.X_train, pipe.y_train))
    else:
        test_acc = 0.0
        best_train = 0.0

    return {
        "best_val_accuracy": best_val,
        "best_test_accuracy": test_acc,
        "overfitting_gap": best_train - best_val,
        "total_evaluations": len(evaluated_points),
        "evaluated_points": evaluated_points,
        "convergence_curve": [max(val_accs[:i+1]) for i in range(len(val_accs))],
    }
