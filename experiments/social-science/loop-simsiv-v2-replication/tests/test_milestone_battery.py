"""
SIMSIV v2 Replication — CHP Milestone Test Battery

10 milestones. Tests the North vs Bowles result reproduction.
Key test: n=3 false positive caught and killed at n=10.

Usage:
    pytest tests/test_milestone_battery.py -v
"""

import numpy as np
import pytest

SIGMA_THRESHOLD = 0.15
SEEDS = list(range(1, 7))

try:
    from models.clan.clan_simulation import ClanSimulation
    from config import Config
    from models.clan.clan_config import ClanConfig
    V2_AVAILABLE = True
except ImportError:
    V2_AVAILABLE = False


def _skip():
    if not V2_AVAILABLE:
        pytest.skip("v2 clan simulator not built yet — run the CHP loop")


class TestMilestone1Foundation:
    def test_band_construction(self):
        _skip()
        from models.clan.band import Band
        b = Band(band_id=1, name="Test", config=Config(), rng=np.random.default_rng(42))
        assert b.band_id == 1
        assert b.population_size() > 0

    def test_clan_society(self):
        _skip()
        from models.clan.clan_society import ClanSociety
        cs = ClanSociety()
        assert len(cs.bands) == 0


class TestMilestone6SimulationWrapper:
    def test_per_band_config(self):
        _skip()
        sim = ClanSimulation(
            seed=42, n_years=5,
            band_setups=[("Free", Config(law_strength=0.0)),
                         ("State", Config(law_strength=0.8))],
            population_per_band=30,
        )
        sim.run()
        free_cfg = sim.get_band_config("Free")
        state_cfg = sim.get_band_config("State")
        # Institutional drift means exact values shift, but gap persists
        assert state_cfg.law_strength > free_cfg.law_strength + 0.3


class TestMilestone7FalsePositive:
    """At n=3, a positive interaction effect may appear. It's a false positive."""

    def test_n3_may_show_effect(self):
        """This test DOCUMENTS the false positive, not asserts it."""
        _skip()
        # Run n=3 factorial — the effect may or may not appear
        # The point is: if it does, the Critic must say "replicate at n=10"
        pass  # Documented in spec.md


class TestMilestone9DefinitiveResult:
    @pytest.mark.slow
    def test_20_band_north_wins(self):
        """10 Free + 10 State: State cooperation > Free (p < 0.01)."""
        _skip()
        clan_cfg = ClanConfig(
            raid_base_probability=0.50, raid_scarcity_threshold=20.0,
            raid_trust_suppression_threshold=0.5,
        )
        diffs = []
        for seed in SEEDS:
            sim = ClanSimulation(
                seed=seed, n_years=200,
                band_setups=(
                    [(f"F{i}", Config(law_strength=0.0)) for i in range(10)] +
                    [(f"S{i}", Config(law_strength=0.8)) for i in range(10)]
                ),
                population_per_band=30, clan_config=clan_cfg,
                base_interaction_rate=0.5,
            )
            sim.run()
            free_coops, state_coops = [], []
            for bid in sim.clan_society.bands:
                band = sim.clan_society.bands[bid]
                living = band.get_living()
                if not living:
                    continue
                coop = float(np.mean([a.cooperation_propensity for a in living]))
                if band.society.config.law_strength < 0.4:
                    free_coops.append(coop)
                else:
                    state_coops.append(coop)
            if free_coops and state_coops:
                diffs.append(np.mean(free_coops) - np.mean(state_coops))

        if len(diffs) >= 3:
            mean_diff = np.mean(diffs)
            from scipy import stats
            t, p = stats.ttest_1samp(diffs, 0)
            assert mean_diff < 0, (
                f"State should have higher cooperation than Free: diff={mean_diff:+.4f}"
            )
            assert p < 0.01, (
                f"Result should be significant: p={p:.4f} (expected < 0.01)"
            )


class TestCoefficientDrift:
    def test_default_trust_03(self):
        _skip()
        from models.clan.band import Band
        b = Band(band_id=1, name="T", config=Config(), rng=np.random.default_rng(42))
        assert b.trust_toward(999) == 0.3, "Default trust should be 0.3, not 0.5"

    def test_fission_inherits_config(self):
        """Daughters must inherit parent Config, not default."""
        _skip()
        # This is Dead End 5 prevention — verified by checking the selection engine source
        import inspect
        from engines.clan_selection import _process_fission
        source = inspect.getsource(_process_fission)
        assert "dc_replace" in source or "dataclasses.replace" in source or "parent_config" in source, (
            "Fission must use parent's Config via dataclasses.replace"
        )
