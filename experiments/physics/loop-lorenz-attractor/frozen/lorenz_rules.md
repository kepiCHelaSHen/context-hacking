# Lorenz Attractor — Frozen Specification
# Source: Lorenz (1963) "Deterministic Nonperiodic Flow", J. Atmospheric Sciences 20:130-141
# THIS FILE IS FROZEN. No agent may modify it.

================================================================================
OVERVIEW
================================================================================

The Lorenz system is a system of three coupled ordinary differential equations
that exhibits chaotic behavior for certain parameter values. It is the canonical
example of deterministic chaos: the system is fully deterministic (no randomness)
but exhibits sensitive dependence on initial conditions (SDIC).

The key scientific point: LLMs know the Lorenz equations and will generate them
correctly. But they DEFAULT to Euler integration with fixed step size, which is
NUMERICALLY UNSTABLE for chaotic systems. Small integration errors compound
exponentially, producing trajectories that diverge from the true solution.
The frozen spec requires ADAPTIVE step-size integration (RK45).

================================================================================
EQUATIONS
================================================================================

dx/dt = sigma * (y - x)
dy/dt = x * (rho - z) - y
dz/dt = x * y - beta * z

PARAMETERS (frozen):
  sigma = 10.0
  rho = 28.0
  beta = 8.0 / 3.0  (exactly, as a fraction — NOT 2.667 or 2.67)

  NOTE: These are the EXACT Lorenz (1963) values. LLMs sometimes generate
  sigma=10, rho=28, beta=2.667 (rounded). The frozen value is 8/3 EXACTLY.
  Any rounded value is specification drift.

INITIAL CONDITIONS (frozen):
  x0 = 1.0
  y0 = 1.0
  z0 = 1.0

  NOTE: These are NOT the Lorenz (1963) original IC (which were x=0, y=1, z=0).
  The frozen spec uses (1,1,1) for consistency across seeds. LLMs that generate
  from the paper's prior will use (0,1,0) — this is drift.

================================================================================
INTEGRATION METHOD (FROZEN)
================================================================================

METHOD: Adaptive Runge-Kutta (RK45) — Dormand-Prince variant.

IMPLEMENTATION: scipy.integrate.solve_ivp with method='RK45'
  rtol = 1e-9
  atol = 1e-9

  NOTE: These are TIGHT tolerances for high-accuracy integration.
  The default scipy tolerances (rtol=1e-3, atol=1e-6) are INSUFFICIENT
  for accurate Lorenz integration beyond t=30 due to exponential error growth.

  LLMs commonly generate:
  1. Fixed-step Euler: dx = sigma*(y-x)*dt — UNSTABLE for dt > 0.005
  2. Fixed-step RK4: stable but accumulates error proportional to dt^4 * t
  3. solve_ivp with default tolerances: diverges from true solution by t=40

  The frozen spec requires RK45 with rtol=atol=1e-9.

TIME SPAN:
  t_start = 0.0
  t_end = 50.0
  t_eval: 10,000 equally-spaced points in [0, 50]

  NOTE: t=50 is chosen specifically because:
  - t < 20: any reasonable integrator produces a correct-looking trajectory
  - t = 20-30: Euler diverges; fixed-step RK4 begins to accumulate error
  - t = 30-50: only adaptive RK45 with tight tolerances produces the
    correct attractor topology

================================================================================
METRICS
================================================================================

  lyapunov_exponent: estimated largest Lyapunov exponent
    Expected: ~0.906 (Lorenz 1963 system at these parameters)
    Method: Benettin et al. (1980) algorithm — integrate a tangent vector
    alongside the trajectory and compute the time-averaged exponential growth rate.

  attractor_bounded: boolean — does |x| < 25, |y| < 30, |z| < 55 for all t?
    If unbounded: integration has diverged (numerical instability).

  not_fixed_point: boolean — trajectory does NOT converge to a fixed point.
    The Lorenz system has three unstable fixed points at these parameters.
    A correct integration should show perpetual oscillation, not convergence.

  trajectory_divergence: max |x_test(t) - x_ref(t)| at t=50 between two
    trajectories started at IC = (1.0, 1.0, 1.0) and IC = (1.0, 1.0, 1.0001).
    Expected: divergence > 10 by t=50 (SDIC — sensitive dependence).
    If divergence < 0.01: the integrator is losing precision (rounding the
    chaos into numerical convergence).

  correlation_dimension: estimated from box-counting or Grassberger-Procaccia.
    Expected: ~2.05 (Lorenz attractor is a fractal with non-integer dimension).

================================================================================
EULER CONTAMINATION WARNING
================================================================================

The Euler method is:
  x(t+dt) = x(t) + sigma * (y(t) - x(t)) * dt

LLMs WILL generate this when asked to "integrate the Lorenz system" because
Euler is the simplest integrator and appears in every numerical methods tutorial.

Signs of Euler contamination:
  - Variable named dt with a fixed value (dt=0.01 or dt=0.001)
  - No call to scipy.integrate.solve_ivp or equivalent adaptive solver
  - Trajectory that looks correct for t < 20 but diverges or goes unbounded for t > 30
  - Lyapunov exponent estimate that differs from 0.906 by more than 0.1

Fixed-step RK4 is ALSO contamination for this spec (even though it's more accurate
than Euler). The frozen spec requires ADAPTIVE step size.

================================================================================
EXACT COEFFICIENTS (for drift detection)
================================================================================

  SIGMA: 10.0
  RHO: 28.0
  BETA: 8.0 / 3.0  (2.6666666666666665 in float64)
  X0: 1.0
  Y0: 1.0
  Z0: 1.0
  T_END: 50.0
  N_POINTS: 10000
  RTOL: 1e-9
  ATOL: 1e-9
  METHOD: "RK45"
  LYAPUNOV_EXPECTED: 0.906
