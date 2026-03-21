"""
Spatial Prisoner's Dilemma — CHP Milestone Test Battery

4 milestones x 30 seeds. sigma-gated convergence verification.

Usage:
    pytest tests/test_milestone_battery.py -v
"""

import numpy as np
import pytest

try:
    from spatial_pd import SpatialPDGrid, run_simulation
    SPATIAL_PD_AVAILABLE = True
except ImportError:
    SPATIAL_PD_AVAILABLE = False

# ── Frozen coefficients ──────────────────────────────────────────────────────
GRID_SIZE = 100
B_DEFAULT = 1.8
NEIGHBORHOOD_SIZE = 9  # Moore + self
GENERATIONS = 200
PAYOFF_CC = 1
PAYOFF_CD = 0
PAYOFF_DD = 0

SIGMA_THRESHOLD = 0.15
SEEDS_QUICK = [42, 137, 271]
SEEDS_FULL = list(range(1, 31))


def _skip_if_not_built():
    if not SPATIAL_PD_AVAILABLE:
        pytest.skip("spatial_pd.py not yet built — run the CHP loop first")


def _run(seed: int, b: float = B_DEFAULT, initial: str = "single_defector_center",
         generations: int = GENERATIONS) -> dict:
    _skip_if_not_built()
    return run_simulation(seed=seed, grid_size=GRID_SIZE, b=b,
                          initial_condition=initial, generations=generations)


# =============================================================================
# MILESTONE 1 — Foundation
# =============================================================================

class TestMilestone1Foundation:

    def test_grid_construction(self):
        _skip_if_not_built()
        grid = SpatialPDGrid(grid_size=GRID_SIZE, b=B_DEFAULT)
        assert grid.grid_size == GRID_SIZE
        assert grid.grid.shape == (GRID_SIZE, GRID_SIZE)

    def test_single_defector_initial(self):
        """Initial condition: all C except center cell = D."""
        _skip_if_not_built()
        grid = SpatialPDGrid(grid_size=GRID_SIZE, b=B_DEFAULT)
        grid.set_initial("single_defector_center")
        center = GRID_SIZE // 2
        assert grid.grid[center, center] == 0  # D
        assert np.sum(grid.grid == 1) == GRID_SIZE * GRID_SIZE - 1  # all others C

    def test_step_no_crash(self):
        _skip_if_not_built()
        grid = SpatialPDGrid(grid_size=GRID_SIZE, b=B_DEFAULT)
        grid.set_initial("single_defector_center")
        grid.step()

    def test_deterministic(self):
        """Same initial condition → same result (deterministic imitation)."""
        _skip_if_not_built()
        r1 = _run(42)
        r2 = _run(42)
        assert r1["cooperation_rate"] == r2["cooperation_rate"]

    def test_synchronous_update(self):
        """Verify update is synchronous: new grid computed from old grid entirely."""
        _skip_if_not_built()
        grid = SpatialPDGrid(grid_size=GRID_SIZE, b=B_DEFAULT)
        grid.set_initial("single_defector_center")
        old_grid = grid.grid.copy()
        grid.step()
        # After one step from single defector, the pattern should be symmetric
        # (because the initial condition is symmetric and update is synchronous).
        # Asynchronous update would break symmetry.
        center = GRID_SIZE // 2
        # Check 4-fold symmetry around center
        new = grid.grid
        assert new[center-1, center] == new[center+1, center], "Synchronous update should preserve symmetry"
        assert new[center, center-1] == new[center, center+1], "Synchronous update should preserve symmetry"


# =============================================================================
# MILESTONE 2 — Metrics
# =============================================================================

class TestMilestone2Metrics:

    def test_cooperation_rate_bounded(self):
        _skip_if_not_built()
        r = _run(42)
        assert 0.0 <= r["cooperation_rate"] <= 1.0

    def test_cooperation_survives_at_b18(self):
        """At b=1.8 with spatial structure, cooperators should survive."""
        _skip_if_not_built()
        r = _run(42, b=1.8)
        assert r["cooperation_rate"] > 0.20, (
            f"Cooperators should survive at b=1.8 in spatial PD, "
            f"got rate={r['cooperation_rate']:.3f}. "
            f"If zero, check: is the neighborhood including self (size 9)? "
            f"Is the update synchronous?"
        )

    def test_defectors_survive_at_b18(self):
        """At b=1.8, defectors should also persist (not trivial all-C)."""
        _skip_if_not_built()
        r = _run(42, b=1.8)
        assert r["cooperation_rate"] < 0.80

    def test_cooperation_extinct_at_high_b(self):
        """At b=2.5, defectors should dominate (cooperation near zero)."""
        _skip_if_not_built()
        r = _run(42, b=2.5)
        assert r["cooperation_rate"] < 0.15

    @pytest.mark.parametrize("seed", SEEDS_QUICK)
    def test_quick_bound_check(self, seed):
        _skip_if_not_built()
        r = _run(seed, b=1.8)
        assert 0.20 < r["cooperation_rate"] < 0.80
        assert r.get("spatial_clustering", 0) > 0


# =============================================================================
# MILESTONE 3 — b-Sweep
# =============================================================================

class TestMilestone3BSweep:

    def test_cooperation_decreases_with_b(self):
        """Higher b → lower cooperation (monotonic relationship)."""
        _skip_if_not_built()
        b_values = [1.0, 1.4, 1.8, 2.0, 2.5]
        rates = []
        for b in b_values:
            r = _run(42, b=b, initial="single_defector_center")
            rates.append(r["cooperation_rate"])

        # Should be roughly monotonically decreasing
        # Allow one violation (stochastic at boundaries)
        decreasing_count = sum(1 for i in range(len(rates)-1) if rates[i] >= rates[i+1])
        assert decreasing_count >= 3, (
            f"Cooperation should decrease with b. Rates: {list(zip(b_values, rates))}"
        )

    def test_false_positive_wellmixed_extinction(self):
        """At b=1.8 with spatial structure, cooperation should NOT go extinct.

        If cooperation goes extinct at b=1.8, the Builder implemented
        well-mixed dynamics (no spatial structure) or has a neighborhood bug.
        This is the textbook PD prior: defection dominates. In the spatial
        version, cooperator clusters survive through mutual reinforcement.
        """
        _skip_if_not_built()
        r = _run(42, b=1.8)
        if r["cooperation_rate"] < 0.05:
            pytest.fail(
                f"FALSE POSITIVE DETECTED: cooperation_rate={r['cooperation_rate']:.3f} "
                f"at b=1.8. This is the well-mixed PD result (defection dominates). "
                f"In the spatial version, cooperators should survive (rate ~0.3-0.6). "
                f"Check: is the neighborhood spatial (Moore+self)? Is update synchronous?"
            )


# =============================================================================
# MILESTONE 4 — Convergence Battery (30 seeds)
# =============================================================================

class TestMilestone4ConvergenceBattery:

    @pytest.mark.slow
    def test_cooperation_rate_30_seeds_b18(self):
        """b=1.8 across 30 seeds: cooperation rate std < 0.15."""
        _skip_if_not_built()
        rates = []
        for seed in SEEDS_FULL:
            r = _run(seed, b=1.8, initial="random_half", generations=100)
            rates.append(r["cooperation_rate"])

        mean_r = np.mean(rates)
        std_r = np.std(rates)

        assert std_r < SIGMA_THRESHOLD, (
            f"Cooperation rate std={std_r:.4f} exceeds sigma threshold "
            f"{SIGMA_THRESHOLD} (mean={mean_r:.4f})"
        )
        assert 0.20 < mean_r < 0.80, (
            f"Mean cooperation rate={mean_r:.4f} out of expected range"
        )

    @pytest.mark.slow
    def test_pattern_stability_30_seeds(self):
        """Patterns should stabilize: Hamming distance < 0.1 by gen 100."""
        _skip_if_not_built()
        stabilities = []
        for seed in SEEDS_FULL:
            r = _run(seed, b=1.8, initial="random_half", generations=100)
            stabilities.append(r.get("pattern_stability", 0))

        mean_s = np.mean(stabilities)
        assert mean_s < 0.10, (
            f"Mean pattern instability={mean_s:.4f} — patterns not converging"
        )


# =============================================================================
# COEFFICIENT DRIFT CHECKS
# =============================================================================

class TestCoefficientDrift:

    def test_b_is_18(self):
        _skip_if_not_built()
        grid = SpatialPDGrid(grid_size=GRID_SIZE, b=B_DEFAULT)
        assert abs(grid.b - 1.8) < 1e-6, f"b should be 1.8, got {grid.b}"

    def test_neighborhood_size_is_9(self):
        """Must be Moore + self = 9, not Moore = 8."""
        _skip_if_not_built()
        grid = SpatialPDGrid(grid_size=GRID_SIZE, b=B_DEFAULT)
        center = GRID_SIZE // 2
        neighbors = grid.get_neighborhood(center, center)
        assert len(neighbors) == 9, (
            f"Neighborhood should be 9 (Moore+self), got {len(neighbors)}. "
            f"Missing self-inclusion is a common drift from the Nowak & May spec."
        )

    def test_grid_size_is_100(self):
        _skip_if_not_built()
        grid = SpatialPDGrid(grid_size=GRID_SIZE, b=B_DEFAULT)
        assert grid.grid_size == 100

    def test_payoff_cc_is_1(self):
        _skip_if_not_built()
        grid = SpatialPDGrid(grid_size=GRID_SIZE, b=B_DEFAULT)
        assert grid.payoff(1, 1) == PAYOFF_CC  # C vs C = 1

    def test_payoff_dc_is_b(self):
        _skip_if_not_built()
        grid = SpatialPDGrid(grid_size=GRID_SIZE, b=B_DEFAULT)
        assert abs(grid.payoff(0, 1) - B_DEFAULT) < 1e-6  # D vs C = b
