# ML Hyperparameter Search — Frozen Specification
# Grounded in: Snoek et al. (2012) "Practical Bayesian Optimization of ML Algorithms"
#              Bergstra & Bengio (2012) "Random Search for Hyper-Parameter Optimization"
# THIS FILE IS FROZEN. No agent may modify it.

================================================================================
OVERVIEW
================================================================================

A Bayesian optimization pipeline for neural network hyperparameters using
Gaussian Process (GP) surrogate with Expected Improvement (EI) acquisition.
The pipeline enforces STRICT train/validation/test splits with NO data leakage.

The key scientific point: LLMs default to GRID SEARCH when asked for
"hyperparameter optimization" because grid search dominates tutorials and
textbooks. Grid search scales exponentially with dimension count and is
provably less efficient than random search (Bergstra & Bengio 2012) or
Bayesian optimization (Snoek et al. 2012). Additionally, LLMs routinely
leak test data into training or evaluate on training data when generating
ML pipelines.

================================================================================
TASK
================================================================================

DATASET: Synthetic classification (sklearn.datasets.make_classification)
  n_samples: 2000
  n_features: 20
  n_informative: 10
  n_redundant: 5
  n_classes: 3
  random_state: frozen per seed

SPLIT: strict 60/20/20 train/val/test
  - Train: indices [0:1200]
  - Validation: indices [1200:1600]
  - Test: indices [1600:2000]
  - NO shuffling after split (prevents leakage via index reuse)
  - Test set is NEVER seen during search. Only used for FINAL evaluation.

MODEL: sklearn.neural_network.MLPClassifier
  Fixed architecture: 2 hidden layers
  Fixed: max_iter=500, early_stopping=True, validation_fraction=0.15
    (this is MLPClassifier's INTERNAL validation, separate from our val split)

================================================================================
HYPERPARAMETERS TO OPTIMIZE (frozen search space)
================================================================================

  hidden_layer_sizes:
    layer_1: integer [32, 256]
    layer_2: integer [16, 128]

  learning_rate_init: float [1e-4, 1e-1] (log-uniform)

  alpha: float [1e-5, 1e-1] (log-uniform, L2 regularization)

  batch_size: integer [16, 128]

  activation: categorical ["relu", "tanh"]

  TOTAL: 6 hyperparameters, 4 continuous + 1 integer + 1 categorical

================================================================================
SEARCH METHOD (FROZEN)
================================================================================

METHOD: Bayesian Optimization with Gaussian Process surrogate

ACQUISITION: Expected Improvement (EI)
  EI(x) = E[max(f(x) - f_best, 0)]
  where f is the GP posterior predictive distribution.

BUDGET: 50 evaluations (function calls to train + validate)
  - First 10: random initialization (Latin Hypercube or uniform random)
  - Remaining 40: GP-guided via EI acquisition

OBJECTIVE: VALIDATION accuracy (NOT train accuracy, NOT test accuracy)
  The search optimizes ONLY against the validation set.
  Test accuracy is computed ONCE at the end for the best config.

  NOTE: This is the critical data hygiene rule. LLMs routinely generate
  code that optimizes against test accuracy or reports train accuracy as
  the result. The frozen spec requires strict separation:
    - Search sees: train + validation ONLY
    - Final report: test accuracy of best-on-validation config

GP KERNEL: Matern 5/2 with automatic relevance determination (ARD)
  Hyperparameters of the GP itself are optimized via marginal likelihood.

================================================================================
METRICS
================================================================================

  best_val_accuracy: highest validation accuracy found during search
  best_test_accuracy: test accuracy of the config that won on validation
  overfitting_gap: best_train_accuracy - best_val_accuracy
  search_efficiency: (best_val after 50 BO evals) vs (best_val after 50 random evals)
  convergence_curve: best-so-far validation accuracy vs evaluation number

================================================================================
DATA LEAKAGE WARNING
================================================================================

The most common LLM-generated ML error is DATA LEAKAGE. Signs:

  1. Reporting TRAIN accuracy as the result (accuracy > 0.98 is suspicious)
  2. Using test data during hyperparameter search (test should be touched ONCE)
  3. Fitting a scaler/encoder on full dataset before splitting
  4. Shuffling after split with a data-dependent random state
  5. Using cross-validation that includes test fold in training

If best accuracy > 0.98 at 50 evaluations on this synthetic dataset:
almost certainly data leakage. Expected range: 0.88-0.95 on validation,
0.85-0.93 on test.

================================================================================
EXACT COEFFICIENTS (for drift detection)
================================================================================

  N_SAMPLES: 2000
  N_FEATURES: 20
  N_INFORMATIVE: 10
  N_REDUNDANT: 5
  N_CLASSES: 3
  TRAIN_SIZE: 1200
  VAL_SIZE: 400
  TEST_SIZE: 400
  BO_BUDGET: 50
  BO_INIT_RANDOM: 10
  BO_GUIDED: 40
  GP_KERNEL: "matern52_ard"
  ACQUISITION: "expected_improvement"
  OBJECTIVE: "validation_accuracy"
