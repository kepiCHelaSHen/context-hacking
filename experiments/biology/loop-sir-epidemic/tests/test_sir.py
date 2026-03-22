"""Tests for Stochastic SIR Epidemic Model."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sir_model import SIRModel, run_simulation


class TestReturnStructure:
    def test_returns_dict_with_required_keys(self):
        result = run_simulation(seed=42, n=100, max_ticks=50)
        expected_keys = {
            "peak_infected", "peak_tick", "final_recovered",
            "final_size_fraction", "fadeout", "epidemic_curve", "r0_recovered",
        }
        assert expected_keys <= set(result.keys())

    def test_epidemic_curve_is_list(self):
        result = run_simulation(seed=42, n=100, max_ticks=50)
        assert isinstance(result["epidemic_curve"], list)
        assert len(result["epidemic_curve"]) > 1


class TestInfectedIsInteger:
    def test_i_count_is_integer_at_each_step(self):
        model = SIRModel(seed=42, n=200)
        for _ in range(20):
            model.step()
            i_count = model.count_infected()
            assert isinstance(i_count, int), f"I(t) should be int, got {type(i_count)}"

    def test_epidemic_curve_values_are_integers(self):
        result = run_simulation(seed=42, n=200, max_ticks=50)
        for val in result["epidemic_curve"]:
            assert isinstance(val, int), f"Epidemic curve value should be int, got {type(val)}"


class TestFinalSizeRange:
    def test_final_size_fraction_in_valid_range(self):
        result = run_simulation(seed=42, n=500, max_ticks=300)
        assert 0.0 <= result["final_size_fraction"] <= 1.0

    def test_final_recovered_not_greater_than_n(self):
        n = 500
        result = run_simulation(seed=42, n=n, max_ticks=300)
        assert result["final_recovered"] <= n


class TestDeterminism:
    def test_same_seed_same_result(self):
        r1 = run_simulation(seed=77, n=200, max_ticks=100)
        r2 = run_simulation(seed=77, n=200, max_ticks=100)
        assert r1["peak_infected"] == r2["peak_infected"]
        assert r1["final_recovered"] == r2["final_recovered"]
        assert r1["epidemic_curve"] == r2["epidemic_curve"]


class TestConservation:
    def test_s_plus_i_plus_r_equals_n(self):
        n = 300
        model = SIRModel(seed=42, n=n)
        for _ in range(50):
            model.step()
            s = model.count_susceptible()
            i = model.count_infected()
            r = model.count_recovered()
            assert s + i + r == n, f"S+I+R={s+i+r} != N={n}"
