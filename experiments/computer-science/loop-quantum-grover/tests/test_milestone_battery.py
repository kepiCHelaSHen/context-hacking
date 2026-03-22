"""
Grover's Algorithm — CHP Milestone Test Battery

4 milestones x 30 random targets. Sigma-gated success probability.
Key test: iteration count = floor(pi/4 * sqrt(N)), not N/2 (classical).

Usage:
    pytest tests/test_milestone_battery.py -v
"""

import math
import numpy as np
import pytest

try:
    from grover import GroverSimulator, run_simulation
    GROVER_AVAILABLE = True
except ImportError:
    GROVER_AVAILABLE = False

# ── Frozen coefficients ──────────────────────────────────────────────────────
N_QUBITS = 10
N_ITEMS = 2 ** N_QUBITS  # 1024
K_OPTIMAL = int(math.floor(math.pi / 4 * math.sqrt(N_ITEMS)))  # 25
SUCCESS_THRESHOLD = 0.95

SIGMA_THRESHOLD = 0.15
SEEDS = list(range(1, 31))


def _skip():
    if not GROVER_AVAILABLE:
        pytest.skip("grover.py not yet built — run the CHP loop first")


def _run(seed: int, n_qubits: int = N_QUBITS, k: int | None = None) -> dict:
    _skip()
    return run_simulation(seed=seed, n_qubits=n_qubits,
                          iterations=k if k is not None else K_OPTIMAL)


# =============================================================================
# MILESTONE 1 — Foundation (state vector, Hadamard, oracle)
# =============================================================================

class TestMilestone1Foundation:

    def test_state_vector_size(self):
        _skip()
        sim = GroverSimulator(n_qubits=N_QUBITS, seed=42)
        assert len(sim.amplitudes) == N_ITEMS

    def test_initial_superposition(self):
        """After Hadamard, all amplitudes should be 1/sqrt(N)."""
        _skip()
        sim = GroverSimulator(n_qubits=N_QUBITS, seed=42)
        sim.initialize()
        expected = 1.0 / math.sqrt(N_ITEMS)
        assert np.allclose(np.abs(sim.amplitudes), expected, atol=1e-10)

    def test_oracle_flips_phase(self):
        """Oracle must flip the sign of the target amplitude, not return bool."""
        _skip()
        sim = GroverSimulator(n_qubits=N_QUBITS, seed=42)
        sim.initialize()
        target = sim.target
        amp_before = sim.amplitudes[target]
        sim.apply_oracle()
        amp_after = sim.amplitudes[target]
        assert np.isclose(amp_after, -amp_before), (
            f"Oracle should flip phase: before={amp_before}, after={amp_after}. "
            f"If unchanged, oracle may be boolean (returns True/False) instead "
            f"of quantum (flips amplitude sign)."
        )

    def test_oracle_leaves_others(self):
        """Non-target amplitudes should be unchanged by oracle."""
        _skip()
        sim = GroverSimulator(n_qubits=N_QUBITS, seed=42)
        sim.initialize()
        target = sim.target
        other = (target + 1) % N_ITEMS
        amp_before = sim.amplitudes[other]
        sim.apply_oracle()
        amp_after = sim.amplitudes[other]
        assert np.isclose(amp_after, amp_before)

    def test_state_vector_not_boolean(self):
        """Amplitudes must be complex/float, not boolean."""
        _skip()
        sim = GroverSimulator(n_qubits=N_QUBITS, seed=42)
        sim.initialize()
        assert sim.amplitudes.dtype in (np.float64, np.complex128, np.float32, np.complex64)

    def test_deterministic_given_seed(self):
        _skip()
        r1 = _run(42)
        r2 = _run(42)
        assert r1["success_probability"] == r2["success_probability"]


# =============================================================================
# MILESTONE 2 — Diffusion operator
# =============================================================================

class TestMilestone2Diffusion:

    def test_diffusion_changes_amplitudes(self):
        """After oracle + diffusion, target amplitude should INCREASE."""
        _skip()
        sim = GroverSimulator(n_qubits=N_QUBITS, seed=42)
        sim.initialize()
        initial_target_amp = abs(sim.amplitudes[sim.target])
        sim.apply_oracle()
        sim.apply_diffusion()
        after_amp = abs(sim.amplitudes[sim.target])
        assert after_amp > initial_target_amp, (
            f"Target amplitude should increase after one Grover iteration: "
            f"before={initial_target_amp:.6f}, after={after_amp:.6f}. "
            f"If unchanged, diffusion operator may be missing or wrong."
        )

    def test_normalization_preserved(self):
        """Sum of |amplitude|^2 must equal 1 after each iteration."""
        _skip()
        sim = GroverSimulator(n_qubits=N_QUBITS, seed=42)
        sim.initialize()
        for _ in range(5):
            sim.apply_oracle()
            sim.apply_diffusion()
            total = np.sum(np.abs(sim.amplitudes) ** 2)
            assert np.isclose(total, 1.0, atol=1e-8), (
                f"State not normalized: sum|amp|^2 = {total:.10f}"
            )

    def test_amplitude_sinusoidal(self):
        """Target amplitude should follow sinusoidal growth with iterations."""
        _skip()
        sim = GroverSimulator(n_qubits=N_QUBITS, seed=42)
        sim.initialize()
        amps = []
        for k in range(50):
            amps.append(abs(sim.amplitudes[sim.target]) ** 2)
            sim.apply_oracle()
            sim.apply_diffusion()

        arr = np.array(amps)
        # Should have at least one peak and one trough (sinusoidal)
        peaks = sum(1 for i in range(1, len(arr)-1) if arr[i] > arr[i-1] and arr[i] > arr[i+1])
        assert peaks >= 1, (
            f"Expected sinusoidal amplitude evolution, found {peaks} peaks. "
            f"Flat = no diffusion. Linear growth = classical search."
        )


# =============================================================================
# MILESTONE 3 — Verification
# =============================================================================

class TestMilestone3Verification:

    def test_success_at_k_optimal(self):
        """At k_opt=25 iterations, success probability should be > 0.95."""
        _skip()
        r = _run(42, k=K_OPTIMAL)
        assert r["success_probability"] > SUCCESS_THRESHOLD, (
            f"P(success) = {r['success_probability']:.4f} at k={K_OPTIMAL} — "
            f"too low. Expected > {SUCCESS_THRESHOLD}."
        )

    def test_k_optimal_is_25(self):
        """Optimal iteration count for N=1024 must be exactly 25."""
        k = int(math.floor(math.pi / 4 * math.sqrt(N_ITEMS)))
        assert k == 25

    def test_overshoot_reduces_success(self):
        """Going beyond k_opt should REDUCE success probability (sinusoidal)."""
        _skip()
        r_opt = _run(42, k=K_OPTIMAL)
        r_over = _run(42, k=K_OPTIMAL + 10)
        assert r_over["success_probability"] < r_opt["success_probability"], (
            f"Overshooting k_opt should reduce P(success): "
            f"k={K_OPTIMAL}: {r_opt['success_probability']:.4f}, "
            f"k={K_OPTIMAL+10}: {r_over['success_probability']:.4f}"
        )

    def test_classical_contamination_detector(self):
        """If success requires ~N/2 iterations, it's classical search.

        Classical random search: expected iterations = N/2 = 512.
        Grover: optimal iterations = 25.
        If the algorithm needs > 100 iterations to find the target reliably,
        it's classical, not quantum.
        """
        _skip()
        r = _run(42, k=K_OPTIMAL)
        if r["success_probability"] < 0.50:
            pytest.fail(
                f"FALSE POSITIVE RISK: P(success) = {r['success_probability']:.4f} "
                f"at k={K_OPTIMAL}. This is too low for Grover's algorithm. "
                f"Classical search needs ~512 iterations for N=1024. "
                f"Check: is the oracle a phase flip? Is diffusion present?"
            )

    def test_n_sweep_quadratic_speedup(self):
        """k_opt should scale as sqrt(N), not linearly with N."""
        _skip()
        for n_qubits, expected_k in [(6, 6), (8, 12), (10, 25)]:
            n_items = 2 ** n_qubits
            k = int(math.floor(math.pi / 4 * math.sqrt(n_items)))
            assert k == expected_k, f"n={n_qubits}: expected k={expected_k}, got {k}"

            r = _run(42, n_qubits=n_qubits, k=k)
            assert r["success_probability"] > 0.90, (
                f"n_qubits={n_qubits}, k={k}: P={r['success_probability']:.4f} < 0.90"
            )


# =============================================================================
# MILESTONE 4 — Convergence Battery
# =============================================================================

class TestMilestone4ConvergenceBattery:

    @pytest.mark.slow
    def test_success_probability_30_targets(self):
        """Success probability across 30 random targets: all > 0.95."""
        _skip()
        probs = []
        for seed in SEEDS:
            r = _run(seed, k=K_OPTIMAL)
            probs.append(r["success_probability"])

        mean_p = np.mean(probs)
        std_p = np.std(probs)

        assert std_p < SIGMA_THRESHOLD, (
            f"Success probability std={std_p:.4f} exceeds {SIGMA_THRESHOLD}. "
            f"High variance suggests the algorithm is stochastic (classical) "
            f"rather than deterministic quantum."
        )
        assert mean_p > 0.95, (
            f"Mean success probability={mean_p:.4f} < 0.95"
        )

    @pytest.mark.slow
    def test_all_targets_found(self):
        """Every random target should be findable with P > 0.90."""
        _skip()
        for seed in SEEDS:
            r = _run(seed, k=K_OPTIMAL)
            assert r["success_probability"] > 0.90, (
                f"Seed {seed}: P={r['success_probability']:.4f} — target not found"
            )


# =============================================================================
# COEFFICIENT DRIFT CHECKS
# =============================================================================

class TestCoefficientDrift:

    def test_n_qubits_is_10(self):
        _skip()
        sim = GroverSimulator(n_qubits=N_QUBITS, seed=42)
        assert sim.n_qubits == 10

    def test_n_items_is_1024(self):
        _skip()
        sim = GroverSimulator(n_qubits=N_QUBITS, seed=42)
        assert len(sim.amplitudes) == 1024

    def test_oracle_is_phase_flip(self):
        """Oracle must be phase flip, not boolean return."""
        _skip()
        import inspect
        source = inspect.getsource(GroverSimulator)
        # Phase flip: amplitudes[target] *= -1 or equivalent
        assert "*= -1" in source or "* -1" in source or "negate" in source.lower(), (
            "No phase flip pattern found — oracle may be classical boolean"
        )

    def test_diffusion_present(self):
        """Diffusion operator must be explicitly implemented."""
        _skip()
        assert hasattr(GroverSimulator, 'apply_diffusion'), (
            "No apply_diffusion method — diffusion operator is missing"
        )
