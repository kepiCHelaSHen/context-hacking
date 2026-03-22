"""Tests for Agent-Based Lotka-Volterra predator-prey model."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lotka_volterra import LotkaVolterraGrid, run_simulation


class TestReturnStructure:
    def test_returns_trajectories(self):
        result = run_simulation(seed=42, max_ticks=50)
        assert "prey_trajectory" in result
        assert "predator_trajectory" in result
        assert isinstance(result["prey_trajectory"], list)
        assert isinstance(result["predator_trajectory"], list)
        assert len(result["prey_trajectory"]) > 1
        assert len(result["predator_trajectory"]) > 1

    def test_returns_count_fields(self):
        result = run_simulation(seed=42, max_ticks=50)
        assert "prey_count" in result
        assert "predator_count" in result
        assert "prey_extinct" in result
        assert "predator_extinct" in result


class TestNoisy:
    def test_agent_based_not_deterministic_ode(self):
        """Different seeds should produce different trajectories (agent-based noise)."""
        r1 = run_simulation(seed=1, max_ticks=100)
        r2 = run_simulation(seed=2, max_ticks=100)
        # Agent-based model is stochastic; different seeds -> different results
        assert r1["prey_trajectory"] != r2["prey_trajectory"]


class TestIntegerPopulations:
    def test_populations_are_integers(self):
        result = run_simulation(seed=42, max_ticks=100)
        for val in result["prey_trajectory"]:
            assert isinstance(val, int), f"Prey count should be int, got {type(val)}"
        for val in result["predator_trajectory"]:
            assert isinstance(val, int), f"Predator count should be int, got {type(val)}"

    def test_populations_non_negative(self):
        result = run_simulation(seed=42, max_ticks=100)
        for val in result["prey_trajectory"]:
            assert val >= 0
        for val in result["predator_trajectory"]:
            assert val >= 0


class TestExtinction:
    def test_extinction_possible_in_some_seeds(self):
        """At least one seed out of 20 should show predator or prey extinction.
        Use a small grid and high predator ratio to make extinction likely and fast."""
        any_extinct = False
        for seed in range(20):
            result = run_simulation(
                seed=seed, grid_w=20, grid_h=20,
                initial_prey=30, initial_predators=40,
                max_ticks=200,
            )
            if result["prey_extinct"] or result["predator_extinct"]:
                any_extinct = True
                break
        assert any_extinct, "Expected at least one extinction event across 20 seeds"
