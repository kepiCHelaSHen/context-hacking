# ML Hyperparameter Search — Chain Prompt

================================================================================
PROJECT IDENTITY
================================================================================

Name:       ML Hyperparameter Search (CHP Showcase)
Purpose:    Demonstrate Prior-as-Detector catching grid search prior and
            data leakage in LLM-generated ML pipelines.

================================================================================
CONFIRMED DESIGN DECISIONS
================================================================================

DD01 — Search method: Bayesian optimization with GP surrogate + EI acquisition.
DD02 — NOT grid search. NOT random search (except as baseline comparison).
DD03 — Split: strict 60/20/20 train/val/test. Indices [0:1200]/[1200:1600]/[1600:2000].
DD04 — Objective: VALIDATION accuracy. NOT train. NOT test.
DD05 — Test set touched ONCE — after search is complete.
DD06 — Budget: 50 evaluations (10 random init + 40 GP-guided).
DD07 — Dataset: make_classification(n=2000, features=20, informative=10, classes=3).
DD08 — Model: MLPClassifier, 2 hidden layers, fixed max_iter=500.

================================================================================
ARCHITECTURE RULES
================================================================================

- Pure library: NO print(), NO UI.
- All randomness via seeded numpy.random.Generator / random_state.
- Same seed = identical output.
- Structured logging.
- NO data leakage: test indices never accessed during search.

================================================================================
FROZEN CODE
================================================================================

frozen/hyperparam_rules.md — DO NOT MODIFY.
