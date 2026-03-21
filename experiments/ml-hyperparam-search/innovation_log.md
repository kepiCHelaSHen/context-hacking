# ML Hyperparameter Search — Innovation Log

---

## Expected Build Sequence

Turn 1: Foundation — data generation, strict split, MLP training (Milestone 1)
  → Watch for: test data used during training (Dead End 3), shuffling after split
Turn 2: Bayesian optimization — GP surrogate, EI acquisition (Milestone 2)
  → Watch for: grid search (Dead End 1), train accuracy reported as val (Dead End 2)
  → EXPECTED FALSE POSITIVE: accuracy > 0.98 = data leakage
Turn 3: Comparison — BO vs random vs grid at 50 evals (Milestone 3)
Turn 4: Convergence battery — 30 seeds, leakage detection (Milestone 4)
