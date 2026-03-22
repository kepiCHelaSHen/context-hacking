"""Tests for Grover's Search Algorithm simulation."""

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from grover import GroverSimulator, run_simulation, K_OPTIMAL, N_ITEMS


class TestNItems:
    def test_n_equals_1024(self):
        assert N_ITEMS == 1024, f"N should be 1024, got {N_ITEMS}"

    def test_simulator_n_items(self):
        sim = GroverSimulator(n_qubits=10)
        assert sim.n_items == 1024


class TestOptimalIterations:
    def test_high_probability_at_k25(self):
        """At k_opt=25 iterations, success probability should exceed 0.90."""
        result = run_simulation(seed=42, n_qubits=10, iterations=25)
        assert result["success_probability"] > 0.90, \
            f"P(success) at k=25 should be > 0.90, got {result['success_probability']}"

    def test_k_opt_is_25(self):
        """k_opt = floor(pi/4 * sqrt(1024)) = floor(25.13) = 25."""
        assert K_OPTIMAL == 25, f"k_opt should be 25, got {K_OPTIMAL}"
        # Verify the formula
        expected = int(math.floor(math.pi / 4 * math.sqrt(1024)))
        assert expected == 25


class TestOvershoot:
    def test_overshoot_at_k35(self):
        """Overshooting beyond k_opt should reduce probability."""
        r_opt = run_simulation(seed=42, n_qubits=10, iterations=25)
        r_over = run_simulation(seed=42, n_qubits=10, iterations=35)
        assert r_over["success_probability"] < r_opt["success_probability"], \
            f"Overshoot at k=35 ({r_over['success_probability']}) should be < optimal k=25 ({r_opt['success_probability']})"


class TestPhaseFlipOracle:
    def test_oracle_is_phase_flip(self):
        """Oracle must flip the amplitude sign (phase flip), not return boolean."""
        sim = GroverSimulator(n_qubits=10, seed=42)
        sim.initialize()
        target = sim.target
        amp_before = sim.amplitudes[target]
        sim.apply_oracle()
        amp_after = sim.amplitudes[target]
        # Phase flip: amplitude should be negated
        assert abs(amp_after - (-amp_before)) < 1e-12, \
            f"Oracle should negate amplitude: before={amp_before}, after={amp_after}"

    def test_oracle_only_affects_target(self):
        """Oracle should only flip the target, leaving all other amplitudes unchanged."""
        sim = GroverSimulator(n_qubits=10, seed=42)
        sim.initialize()
        target = sim.target
        amps_before = sim.amplitudes.copy()
        sim.apply_oracle()
        for i in range(sim.n_items):
            if i == target:
                assert abs(sim.amplitudes[i] - (-amps_before[i])) < 1e-12
            else:
                assert abs(sim.amplitudes[i] - amps_before[i]) < 1e-12
