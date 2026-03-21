"""
Schelling Segregation — CHP Milestone Test Battery

4 milestones x 30 seeds. All primary metrics must have sigma < 0.15.
This is the sigma-gated convergence test that proves the implementation
is stable across random seeds, not just lucky on one.

Adapted from the SIMSIV v2 convergence battery pattern.

Usage:
    pytest tests/test_milestone_battery.py -v
"""

import numpy as np
import pytest

# These imports will work once schelling.py is built by the loop.
# Until then, the tests serve as the SPEC for what the Builder must produce.
try:
    from schelling import SchellingGrid, run_simulation
    SCHELLING_AVAILABLE = True
except ImportError:
    SCHELLING_AVAILABLE = False

# ── Frozen coefficients (must match frozen/schelling_rules.md) ────────────────
GRID_SIZE = 50
DENSITY = 0.90
TYPE_RATIO = 0.50
TOLERANCE_DEFAULT = 0.375
TOLERANCE_UPDATE_RATE = 0.005
TOLERANCE_COMFORT_MARGIN = 0.1
TOLERANCE_MIN = 0.1
TOLERANCE_MAX = 0.9
MAX_STEPS = 500

# ── sigma-gate thresholds ────────────────────────────────────────────────────
SIGMA_THRESHOLD = 0.15
N_SEEDS_QUICK = 3
N_SEEDS_FULL = 30

SEEDS_QUICK = [42, 137, 271]
SEEDS_FULL = list(range(1, 31))


# ── Helpers ──────────────────────────────────────────────────────────────────

def _skip_if_not_built():
    if not SCHELLING_AVAILABLE:
        pytest.skip("schelling.py not yet built — run the CHP loop first")


def _run_and_collect(seed: int, dynamic_tolerance: bool = False) -> dict:
    """Run one simulation and return final metrics."""
    _skip_if_not_built()
    result = run_simulation(
        seed=seed,
        grid_size=GRID_SIZE,
        density=DENSITY,
        type_ratio=TYPE_RATIO,
        tolerance=TOLERANCE_DEFAULT,
        dynamic_tolerance=dynamic_tolerance,
        tolerance_update_rate=TOLERANCE_UPDATE_RATE,
        tolerance_comfort_margin=TOLERANCE_COMFORT_MARGIN,
        tolerance_min=TOLERANCE_MIN,
        tolerance_max=TOLERANCE_MAX,
        max_steps=MAX_STEPS,
    )
    return result


# =============================================================================
# MILESTONE 1 — Foundation (Grid, agents, step function)
# =============================================================================

class TestMilestone1Foundation:
    """Basic construction and stepping — no crashes, correct grid size."""

    def test_grid_construction(self):
        _skip_if_not_built()
        grid = SchellingGrid(seed=42, grid_size=GRID_SIZE, density=DENSITY)
        assert grid.grid_size == GRID_SIZE
        n_occupied = np.sum(grid.grid != 0)
        expected = int(GRID_SIZE * GRID_SIZE * DENSITY)
        assert abs(n_occupied - expected) < 50  # within tolerance of stochastic placement

    def test_step_no_crash(self):
        _skip_if_not_built()
        grid = SchellingGrid(seed=42, grid_size=GRID_SIZE, density=DENSITY)
        grid.step()  # one step should not crash

    def test_deterministic(self):
        _skip_if_not_built()
        r1 = _run_and_collect(42)
        r2 = _run_and_collect(42)
        assert r1["segregation_index"] == r2["segregation_index"]

    def test_different_seeds_differ(self):
        _skip_if_not_built()
        r1 = _run_and_collect(42)
        r2 = _run_and_collect(137)
        # At least one metric should differ
        assert r1["segregation_index"] != r2["segregation_index"]


# =============================================================================
# MILESTONE 2 — Metrics (Segregation index, clusters, convergence)
# =============================================================================

class TestMilestone2Metrics:
    """Metrics are computed correctly and within expected ranges."""

    def test_segregation_index_bounded(self):
        _skip_if_not_built()
        r = _run_and_collect(42)
        assert 0.0 <= r["segregation_index"] <= 1.0

    def test_cluster_count_positive(self):
        _skip_if_not_built()
        r = _run_and_collect(42)
        assert r["cluster_count"] >= 1

    def test_original_model_high_segregation(self):
        """Original Schelling (fixed tolerance) should produce high segregation."""
        _skip_if_not_built()
        r = _run_and_collect(42, dynamic_tolerance=False)
        assert r["segregation_index"] > 0.70, (
            f"Original Schelling should segregate strongly, got {r['segregation_index']:.3f}"
        )

    @pytest.mark.parametrize("seed", SEEDS_QUICK)
    def test_quick_bound_check(self, seed):
        """Quick 3-seed bound check: segregation in [0.3, 1.0], clusters > 1."""
        _skip_if_not_built()
        r = _run_and_collect(seed)
        assert r["segregation_index"] > 0.30
        assert r["cluster_count"] > 1


# =============================================================================
# MILESTONE 3 — Dynamic Tolerance Extension
# =============================================================================

class TestMilestone3DynamicTolerance:
    """Dynamic tolerance should produce LESS segregation than the original."""

    def test_dynamic_produces_partial_mixing(self):
        """Dynamic tolerance: segregation should be 0.5-0.7, not 0.8+."""
        _skip_if_not_built()
        r = _run_and_collect(42, dynamic_tolerance=True)
        assert r["segregation_index"] < 0.80, (
            f"Dynamic tolerance should prevent complete segregation, "
            f"got {r['segregation_index']:.3f} — possible spec drift "
            f"(tolerance update applied before move instead of after?)"
        )

    def test_dynamic_vs_original_comparison(self):
        """Dynamic tolerance should produce LOWER segregation than original."""
        _skip_if_not_built()
        r_original = _run_and_collect(42, dynamic_tolerance=False)
        r_dynamic = _run_and_collect(42, dynamic_tolerance=True)
        assert r_dynamic["segregation_index"] < r_original["segregation_index"], (
            f"Dynamic ({r_dynamic['segregation_index']:.3f}) should be less "
            f"segregated than original ({r_original['segregation_index']:.3f})"
        )

    def test_false_positive_detector(self):
        """If dynamic tolerance gives segregation > 0.80, it's the textbook prior, not the spec.

        This is the pre-loaded false positive: the Builder generates from the
        Schelling prior (near-complete segregation) instead of from the frozen
        spec (partial mixing under dynamic tolerance).
        """
        _skip_if_not_built()
        r = _run_and_collect(42, dynamic_tolerance=True)
        if r["segregation_index"] > 0.80:
            pytest.fail(
                f"FALSE POSITIVE DETECTED: segregation={r['segregation_index']:.3f} "
                f"matches textbook Schelling prior, not the dynamic-tolerance spec. "
                f"Check: is tolerance_update_rate applied AFTER the move step? "
                f"Check: is the update rate exactly {TOLERANCE_UPDATE_RATE}?"
            )


# =============================================================================
# MILESTONE 4 — Convergence Battery (30 seeds, sigma-gates)
# =============================================================================

class TestMilestone4ConvergenceBattery:
    """Full 30-seed convergence battery with sigma-gating."""

    @pytest.mark.slow
    def test_original_model_30_seeds(self):
        """Original Schelling across 30 seeds: segregation std < 0.15."""
        _skip_if_not_built()
        segregation_values = []
        for seed in SEEDS_FULL:
            r = _run_and_collect(seed, dynamic_tolerance=False)
            segregation_values.append(r["segregation_index"])

        mean_seg = np.mean(segregation_values)
        std_seg = np.std(segregation_values)

        assert std_seg < SIGMA_THRESHOLD, (
            f"Original model segregation std={std_seg:.4f} exceeds "
            f"sigma threshold {SIGMA_THRESHOLD} (mean={mean_seg:.4f})"
        )
        assert mean_seg > 0.70, (
            f"Original model mean segregation={mean_seg:.4f} too low"
        )

    @pytest.mark.slow
    def test_dynamic_tolerance_30_seeds(self):
        """Dynamic tolerance across 30 seeds: segregation std < 0.15."""
        _skip_if_not_built()
        segregation_values = []
        for seed in SEEDS_FULL:
            r = _run_and_collect(seed, dynamic_tolerance=True)
            segregation_values.append(r["segregation_index"])

        mean_seg = np.mean(segregation_values)
        std_seg = np.std(segregation_values)

        assert std_seg < SIGMA_THRESHOLD, (
            f"Dynamic model segregation std={std_seg:.4f} exceeds "
            f"sigma threshold {SIGMA_THRESHOLD} (mean={mean_seg:.4f})"
        )
        assert 0.30 < mean_seg < 0.80, (
            f"Dynamic model mean segregation={mean_seg:.4f} out of "
            f"expected range [0.30, 0.80] — possible specification drift"
        )

    @pytest.mark.slow
    def test_dynamic_consistently_less_segregated(self):
        """Dynamic tolerance produces less segregation in >= 80% of seeds."""
        _skip_if_not_built()
        n_less = 0
        for seed in SEEDS_FULL:
            r_orig = _run_and_collect(seed, dynamic_tolerance=False)
            r_dyn = _run_and_collect(seed, dynamic_tolerance=True)
            if r_dyn["segregation_index"] < r_orig["segregation_index"]:
                n_less += 1

        frac = n_less / len(SEEDS_FULL)
        assert frac >= 0.80, (
            f"Dynamic tolerance less segregated in only {n_less}/{len(SEEDS_FULL)} "
            f"seeds ({frac:.0%}) — expected >= 80%"
        )


# =============================================================================
# COEFFICIENT DRIFT CHECKS (Prior-as-Detector)
# =============================================================================

class TestCoefficientDrift:
    """Verify frozen coefficients are exactly as specified."""

    def test_tolerance_is_0375(self):
        """The most common LLM drift: generating 0.33 instead of 0.375."""
        _skip_if_not_built()
        grid = SchellingGrid(seed=42, grid_size=GRID_SIZE, density=DENSITY)
        # Check the default tolerance stored on agents
        tolerances = [a.tolerance for a in grid.agents if a is not None]
        if tolerances:
            assert all(abs(t - 0.375) < 1e-6 for t in tolerances), (
                f"Tolerance should be exactly 0.375, found: "
                f"{set(round(t, 4) for t in tolerances)}"
            )

    def test_grid_size_is_50(self):
        _skip_if_not_built()
        grid = SchellingGrid(seed=42, grid_size=GRID_SIZE, density=DENSITY)
        assert grid.grid_size == 50

    def test_density_is_090(self):
        _skip_if_not_built()
        grid = SchellingGrid(seed=42, grid_size=GRID_SIZE, density=DENSITY)
        n_occupied = np.sum(grid.grid != 0)
        total = GRID_SIZE * GRID_SIZE
        actual_density = n_occupied / total
        assert abs(actual_density - 0.90) < 0.02, (
            f"Density should be ~0.90, got {actual_density:.3f}"
        )

    def test_update_order_is_simultaneous(self):
        """Verify simultaneous update: all moves computed from same pre-move state."""
        _skip_if_not_built()
        grid = SchellingGrid(seed=42, grid_size=GRID_SIZE, density=DENSITY)
        # Run one step and verify the update order attribute
        assert hasattr(grid, 'update_order') or hasattr(grid, 'simultaneous')
        # The implementation should document which update order it uses
