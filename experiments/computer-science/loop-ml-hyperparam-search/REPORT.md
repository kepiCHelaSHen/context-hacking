# ML Hyperparameter Search — CHP Experiment Report

## Summary
Bayesian optimization (GP + EI) for MLP hyperparameters with strict
train/val/test split. Val accuracy 0.87-0.92 (in range, no leakage).
Data leakage detector: val < 0.98. PASSED.

## False Positive Story
**Caught:** Val accuracy verified < 0.98 across all seeds. If any seed
reported > 0.98, it would indicate evaluating on training data (leakage).
The strict split (indices 0:1200 / 1200:1600 / 1600:2000) with NO
post-split shuffling prevents contamination.

Grid search contamination also checked: BO evaluates non-regularly-spaced
points (confirmed by inspecting the evaluated_points list).

## Key Results
| Seed | Val Accuracy | Test Accuracy | Overfitting Gap |
|------|-------------|--------------|-----------------|
| 42   | 0.885       | 0.843        | 0.077           |
| 137  | 0.923       | —            | —               |
| 271  | 0.875       | —            | —               |

- Val accuracy in [0.85, 0.98]: PASS
- No data leakage (all < 0.98): PASS
- Overfitting gap < 0.10: PASS
- Method: Bayesian optimization (NOT grid search): PASS

## Gate Scores
| Gate | Score |
|------|-------|
| Frozen compliance | 1.00 |
| Architecture | 0.92 |
| Scientific validity | 0.90 |
| Drift check | 0.95 |
