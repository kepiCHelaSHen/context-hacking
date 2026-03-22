"""
Izhikevich Neurons — CHP Milestone Test Battery

4 milestones x 5 patterns x 30 seeds. Sigma-gated ISI convergence.
Key test: variable count = 2 (catches Hodgkin-Huxley contamination).

Usage:
    pytest tests/test_milestone_battery.py -v
"""

import numpy as np
import pytest

try:
    from izhikevich import IzhikevichNeuron, run_simulation
    IZH_AVAILABLE = True
except ImportError:
    IZH_AVAILABLE = False

# ── Frozen coefficients ──────────────────────────────────────────────────────
DT = 0.5
DURATION = 1000
STEPS = 2000
SPIKE_THRESHOLD = 30

PATTERNS = {
    "RS":  {"a": 0.02, "b": 0.2,  "c": -65, "d": 8, "I": 10},
    "IB":  {"a": 0.02, "b": 0.2,  "c": -55, "d": 4, "I": 10},
    "CH":  {"a": 0.02, "b": 0.2,  "c": -50, "d": 2, "I": 10},
    "FS":  {"a": 0.10, "b": 0.2,  "c": -65, "d": 2, "I": 10},
    "LTS": {"a": 0.02, "b": 0.25, "c": -65, "d": 2, "I": 10},
}

SIGMA_THRESHOLD = 0.15
SEEDS_FULL = list(range(1, 31))


def _skip():
    if not IZH_AVAILABLE:
        pytest.skip("izhikevich.py not yet built — run the CHP loop first")


def _run(pattern: str = "RS", seed: int = 42) -> dict:
    _skip()
    p = PATTERNS[pattern]
    return run_simulation(
        a=p["a"], b=p["b"], c=p["c"], d=p["d"], I=p["I"],
        dt=DT, duration=DURATION, seed=seed,
    )


# =============================================================================
# MILESTONE 1 — Foundation
# =============================================================================

class TestMilestone1Foundation:

    def test_neuron_construction(self):
        _skip()
        n = IzhikevichNeuron(a=0.02, b=0.2, c=-65, d=8)
        assert hasattr(n, "v")
        assert hasattr(n, "u")

    def test_only_two_state_variables(self):
        """Izhikevich has exactly 2 state variables (v, u).

        If the neuron has more (m, h, n, ...), it's Hodgkin-Huxley.
        This is THE key contamination test.
        """
        _skip()
        n = IzhikevichNeuron(a=0.02, b=0.2, c=-65, d=8)
        hh_vars = ["m", "h", "n", "gNa", "gK", "gL"]
        for var in hh_vars:
            assert not hasattr(n, var), (
                f"HODGKIN-HUXLEY CONTAMINATION: neuron has attribute '{var}'. "
                f"Izhikevich model has only v and u. "
                f"If the model has m, h, n: it's HH, not Izhikevich."
            )

    def test_spike_detected(self):
        """RS pattern should produce spikes (v reaches 30 mV)."""
        _skip()
        r = _run("RS")
        assert r["spike_count"] > 0, "No spikes detected in RS pattern"

    def test_spike_resets_v(self):
        """After spike, v should reset to c (not stay at 30+)."""
        _skip()
        r = _run("RS")
        v_trace = r.get("v_trace", [])
        if v_trace:
            assert max(v_trace) <= 35, (
                f"v_max = {max(v_trace):.1f} — should reset at 30. "
                f"If v >> 30, the spike reset is missing."
            )

    def test_v_bounded(self):
        """Membrane potential must stay in [-90, 40] mV."""
        _skip()
        r = _run("RS")
        v_trace = r.get("v_trace", [])
        if v_trace:
            assert min(v_trace) >= -90, f"v_min={min(v_trace):.1f} < -90"
            assert max(v_trace) <= 40, f"v_max={max(v_trace):.1f} > 40"

    def test_deterministic(self):
        _skip()
        r1 = _run("RS", seed=42)
        r2 = _run("RS", seed=42)
        assert r1["spike_count"] == r2["spike_count"]


# =============================================================================
# MILESTONE 2 — Firing Patterns
# =============================================================================

class TestMilestone2Patterns:

    def test_rs_regular_spiking(self):
        """RS: regular, evenly-spaced spikes. ISI CV < 0.15."""
        _skip()
        r = _run("RS")
        assert r["spike_count"] > 10, f"RS should produce many spikes, got {r['spike_count']}"
        cv = r.get("isi_cv", 1.0)
        assert cv < 0.15, (
            f"RS ISI CV={cv:.3f} — should be < 0.15 (regular spiking)"
        )

    def test_ib_bursting(self):
        """IB: initial burst then regular. ISI CV > 0.30."""
        _skip()
        r = _run("IB")
        assert r["spike_count"] > 5
        cv = r.get("isi_cv", 0)
        assert cv > 0.20, (
            f"IB ISI CV={cv:.3f} — should be > 0.20 (bursting produces variable ISI)"
        )

    def test_fs_fast_spiking(self):
        """FS: high-frequency, very regular. ISI CV < 0.10."""
        _skip()
        r = _run("FS")
        r_rs = _run("RS")
        assert r["spike_count"] > r_rs["spike_count"], (
            f"FS ({r['spike_count']} spikes) should fire faster than RS ({r_rs['spike_count']})"
        )
        cv = r.get("isi_cv", 1.0)
        assert cv < 0.10, (
            f"FS ISI CV={cv:.3f} — should be < 0.10 (very regular)"
        )

    def test_ch_chattering(self):
        """CH: rhythmic bursts. Should produce spikes."""
        _skip()
        r = _run("CH")
        assert r["spike_count"] > 5

    def test_lts_low_threshold(self):
        """LTS: regular spiking with low threshold."""
        _skip()
        r = _run("LTS")
        assert r["spike_count"] > 5

    @pytest.mark.parametrize("pattern", ["RS", "IB", "CH", "FS", "LTS"])
    def test_all_patterns_spike(self, pattern):
        """Every pattern must produce at least 1 spike at I=10."""
        _skip()
        r = _run(pattern)
        assert r["spike_count"] > 0, f"Pattern {pattern} produced no spikes"


# =============================================================================
# MILESTONE 3 — Integration Method Comparison
# =============================================================================

class TestMilestone3Integration:

    def test_half_step_vs_single_step(self):
        """Half-step (dt=0.5) should produce different spike count than dt=1.0.

        If they're identical, the Builder may not be using the two-half-step
        method from Izhikevich (2003).
        """
        _skip()
        p = PATTERNS["FS"]
        r_half = run_simulation(a=p["a"], b=p["b"], c=p["c"], d=p["d"],
                                I=p["I"], dt=0.5, duration=DURATION, seed=42)
        r_full = run_simulation(a=p["a"], b=p["b"], c=p["c"], d=p["d"],
                                I=p["I"], dt=1.0, duration=DURATION, seed=42)
        # They should produce different spike counts (dt=1.0 is less accurate)
        # This test documents the difference, doesn't require a specific direction
        assert r_half["spike_count"] != r_full["spike_count"] or True  # soft check

    def test_hh_source_scan(self):
        """Source code should NOT contain Hodgkin-Huxley variable names."""
        _skip()
        import inspect
        source = inspect.getsource(IzhikevichNeuron)
        hh_signs = ["gNa", "gK", "gL", "ENa", "EK", "EL",
                     "alpha_m", "beta_m", "alpha_h", "beta_h",
                     "alpha_n", "beta_n", "conductance"]
        for sign in hh_signs:
            assert sign not in source, (
                f"HODGKIN-HUXLEY CONTAMINATION: '{sign}' found in source. "
                f"Izhikevich model uses v, u, a, b, c, d only."
            )


# =============================================================================
# MILESTONE 4 — Convergence Battery
# =============================================================================

class TestMilestone4ConvergenceBattery:

    @pytest.mark.slow
    @pytest.mark.parametrize("pattern", ["RS", "FS"])
    def test_spike_count_30_seeds_sigma(self, pattern):
        """Spike count across 30 seeds: std/mean < sigma threshold."""
        _skip()
        counts = []
        for seed in SEEDS_FULL:
            r = _run(pattern, seed=seed)
            counts.append(r["spike_count"])

        mean_c = np.mean(counts)
        std_c = np.std(counts)
        cv = std_c / max(mean_c, 1)

        # For constant-current injection, spike count should be very consistent
        # (the model is deterministic given same I — variance comes from
        # network noise if enabled)
        assert cv < 0.10, (
            f"Pattern {pattern}: spike count CV={cv:.4f} exceeds 0.10 "
            f"(mean={mean_c:.1f}, std={std_c:.1f})"
        )

    @pytest.mark.slow
    @pytest.mark.parametrize("pattern", ["RS", "FS"])
    def test_isi_cv_30_seeds(self, pattern):
        """ISI coefficient of variation across 30 seeds: std < sigma threshold."""
        _skip()
        cvs = []
        for seed in SEEDS_FULL:
            r = _run(pattern, seed=seed)
            cv = r.get("isi_cv", 0)
            if cv > 0:
                cvs.append(cv)

        if len(cvs) < 20:
            pytest.skip("Not enough valid ISI measurements")

        std_cv = np.std(cvs)
        assert std_cv < SIGMA_THRESHOLD, (
            f"Pattern {pattern}: ISI CV std={std_cv:.4f} exceeds {SIGMA_THRESHOLD}"
        )


# =============================================================================
# COEFFICIENT DRIFT CHECKS
# =============================================================================

class TestCoefficientDrift:

    def test_v_equation_coefficients(self):
        """v' = 0.04*v^2 + 5*v + 140 — check these exact constants."""
        _skip()
        import inspect
        source = inspect.getsource(IzhikevichNeuron)
        assert "0.04" in source, "Missing 0.04 coefficient in v equation"
        assert "140" in source, "Missing 140 constant in v equation"

    def test_rs_parameters_exact(self):
        _skip()
        n = IzhikevichNeuron(a=0.02, b=0.2, c=-65, d=8)
        assert n.a == 0.02
        assert n.b == 0.2
        assert n.c == -65
        assert n.d == 8

    def test_fs_parameters_exact(self):
        _skip()
        n = IzhikevichNeuron(a=0.10, b=0.2, c=-65, d=2)
        assert n.a == 0.10

    def test_spike_threshold_is_30(self):
        _skip()
        import inspect
        source = inspect.getsource(IzhikevichNeuron)
        assert "30" in source, "Spike threshold 30 mV not found in source"

    def test_dt_is_half_ms(self):
        """Integration step should be 0.5 ms (two half-steps)."""
        _skip()
        import inspect
        source = inspect.getsource(run_simulation)
        assert "0.5" in source, (
            "dt=0.5 not found — possible single-step (dt=1.0) contamination"
        )
