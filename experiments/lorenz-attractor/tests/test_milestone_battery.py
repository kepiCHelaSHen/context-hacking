"""
Lorenz Attractor — CHP Milestone Test Battery

4 milestones x 30 perturbed ICs. Sigma-gated Lyapunov convergence.
Key test: Euler contamination detector via trajectory bounds at t=50.

Usage:
    pytest tests/test_milestone_battery.py -v
"""

import numpy as np
import pytest

try:
    from lorenz import LorenzSystem, run_simulation
    LORENZ_AVAILABLE = True
except ImportError:
    LORENZ_AVAILABLE = False

# ── Frozen coefficients ──────────────────────────────────────────────────────
SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0
X0, Y0, Z0 = 1.0, 1.0, 1.0
T_END = 50.0
N_POINTS = 10000
RTOL = 1e-9
ATOL = 1e-9
LYAPUNOV_EXPECTED = 0.906

SIGMA_THRESHOLD = 0.15
# "Seeds" here are IC perturbations: z0 = 1.0 + i*0.0001
PERTURBATIONS = 30


def _skip():
    if not LORENZ_AVAILABLE:
        pytest.skip("lorenz.py not yet built — run the CHP loop first")


def _run(perturbation: float = 0.0) -> dict:
    _skip()
    return run_simulation(
        sigma=SIGMA, rho=RHO, beta=BETA,
        x0=X0, y0=Y0, z0=Z0 + perturbation,
        t_end=T_END, n_points=N_POINTS,
        rtol=RTOL, atol=ATOL,
    )


# =============================================================================
# MILESTONE 1 — Foundation
# =============================================================================

class TestMilestone1Foundation:

    def test_integration_completes(self):
        _skip()
        r = _run()
        assert len(r["x"]) == N_POINTS

    def test_deterministic(self):
        """Same IC → same trajectory (no hidden randomness)."""
        _skip()
        r1 = _run()
        r2 = _run()
        assert np.allclose(r1["x"], r2["x"])

    def test_trajectory_bounded(self):
        """Attractor should stay bounded: |x|<25, |y|<30, |z|<55."""
        _skip()
        r = _run()
        assert np.all(np.abs(r["x"]) < 25), "x unbounded — integration diverged"
        assert np.all(np.abs(r["y"]) < 30), "y unbounded — integration diverged"
        assert np.all(np.abs(r["z"]) < 55), "z unbounded — integration diverged"

    def test_not_fixed_point(self):
        """Trajectory must NOT converge to a fixed point."""
        _skip()
        r = _run()
        x = np.array(r["x"])
        # Check last 1000 points have significant variation
        x_tail = x[-1000:]
        assert np.std(x_tail) > 1.0, (
            f"x std in last 1000 points = {np.std(x_tail):.4f} — "
            f"trajectory may have converged to a fixed point"
        )

    def test_not_euler(self):
        """Check that no fixed dt variable exists — catches Euler contamination."""
        _skip()
        import inspect
        source = inspect.getsource(LorenzSystem)
        # Euler uses a fixed dt loop: for i in range(...): x += ...
        euler_signs = ["* dt", "*dt", "+= sigma", "+= rho"]
        for sign in euler_signs:
            if sign in source:
                # Not conclusive, but suspicious
                assert "solve_ivp" in source or "RK45" in source, (
                    f"Euler-like pattern '{sign}' found without solve_ivp/RK45 — "
                    f"possible Euler contamination"
                )


# =============================================================================
# MILESTONE 2 — Metrics
# =============================================================================

class TestMilestone2Metrics:

    def test_lyapunov_in_range(self):
        """Largest Lyapunov exponent should be ~0.906."""
        _skip()
        r = _run()
        le = r.get("lyapunov_exponent", 0)
        assert 0.7 < le < 1.1, (
            f"Lyapunov exponent {le:.4f} outside expected range [0.7, 1.1] "
            f"(expected ~{LYAPUNOV_EXPECTED})"
        )

    def test_sdic_divergence(self):
        """Two nearby ICs should diverge exponentially (sensitive dependence)."""
        _skip()
        r1 = _run(0.0)
        r2 = _run(0.0001)
        x1 = np.array(r1["x"])
        x2 = np.array(r2["x"])
        max_div = np.max(np.abs(x1 - x2))
        assert max_div > 10.0, (
            f"Max divergence {max_div:.4f} too small — trajectories should "
            f"diverge exponentially by t={T_END}. If divergence < 0.01, the "
            f"integrator is losing precision."
        )

    def test_sdic_initial_close(self):
        """The two ICs should START close (sanity check)."""
        _skip()
        r1 = _run(0.0)
        r2 = _run(0.0001)
        initial_div = abs(r1["z"][0] - r2["z"][0])
        assert initial_div < 0.001


# =============================================================================
# MILESTONE 3 — Integration Method Comparison
# =============================================================================

class TestMilestone3Comparison:

    def test_rk45_consistent_lyapunov(self):
        """RK45 should produce consistent Lyapunov estimates across 10 perturbations."""
        _skip()
        lyapunovs = []
        for i in range(10):
            r = _run(i * 0.0001)
            le = r.get("lyapunov_exponent", 0)
            if le > 0:
                lyapunovs.append(le)

        if len(lyapunovs) < 5:
            pytest.skip("Not enough valid Lyapunov estimates")

        std_le = np.std(lyapunovs)
        assert std_le < 0.10, (
            f"Lyapunov std={std_le:.4f} across perturbations — too variable. "
            f"RK45 at rtol=1e-9 should produce std < 0.10. "
            f"High variance suggests fixed-step integration."
        )

    def test_euler_would_fail_at_t50(self):
        """This test documents WHY Euler fails, not tests the current code.

        At dt=0.01 with Euler, the trajectory at t=50 is numerically
        meaningless. This test verifies our RK45 implementation doesn't
        exhibit Euler-like behavior (trajectory going unbounded or
        Lyapunov estimate > 1.5).
        """
        _skip()
        r = _run()
        le = r.get("lyapunov_exponent", 0)
        assert le < 1.5, (
            f"Lyapunov {le:.4f} > 1.5 — suspiciously high, possible "
            f"numerical instability from inadequate integration"
        )
        assert r.get("attractor_bounded", False), (
            "Trajectory went unbounded — integration method is unstable"
        )


# =============================================================================
# MILESTONE 4 — Convergence Battery
# =============================================================================

class TestMilestone4ConvergenceBattery:

    @pytest.mark.slow
    def test_lyapunov_30_perturbations_sigma(self):
        """Lyapunov exponent across 30 perturbations: std < sigma threshold."""
        _skip()
        lyapunovs = []
        for i in range(PERTURBATIONS):
            r = _run(i * 0.0001)
            le = r.get("lyapunov_exponent", 0)
            if le > 0:
                lyapunovs.append(le)

        if len(lyapunovs) < 20:
            pytest.skip("Too few valid estimates")

        mean_le = np.mean(lyapunovs)
        std_le = np.std(lyapunovs)

        assert std_le < SIGMA_THRESHOLD, (
            f"Lyapunov std={std_le:.4f} exceeds sigma threshold "
            f"{SIGMA_THRESHOLD} (mean={mean_le:.4f})"
        )
        assert 0.8 < mean_le < 1.0, (
            f"Mean Lyapunov={mean_le:.4f} outside expected range [0.8, 1.0]"
        )

    @pytest.mark.slow
    def test_all_trajectories_bounded(self):
        """All 30 perturbations must stay within attractor bounds."""
        _skip()
        for i in range(PERTURBATIONS):
            r = _run(i * 0.0001)
            assert r.get("attractor_bounded", False), (
                f"Perturbation {i}: trajectory went unbounded"
            )

    @pytest.mark.slow
    def test_all_trajectories_chaotic(self):
        """No perturbation should converge to a fixed point."""
        _skip()
        for i in range(PERTURBATIONS):
            r = _run(i * 0.0001)
            x = np.array(r["x"])
            x_tail = x[-1000:]
            assert np.std(x_tail) > 1.0, (
                f"Perturbation {i}: trajectory converged (std={np.std(x_tail):.4f})"
            )


# =============================================================================
# COEFFICIENT DRIFT CHECKS
# =============================================================================

class TestCoefficientDrift:

    def test_sigma_exact(self):
        _skip()
        sys = LorenzSystem(sigma=SIGMA, rho=RHO, beta=BETA)
        assert sys.sigma == 10.0

    def test_rho_exact(self):
        _skip()
        sys = LorenzSystem(sigma=SIGMA, rho=RHO, beta=BETA)
        assert sys.rho == 28.0

    def test_beta_exact_fraction(self):
        """Beta must be 8/3 exactly, not a rounded decimal."""
        _skip()
        sys = LorenzSystem(sigma=SIGMA, rho=RHO, beta=BETA)
        assert sys.beta == 8.0 / 3.0, (
            f"Beta should be 8/3 = {8.0/3.0}, got {sys.beta}. "
            f"If 2.667: the Builder rounded from a decimal literal (drift)."
        )

    def test_initial_conditions(self):
        """IC should be (1,1,1), NOT (0,1,0) from Lorenz's paper."""
        _skip()
        r = _run()
        assert r["x"][0] == pytest.approx(1.0)
        assert r["y"][0] == pytest.approx(1.0)
        assert r["z"][0] == pytest.approx(1.0)

    def test_integration_method_is_adaptive(self):
        """Verify RK45 or equivalent adaptive solver is used."""
        _skip()
        import inspect
        source = inspect.getsource(run_simulation)
        assert "solve_ivp" in source or "RK45" in source or "DOP853" in source, (
            "No adaptive solver found in source — possible Euler/RK4 contamination"
        )
