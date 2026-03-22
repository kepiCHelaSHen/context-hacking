"""
Agent-Based Lotka-Volterra — CHP Milestone Test Battery

4 milestones x 30 seeds. Sigma-gated convergence verification.
Key test: predator extinction rate > 0 (catches ODE contamination).

Usage:
    pytest tests/test_milestone_battery.py -v
"""

import numpy as np
import pytest

try:
    from lotka_volterra import LotkaVolterraGrid, run_simulation
    LV_AVAILABLE = True
except ImportError:
    LV_AVAILABLE = False

# ── Frozen coefficients ──────────────────────────────────────────────────────
GRID_W = 50
GRID_H = 50
INITIAL_PREY = 200
INITIAL_PREDATORS = 50
PREY_ENERGY_GAIN = 0.05
PREY_REPRODUCE_THRESHOLD = 1.5
PREDATOR_ENERGY_COST = 0.10
PREDATOR_ENERGY_GAIN = 0.80
PREDATOR_REPRODUCE_THRESHOLD = 1.5
MAX_TICKS = 500

SIGMA_THRESHOLD = 0.15
SEEDS_QUICK = [42, 137, 271]
SEEDS_FULL = list(range(1, 31))


def _skip():
    if not LV_AVAILABLE:
        pytest.skip("lotka_volterra.py not yet built — run the CHP loop first")


def _run(seed: int, n_prey: int = INITIAL_PREY, n_pred: int = INITIAL_PREDATORS,
         ticks: int = MAX_TICKS) -> dict:
    _skip()
    return run_simulation(
        seed=seed, grid_w=GRID_W, grid_h=GRID_H,
        initial_prey=n_prey, initial_predators=n_pred,
        prey_energy_gain=PREY_ENERGY_GAIN,
        prey_reproduce_threshold=PREY_REPRODUCE_THRESHOLD,
        predator_energy_cost=PREDATOR_ENERGY_COST,
        predator_energy_gain=PREDATOR_ENERGY_GAIN,
        predator_reproduce_threshold=PREDATOR_REPRODUCE_THRESHOLD,
        max_ticks=ticks,
    )


# =============================================================================
# MILESTONE 1 — Foundation
# =============================================================================

class TestMilestone1Foundation:

    def test_grid_construction(self):
        _skip()
        grid = LotkaVolterraGrid(seed=42, grid_w=GRID_W, grid_h=GRID_H)
        assert grid.grid_w == GRID_W
        assert grid.grid_h == GRID_H

    def test_initial_populations(self):
        _skip()
        r = _run(42, ticks=0)
        assert r["prey_count"] == INITIAL_PREY
        assert r["predator_count"] == INITIAL_PREDATORS

    def test_step_no_crash(self):
        _skip()
        r = _run(42, ticks=10)
        assert r["prey_count"] >= 0
        assert r["predator_count"] >= 0

    def test_deterministic(self):
        _skip()
        r1 = _run(42, ticks=100)
        r2 = _run(42, ticks=100)
        assert r1["prey_count"] == r2["prey_count"]
        assert r1["predator_count"] == r2["predator_count"]

    def test_different_seeds_differ(self):
        _skip()
        r1 = _run(42, ticks=100)
        r2 = _run(137, ticks=100)
        assert (r1["prey_count"] != r2["prey_count"] or
                r1["predator_count"] != r2["predator_count"])

    def test_predators_die_without_prey(self):
        """With zero prey, predators should starve."""
        _skip()
        r = _run(42, n_prey=0, n_pred=50, ticks=50)
        assert r["predator_count"] == 0, "Predators should starve without prey"

    def test_prey_grow_without_predators(self):
        """With zero predators, prey should grow."""
        _skip()
        r = _run(42, n_prey=50, n_pred=0, ticks=100)
        assert r["prey_count"] > 50, "Prey should reproduce without predation"


# =============================================================================
# MILESTONE 2 — Metrics
# =============================================================================

class TestMilestone2Metrics:

    def test_population_trajectory_is_noisy(self):
        """Agent-based model should produce NOISY trajectories, not smooth curves.

        This catches ODE contamination: if the trajectory is a smooth sinusoid,
        the Builder implemented difference equations, not individual agents.
        """
        _skip()
        r = _run(42, ticks=200)
        trajectory = r.get("prey_trajectory", [])
        if len(trajectory) < 50:
            pytest.skip("Trajectory too short")

        # Compute roughness: mean absolute tick-to-tick change
        diffs = np.abs(np.diff(trajectory))
        roughness = np.mean(diffs) / max(np.mean(trajectory), 1)

        assert roughness > 0.01, (
            f"Trajectory roughness={roughness:.4f} too smooth — "
            f"possible ODE contamination. Agent-based models produce jagged "
            f"trajectories from demographic stochasticity."
        )

    def test_oscillations_present(self):
        """Prey and predator populations should oscillate."""
        _skip()
        r = _run(42, ticks=200)
        prey_traj = r.get("prey_trajectory", [])
        if len(prey_traj) < 100:
            pytest.skip("Trajectory too short")

        # Check for at least 2 local maxima (= at least 1 full oscillation)
        arr = np.array(prey_traj)
        peaks = []
        for i in range(1, len(arr) - 1):
            if arr[i] > arr[i-1] and arr[i] > arr[i+1]:
                peaks.append(i)
        assert len(peaks) >= 2, (
            f"Only {len(peaks)} peaks found — expected oscillating dynamics"
        )

    @pytest.mark.parametrize("seed", SEEDS_QUICK)
    def test_quick_populations_positive(self, seed):
        """Quick 3-seed check: at least one species survives to tick 200."""
        _skip()
        r = _run(seed, ticks=200)
        assert r["prey_count"] > 0 or r["predator_count"] > 0


# =============================================================================
# MILESTONE 3 — Extinction Experiment
# =============================================================================

class TestMilestone3Extinction:

    def test_extinction_rate_nonzero_default(self):
        """At default N (200/50), predator extinction > 0% over 30 seeds.

        This is THE key test. The ODE predicts zero extinction. The agent-based
        model predicts 10-25% predator extinction. If extinction rate is exactly
        zero, the Builder implemented ODE dynamics.
        """
        _skip()
        n_pred_extinct = 0
        for seed in SEEDS_FULL:
            r = _run(seed, ticks=MAX_TICKS)
            if r["predator_count"] == 0:
                n_pred_extinct += 1

        extinction_rate = n_pred_extinct / len(SEEDS_FULL)
        assert extinction_rate > 0.0, (
            f"FALSE POSITIVE DETECTED: predator extinction rate = 0% across "
            f"{len(SEEDS_FULL)} seeds. The ODE predicts zero extinction. "
            f"The agent-based model should show 10-25% extinction at N=200/50. "
            f"Check: is each agent an individual object with energy? "
            f"Or did the Builder generate population-level difference equations?"
        )

    def test_small_populations_higher_extinction(self):
        """Smaller populations should have higher extinction rates."""
        _skip()
        ext_small = 0
        ext_default = 0
        for seed in SEEDS_FULL[:10]:
            r_small = _run(seed, n_prey=50, n_pred=15, ticks=MAX_TICKS)
            r_default = _run(seed, n_prey=INITIAL_PREY, n_pred=INITIAL_PREDATORS,
                             ticks=MAX_TICKS)
            if r_small["predator_count"] == 0:
                ext_small += 1
            if r_default["predator_count"] == 0:
                ext_default += 1

        assert ext_small >= ext_default, (
            f"Small populations ({ext_small}/10 extinct) should have >= extinction "
            f"rate than default ({ext_default}/10). Demographic stochasticity "
            f"is stronger at small N."
        )

    def test_large_populations_lower_extinction(self):
        """Large populations should rarely go extinct."""
        _skip()
        n_ext = 0
        for seed in SEEDS_FULL[:10]:
            r = _run(seed, n_prey=800, n_pred=200, ticks=MAX_TICKS)
            if r["predator_count"] == 0:
                n_ext += 1

        assert n_ext <= 2, (
            f"Large populations (800/200) should rarely go extinct, "
            f"got {n_ext}/10 — check energy parameters"
        )


# =============================================================================
# MILESTONE 4 — Convergence Battery
# =============================================================================

class TestMilestone4ConvergenceBattery:

    @pytest.mark.slow
    def test_prey_count_30_seeds_sigma(self):
        """Prey count at tick 200 across 30 seeds: std/mean < sigma threshold."""
        _skip()
        counts = []
        for seed in SEEDS_FULL:
            r = _run(seed, ticks=200)
            if r["prey_count"] > 0:
                counts.append(r["prey_count"])

        if len(counts) < 20:
            pytest.skip("Too many extinctions for sigma test")

        cv = np.std(counts) / max(np.mean(counts), 1)
        # CV (coefficient of variation) rather than raw std for count data
        assert cv < 0.50, (
            f"Prey count CV={cv:.3f} exceeds threshold — "
            f"unstable dynamics or implementation error"
        )

    @pytest.mark.slow
    def test_oscillation_period_30_seeds(self):
        """Oscillation period across 30 surviving seeds: std < 0.15 * mean."""
        _skip()
        periods = []
        for seed in SEEDS_FULL:
            r = _run(seed, ticks=300)
            period = r.get("oscillation_period", 0)
            if period > 0:
                periods.append(period)

        if len(periods) < 15:
            pytest.skip("Too few runs with detected oscillations")

        mean_p = np.mean(periods)
        std_p = np.std(periods)
        relative_std = std_p / max(mean_p, 1)

        assert relative_std < SIGMA_THRESHOLD, (
            f"Oscillation period relative std={relative_std:.4f} exceeds "
            f"{SIGMA_THRESHOLD} (mean={mean_p:.1f}, std={std_p:.1f})"
        )


# =============================================================================
# COEFFICIENT DRIFT CHECKS
# =============================================================================

class TestCoefficientDrift:

    def test_no_ode_variables(self):
        """Check that the code doesn't use ODE variable names (alpha, beta, etc).

        If the Builder named variables alpha, beta, gamma, delta — it generated
        from the ODE prior, not the agent-based spec.
        """
        _skip()
        import inspect
        source = inspect.getsource(LotkaVolterraGrid)
        ode_vars = ["alpha", "beta", "gamma", "delta", "dX/dt", "dY/dt"]
        for var in ode_vars:
            assert var not in source, (
                f"ODE variable '{var}' found in source code — "
                f"possible ODE contamination. The frozen spec is agent-based."
            )

    def test_prey_energy_gain_exact(self):
        _skip()
        grid = LotkaVolterraGrid(seed=42, grid_w=GRID_W, grid_h=GRID_H)
        assert abs(grid.prey_energy_gain - PREY_ENERGY_GAIN) < 1e-6

    def test_predator_energy_cost_exact(self):
        _skip()
        grid = LotkaVolterraGrid(seed=42, grid_w=GRID_W, grid_h=GRID_H)
        assert abs(grid.predator_energy_cost - PREDATOR_ENERGY_COST) < 1e-6

    def test_grid_dimensions(self):
        _skip()
        grid = LotkaVolterraGrid(seed=42, grid_w=GRID_W, grid_h=GRID_H)
        assert grid.grid_w == 50
        assert grid.grid_h == 50
