"""
Stochastic SIR Epidemic — CHP Milestone Test Battery

4 milestones x 30 seeds. Sigma-gated convergence verification.
Key test: fadeout_rate > 0 (catches deterministic contamination).

Usage:
    pytest tests/test_milestone_battery.py -v
"""

import numpy as np
import pytest

try:
    from sir_model import SIRModel, run_simulation
    SIR_AVAILABLE = True
except ImportError:
    SIR_AVAILABLE = False

# ── Frozen coefficients ──────────────────────────────────────────────────────
N = 500
INITIAL_INFECTED = 5
BETA = 0.03
GAMMA = 0.10
CONTACTS_PER_TICK = 10
MAX_TICKS = 300
R0_EXPECTED = BETA * CONTACTS_PER_TICK * (1 / GAMMA)  # = 3.0

SIGMA_THRESHOLD = 0.15
SEEDS_QUICK = [42, 137, 271]
SEEDS_FULL = list(range(1, 31))


def _skip():
    if not SIR_AVAILABLE:
        pytest.skip("sir_model.py not yet built — run the CHP loop first")


def _run(seed: int, n: int = N, i0: int = INITIAL_INFECTED,
         beta: float = BETA, gamma: float = GAMMA,
         contacts: int = CONTACTS_PER_TICK, ticks: int = MAX_TICKS) -> dict:
    _skip()
    return run_simulation(
        seed=seed, n=n, initial_infected=i0,
        beta=beta, gamma=gamma, contacts_per_tick=contacts,
        max_ticks=ticks,
    )


# =============================================================================
# MILESTONE 1 — Foundation
# =============================================================================

class TestMilestone1Foundation:

    def test_construction(self):
        _skip()
        model = SIRModel(seed=42, n=N, initial_infected=INITIAL_INFECTED,
                         beta=BETA, gamma=GAMMA, contacts_per_tick=CONTACTS_PER_TICK)
        assert model.n == N
        assert model.count_infected() == INITIAL_INFECTED
        assert model.count_susceptible() == N - INITIAL_INFECTED

    def test_step_no_crash(self):
        _skip()
        r = _run(42, ticks=10)
        assert r["peak_infected"] > 0

    def test_deterministic(self):
        _skip()
        r1 = _run(42)
        r2 = _run(42)
        assert r1["final_recovered"] == r2["final_recovered"]

    def test_different_seeds_differ(self):
        _skip()
        r1 = _run(42)
        r2 = _run(137)
        # Stochastic — different seeds should produce different trajectories
        assert r1["final_recovered"] != r2["final_recovered"] or r1["peak_tick"] != r2["peak_tick"]

    def test_infected_count_is_integer(self):
        """I(t) must be an integer (discrete agents), not a float.

        If I(t) is a float, the Builder implemented deterministic rate equations.
        """
        _skip()
        r = _run(42, ticks=50)
        trajectory = r.get("epidemic_curve", [])
        for val in trajectory:
            assert isinstance(val, (int, np.integer)), (
                f"I(t) = {val} (type={type(val).__name__}) — must be integer. "
                f"Float-valued I(t) indicates deterministic contamination."
            )

    def test_conservation(self):
        """S + I + R = N at every tick (no agents created or destroyed)."""
        _skip()
        model = SIRModel(seed=42, n=N, initial_infected=INITIAL_INFECTED,
                         beta=BETA, gamma=GAMMA, contacts_per_tick=CONTACTS_PER_TICK)
        for _ in range(50):
            model.step()
            total = model.count_susceptible() + model.count_infected() + model.count_recovered()
            assert total == N, f"S+I+R={total} != N={N} — conservation violated"


# =============================================================================
# MILESTONE 2 — Metrics
# =============================================================================

class TestMilestone2Metrics:

    def test_final_size_reasonable(self):
        """At R0=3.0, most runs should produce a substantial epidemic."""
        _skip()
        r = _run(42)
        if not r.get("fadeout", False):
            assert r["final_size_fraction"] > 0.50, (
                f"Non-fadeout epidemic with R0=3 should infect >50%, "
                f"got {r['final_size_fraction']:.3f}"
            )

    def test_peak_timing(self):
        """Peak should occur before tick 100 for R0=3.0."""
        _skip()
        r = _run(42)
        if not r.get("fadeout", False):
            assert r["peak_tick"] < 100, (
                f"Peak at tick {r['peak_tick']} — too late for R0=3.0"
            )

    def test_r0_recovery(self):
        """Inferred R0 should be within +/-50% of true R0."""
        _skip()
        r = _run(42)
        if not r.get("fadeout", False) and "r0_recovered" in r:
            assert 1.5 < r["r0_recovered"] < 6.0, (
                f"Inferred R0={r['r0_recovered']:.2f}, expected ~{R0_EXPECTED:.1f}"
            )

    @pytest.mark.parametrize("seed", SEEDS_QUICK)
    def test_quick_bound_check(self, seed):
        """Quick 3-seed check: epidemic occurs or fadeout detected."""
        _skip()
        r = _run(seed)
        assert r["final_recovered"] > 0, "At least some infection should occur"


# =============================================================================
# MILESTONE 3 — Fadeout Experiment
# =============================================================================

class TestMilestone3Fadeout:

    def test_fadeout_rate_nonzero(self):
        """At N=500, I(0)=5, R0=3.0: fadeout rate must be > 0%.

        This is THE key test. The deterministic SIR predicts zero fadeout
        for R0 > 1. The stochastic model at N=500 with I(0)=5 shows fadeout
        in approximately 5-15% of runs.
        """
        _skip()
        n_fadeout = 0
        for seed in SEEDS_FULL:
            r = _run(seed)
            if r.get("fadeout", False):
                n_fadeout += 1

        fadeout_rate = n_fadeout / len(SEEDS_FULL)
        assert fadeout_rate > 0.0, (
            f"FALSE POSITIVE DETECTED: fadeout rate = 0% across "
            f"{len(SEEDS_FULL)} seeds at N={N}, I(0)={INITIAL_INFECTED}. "
            f"The deterministic SIR predicts zero fadeout. "
            f"The stochastic model should show 5-15% fadeout. "
            f"Check: is each agent a discrete individual with integer state? "
            f"Or did the Builder generate dS/dt rate equations?"
        )

    def test_fadeout_increases_at_small_n(self):
        """Smaller populations should have higher fadeout rates."""
        _skip()
        n_fade_small = 0
        n_fade_default = 0
        for seed in SEEDS_FULL[:15]:
            r_small = _run(seed, n=100, i0=2)
            r_default = _run(seed)
            if r_small.get("fadeout", False):
                n_fade_small += 1
            if r_default.get("fadeout", False):
                n_fade_default += 1

        assert n_fade_small >= n_fade_default, (
            f"Fadeout at N=100 ({n_fade_small}/15) should be >= N=500 "
            f"({n_fade_default}/15). Demographic stochasticity is stronger "
            f"at small N."
        )

    def test_fadeout_near_zero_at_large_n(self):
        """Large populations should rarely show fadeout."""
        _skip()
        n_fade = 0
        for seed in SEEDS_FULL[:10]:
            r = _run(seed, n=5000, i0=50)
            if r.get("fadeout", False):
                n_fade += 1

        assert n_fade <= 1, (
            f"N=5000 with I(0)=50 should have ~0% fadeout, got {n_fade}/10"
        )

    def test_fadeout_happens_early(self):
        """When fadeout occurs, it should happen in the first 10-30 ticks."""
        _skip()
        for seed in SEEDS_FULL:
            r = _run(seed)
            if r.get("fadeout", False):
                curve = r.get("epidemic_curve", [])
                # Find when I(t) first hits zero
                zero_tick = next((i for i, v in enumerate(curve) if v == 0), None)
                if zero_tick is not None:
                    assert zero_tick < 50, (
                        f"Fadeout at tick {zero_tick} — should occur early (<50). "
                        f"Late fadeout suggests a different mechanism."
                    )
                break  # Only need to check one fadeout event


# =============================================================================
# MILESTONE 4 — Convergence Battery
# =============================================================================

class TestMilestone4ConvergenceBattery:

    @pytest.mark.slow
    def test_final_size_30_seeds_sigma(self):
        """Final epidemic size across 30 non-fadeout runs: std/mean < threshold."""
        _skip()
        sizes = []
        for seed in SEEDS_FULL:
            r = _run(seed)
            if not r.get("fadeout", False):
                sizes.append(r["final_size_fraction"])

        if len(sizes) < 20:
            pytest.skip("Too many fadeouts for sigma test")

        mean_s = np.mean(sizes)
        std_s = np.std(sizes)
        cv = std_s / max(mean_s, 0.01)

        assert cv < 0.10, (
            f"Final size CV={cv:.4f} exceeds threshold "
            f"(mean={mean_s:.4f}, std={std_s:.4f})"
        )
        assert 0.80 < mean_s < 0.97, (
            f"Mean final size={mean_s:.4f} out of expected range for R0=3.0"
        )

    @pytest.mark.slow
    def test_peak_timing_30_seeds_sigma(self):
        """Peak tick across 30 non-fadeout runs: std < threshold."""
        _skip()
        peaks = []
        for seed in SEEDS_FULL:
            r = _run(seed)
            if not r.get("fadeout", False):
                peaks.append(r["peak_tick"])

        if len(peaks) < 20:
            pytest.skip("Too many fadeouts")

        mean_p = np.mean(peaks)
        std_p = np.std(peaks)
        relative_std = std_p / max(mean_p, 1)

        assert relative_std < SIGMA_THRESHOLD, (
            f"Peak timing relative std={relative_std:.4f} exceeds {SIGMA_THRESHOLD}"
        )


# =============================================================================
# COEFFICIENT DRIFT CHECKS
# =============================================================================

class TestCoefficientDrift:

    def test_no_rate_equation_variables(self):
        """Check source doesn't use deterministic SIR variable patterns."""
        _skip()
        import inspect
        source = inspect.getsource(SIRModel)
        deterministic_signs = [
            "dS/dt", "dI/dt", "dR/dt",
            "beta * S * I / N",
            "beta * s * i / n",
        ]
        for sign in deterministic_signs:
            assert sign not in source, (
                f"Deterministic SIR pattern '{sign}' found in source — "
                f"this should be individual-based, not rate equations"
            )

    def test_beta_exact(self):
        _skip()
        model = SIRModel(seed=42, n=N, initial_infected=INITIAL_INFECTED,
                         beta=BETA, gamma=GAMMA, contacts_per_tick=CONTACTS_PER_TICK)
        assert abs(model.beta - BETA) < 1e-6, f"Beta should be {BETA}, got {model.beta}"

    def test_gamma_exact(self):
        _skip()
        model = SIRModel(seed=42, n=N, initial_infected=INITIAL_INFECTED,
                         beta=BETA, gamma=GAMMA, contacts_per_tick=CONTACTS_PER_TICK)
        assert abs(model.gamma - GAMMA) < 1e-6

    def test_contacts_exact(self):
        _skip()
        model = SIRModel(seed=42, n=N, initial_infected=INITIAL_INFECTED,
                         beta=BETA, gamma=GAMMA, contacts_per_tick=CONTACTS_PER_TICK)
        assert model.contacts_per_tick == 10

    def test_r0_correct(self):
        """R0 = beta * contacts * (1/gamma) = 0.03 * 10 * 10 = 3.0."""
        r0 = BETA * CONTACTS_PER_TICK * (1 / GAMMA)
        assert abs(r0 - 3.0) < 1e-6
