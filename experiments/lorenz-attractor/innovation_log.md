# Lorenz Attractor — Innovation Log

---

## Expected Build Sequence

Turn 1: Foundation — ODE, RK45 integration, trajectory (Milestone 1)
  → Watch for: Euler loop with dt variable (Dead End 1), beta=2.667 (Dead End 2)
  → Watch for: IC (0,1,0) from paper prior (Dead End 3)
Turn 2: Metrics — Lyapunov exponent, bounds, SDIC, fixed-point check (Milestone 2)
Turn 3: Comparison — RK45 vs RK4 vs Euler at t=50 (Milestone 3)
  → EXPECTED FALSE POSITIVE: "attractor verified" from t<20 Euler trajectory
Turn 4: Convergence battery — 30 perturbations, sigma-gates on Lyapunov (Milestone 4)
