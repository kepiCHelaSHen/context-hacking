"""Tests for Spatial Prisoner's Dilemma — Nowak & May (1992)."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from spatial_pd import SpatialPDGrid, run_simulation


class TestSpatialPDGridInit:
    def test_init_default_grid(self):
        grid = SpatialPDGrid()
        assert grid.grid_size == 100
        assert grid.b == 1.8
        assert grid.grid.shape == (100, 100)

    def test_init_all_cooperators(self):
        grid = SpatialPDGrid(grid_size=10)
        # Grid starts as all ones (cooperators)
        assert grid.cooperation_rate() == 1.0


class TestCooperationRate:
    def test_cooperation_rate_bounds(self):
        result = run_simulation(seed=42, grid_size=20, generations=50)
        cr = result["cooperation_rate"]
        assert 0.0 <= cr <= 1.0

    def test_cooperation_rate_after_steps(self):
        grid = SpatialPDGrid(grid_size=10)
        grid.set_initial("single_defector_center")
        for _ in range(5):
            grid.step()
        cr = grid.cooperation_rate()
        assert 0.0 <= cr <= 1.0


class TestDeterminism:
    def test_deterministic_with_same_seed(self):
        r1 = run_simulation(seed=123, grid_size=20, generations=50)
        r2 = run_simulation(seed=123, grid_size=20, generations=50)
        assert r1["cooperation_rate"] == r2["cooperation_rate"]
        assert r1["spatial_clustering"] == r2["spatial_clustering"]
        assert r1["generations_run"] == r2["generations_run"]

    def test_different_seeds_may_differ(self):
        r1 = run_simulation(seed=1, grid_size=20, initial_condition="random_half", generations=50)
        r2 = run_simulation(seed=999, grid_size=20, initial_condition="random_half", generations=50)
        # Different seeds with random init should generally produce different results
        # (not guaranteed but overwhelmingly likely)
        assert (r1["cooperation_rate"] != r2["cooperation_rate"]
                or r1["generations_run"] != r2["generations_run"])


class TestCoexistence:
    def test_b_1_8_coexistence(self):
        """At b=1.8 (Nowak & May), cooperators and defectors coexist."""
        result = run_simulation(seed=42, grid_size=50, b=1.8, generations=200)
        cr = result["cooperation_rate"]
        # Coexistence: neither total cooperation nor total defection
        assert 0.01 < cr < 0.99, f"Expected coexistence, got cooperation_rate={cr}"
