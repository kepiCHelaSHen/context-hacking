"""Tests for Izhikevich (2003) Spiking Neuron Model."""

import sys
import os
import inspect

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from izhikevich import IzhikevichNeuron, run_simulation


class TestReturnStructure:
    def test_returns_v_trace_and_spike_count(self):
        result = run_simulation()
        assert "v_trace" in result
        assert "spike_count" in result
        assert isinstance(result["v_trace"], list)
        assert isinstance(result["spike_count"], int)
        assert len(result["v_trace"]) > 0

    def test_returns_spike_times(self):
        result = run_simulation()
        assert "spike_times" in result
        assert isinstance(result["spike_times"], list)


class TestTwoStateVars:
    def test_only_v_and_u_state_variables(self):
        """Izhikevich model has exactly 2 state variables (v, u).
        NOT 4 like Hodgkin-Huxley (V, m, h, n)."""
        neuron = IzhikevichNeuron(a=0.02, b=0.2, c=-65.0, d=8.0)
        # Check that only v and u exist as state variables
        assert hasattr(neuron, "v")
        assert hasattr(neuron, "u")
        # Should NOT have HH-style gating variables
        assert not hasattr(neuron, "m"), "m is a HH gating variable, not Izhikevich"
        assert not hasattr(neuron, "h"), "h is a HH gating variable, not Izhikevich"
        assert not hasattr(neuron, "n"), "n is a HH gating variable, not Izhikevich"

    def test_no_hh_contamination_in_source(self):
        """Source should not contain HH-specific terms."""
        source = inspect.getsource(IzhikevichNeuron)
        assert "gNa" not in source, "gNa is Hodgkin-Huxley, not Izhikevich"
        assert "gK" not in source, "gK is Hodgkin-Huxley, not Izhikevich"
        assert "gL" not in source, "gL is Hodgkin-Huxley, not Izhikevich"


class TestRSRegularSpiking:
    def test_rs_produces_regular_spikes(self):
        """Regular Spiking (RS): a=0.02, b=0.2, c=-65, d=8."""
        result = run_simulation(a=0.02, b=0.2, c=-65.0, d=8.0, I=10.0)
        assert result["spike_count"] > 5, f"RS should spike regularly, got {result['spike_count']} spikes"
        # ISI CV should be low (regular)
        assert result["isi_cv"] < 0.5, f"RS should have low ISI CV, got {result['isi_cv']}"


class TestFSFiresMore:
    def test_fs_fires_more_than_rs(self):
        """Fast Spiking (FS): a=0.1, b=0.2, c=-65, d=2 should fire faster than RS."""
        rs = run_simulation(a=0.02, b=0.2, c=-65.0, d=8.0, I=10.0, duration=1000)
        fs = run_simulation(a=0.1, b=0.2, c=-65.0, d=2.0, I=10.0, duration=1000)
        assert fs["spike_count"] > rs["spike_count"], \
            f"FS ({fs['spike_count']} spikes) should fire more than RS ({rs['spike_count']} spikes)"


class TestAllFivePatternsSpike:
    def test_all_five_patterns_produce_spikes(self):
        """All 5 standard Izhikevich patterns should produce spikes with sufficient input."""
        patterns = {
            "RS": dict(a=0.02, b=0.2, c=-65.0, d=8.0),
            "IB": dict(a=0.02, b=0.2, c=-55.0, d=4.0),
            "CH": dict(a=0.02, b=0.2, c=-50.0, d=2.0),
            "FS": dict(a=0.1, b=0.2, c=-65.0, d=2.0),
            "LTS": dict(a=0.02, b=0.25, c=-65.0, d=2.0),
        }
        for name, params in patterns.items():
            result = run_simulation(**params, I=10.0, duration=1000)
            assert result["spike_count"] > 0, \
                f"Pattern {name} should produce spikes, got {result['spike_count']}"
