"""
SIMSIV v1 Replication — CHP Milestone Test Battery

16 milestones. The largest CHP experiment: 35 traits, 9 engines, ~10,000 lines.
Sigma-gates based on actual calibration targets from the published paper.

Usage:
    pytest tests/test_milestone_battery.py -v
"""

import numpy as np
import pytest

SIGMA_THRESHOLD = 0.15
SEEDS = list(range(1, 11))

# These tests define the SPEC for what the Builder must produce.
# They will fail until the simulation is built by the CHP loop.

try:
    from simulation import Simulation
    from config import Config
    SIM_AVAILABLE = True
except ImportError:
    SIM_AVAILABLE = False


def _skip():
    if not SIM_AVAILABLE:
        pytest.skip("Simulation not built yet — run the CHP loop")


def _run(seed=42, years=50):
    _skip()
    config = Config(seed=seed, years=years, population_size=200)
    sim = Simulation(config)
    for yr in range(1, years + 1):
        sim.tick()
    return sim


class TestMilestone1AgentModel:
    def test_35_heritable_traits(self):
        _skip()
        from models.agent import HERITABLE_TRAITS
        assert len(HERITABLE_TRAITS) == 35

    def test_life_stages(self):
        _skip()
        sim = _run(years=5)
        stages = set(a.life_stage for a in sim.society.get_living())
        assert "PRIME" in stages or "MATURE" in stages


class TestMilestone13Integration:
    def test_50yr_no_crash(self):
        _skip()
        sim = _run(seed=42, years=50)
        assert sim.society.population_size() > 0

    def test_deterministic(self):
        _skip()
        s1 = _run(seed=42, years=20)
        s2 = _run(seed=42, years=20)
        assert s1.society.population_size() == s2.society.population_size()

    def test_population_stable(self):
        _skip()
        sim = _run(seed=42, years=100)
        assert sim.society.population_size() > 50, "Population collapsed"


class TestMilestone15Validation:
    @pytest.mark.slow
    def test_10_seeds_no_collapse(self):
        _skip()
        for seed in SEEDS:
            sim = _run(seed=seed, years=200)
            assert sim.society.population_size() > 0, f"Seed {seed} collapsed"

    @pytest.mark.slow
    def test_cooperation_selected_for(self):
        """Cooperation should be positively selected across seeds."""
        _skip()
        # Check that mean cooperation doesn't decline over 200yr
        coop_start = []
        coop_end = []
        for seed in SEEDS[:5]:
            config = Config(seed=seed, years=200, population_size=200)
            sim = Simulation(config)
            start_coop = np.mean([a.cooperation_propensity for a in sim.society.get_living()])
            for _ in range(200):
                sim.tick()
            end_coop = np.mean([a.cooperation_propensity for a in sim.society.get_living()])
            coop_start.append(start_coop)
            coop_end.append(end_coop)
        # Cooperation should not decline significantly
        assert np.mean(coop_end) >= np.mean(coop_start) - 0.05

    @pytest.mark.slow
    def test_aggression_selected_against(self):
        _skip()
        agg_vals = []
        for seed in SEEDS[:5]:
            sim = _run(seed=seed, years=200)
            agg = np.mean([a.aggression_propensity for a in sim.society.get_living()])
            agg_vals.append(agg)
        assert np.mean(agg_vals) < 0.55, "Aggression should be selected against"


class TestCoefficientDrift:
    def test_h2_values_used(self):
        """Inheritance must use h² weighting, not simple averaging."""
        _skip()
        import inspect
        from engines.reproduction import ReproductionEngine
        source = inspect.getsource(ReproductionEngine)
        assert "h2" in source.lower() or "heritability" in source.lower(), (
            "No h² reference in reproduction engine — possible simple averaging"
        )

    def test_35_traits_exact(self):
        _skip()
        from models.agent import HERITABLE_TRAITS
        assert len(HERITABLE_TRAITS) == 35, f"Got {len(HERITABLE_TRAITS)} traits, need 35"
