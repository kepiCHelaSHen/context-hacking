# ML Hyperparameter Search — CHP Experiment Specification

## Research Question

Does Bayesian optimization outperform random search at 50 evaluations for a
6-dimensional hyperparameter space on a 3-class classification task?

## What to Build

1. `hyperparam_search.py` — Bayesian optimization pipeline
   - Strict train/val/test split (60/20/20, no leakage)
   - GP surrogate with Matern 5/2 kernel
   - Expected Improvement acquisition
   - 10 random init + 40 GP-guided evaluations
   - Metrics: val accuracy, test accuracy, overfitting gap, convergence curve
   - All randomness via seeded numpy.random.Generator

2. `run_experiment.py` — Experiment runner
   - Condition A: Bayesian optimization (frozen spec), 30 seeds
   - Condition B: Pure random search (50 evals), 30 seeds — baseline
   - Condition C: Grid search (50 evals from grid), 30 seeds — LLM prior baseline
   - Output: per-seed summary CSV + convergence curves

3. `tests/test_milestone_battery.py` — Sigma-gated test battery

## Milestones

1. FOUNDATION — Data generation, split, MLP training, validation evaluation
2. BAYESIAN OPT — GP surrogate, EI acquisition, search loop
3. COMPARISON — BO vs random vs grid at 50 evaluations
4. CONVERGENCE BATTERY — 30 seeds, sigma-gates, leakage detection

## Expected False Positive

At Milestone 1, the Builder may report accuracy of 0.992 — but this is TRAIN
accuracy, not validation. The frozen spec requires VALIDATION accuracy as the
objective. Expected validation accuracy: 0.88-0.95. Anything above 0.98 is
almost certainly data leakage (train/test contamination).

At Milestone 2, the Builder may implement GRID SEARCH and call it "optimization."
Grid search is the LLM prior for "hyperparameter tuning." The frozen spec
requires Bayesian optimization with GP surrogate and EI acquisition.
