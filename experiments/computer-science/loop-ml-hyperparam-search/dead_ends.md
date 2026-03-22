# ML Hyperparameter Search — Dead Ends Log

---

## DEAD END 1 — Grid search instead of Bayesian optimization

**What was attempted**: Builder generated an exhaustive grid over the 6 hyperparameters
with np.linspace for each dimension.

**Result**: 6 dimensions with even 5 values each = 5^6 = 15,625 evaluations. With a
budget of 50, grid search can only sample a tiny, regularly-spaced slice of the space.
Bergstra & Bengio (2012) proved random search outperforms grid search because grid
wastes evaluations on unimportant dimensions.

**Why this is a dead end**: The frozen spec requires Bayesian optimization with GP
surrogate and EI acquisition. Grid search is a completely different algorithm that
cannot exploit the surrogate model's uncertainty estimates.

**Do NOT repeat**: Any exhaustive or regularly-spaced search strategy.

---

## DEAD END 2 — Evaluating on training data

**What was attempted**: Builder computed accuracy on the training set (indices 0:1200)
and reported it as the search objective.

**Result**: Train accuracy was 0.992 — far above the expected validation range of
0.88-0.95. The model memorized the training data. When evaluated on the held-out
validation set, accuracy dropped to 0.87.

**Why this is a dead end**: The frozen spec requires VALIDATION accuracy as the
search objective. Train accuracy is not a valid metric for hyperparameter selection
because it rewards overfitting. This is the most common ML error and the most
common LLM-generated data leakage pattern.

**Do NOT repeat**: Using train indices for ANY evaluation during search. Train data
is for fitting the model ONLY.

---

## DEAD END 3 — Using test set during search

**What was attempted**: Builder used the test set (indices 1600:2000) as the
validation objective during Bayesian optimization.

**Result**: The "best" hyperparameters were overfit to the test set. When evaluated
on truly unseen data, performance degraded. This is test-set leakage — the test
set should be touched exactly ONCE, after the search is complete.

**Why this is a dead end**: The frozen spec enforces strict separation: search sees
train + validation ONLY. Test accuracy is computed ONCE at the end for the
best-on-validation configuration. Using test data during search invalidates the
final test accuracy as an unbiased estimate of generalization performance.

**Do NOT repeat**: Any access to indices 1600:2000 during the search loop.
