"""Integration tests — multi-turn orchestrator loop."""
import pytest
import yaml
from pathlib import Path

from context_hacking.core.orchestrator import Orchestrator, Config
from context_hacking.core.telemetry import TurnMetrics, TELEMETRY_PATH


@pytest.fixture
def orch(tmp_path):
    """Create a fully-wired orchestrator in a temp directory."""
    config_data = {
        "project": {"name": "integration-test"},
        "loop": {
            "max_turns": 20,
            "stagnation_threshold": 3,
            "max_consecutive_exploration": 2,
            "state_vector_interval": 2,
            "auto_tag": False,
        },
        "gates": {
            "seeds": 3,
            "sigma_threshold": 0.15,
            "max_consecutive_anomalies": 3,
            "anomaly_checks": [],
        },
        "exit_conditions": {
            "human_stop": False,  # Don't check STOP file
            "performance_gate": True,
            "unresolvable_anomaly": True,
        },
    }
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.dump(config_data))
    (tmp_path / "state_vector.md").touch()
    (tmp_path / "innovation_log.md").touch()
    (tmp_path / "dead_ends.md").touch()

    # Clean telemetry state
    TELEMETRY_PATH.unlink(missing_ok=True)

    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    config = Config.from_yaml(config_path)
    o = Orchestrator(config)
    yield o
    os.chdir(old_cwd)


class TestMultiTurnLoop:
    def test_five_turns_with_improvement(self, orch):
        """5 turns with steady improvement stays in VALIDATION."""
        for i in range(5):
            result = orch.step()
            assert result["status"] == "awaiting_build"
            assert result["mode"] == "VALIDATION"
            metrics = TurnMetrics(turn=orch.turn, tokens_total=1000, duration_seconds=5.0)
            orch.record_turn_result(gate_passed=True, metrics_improved=True,
                                   anomaly=False, metrics=metrics)
        assert orch.turn == 5
        assert orch.telemetry.total_turns == 5
        assert orch.modes.current_mode == "VALIDATION"

    def test_stagnation_triggers_exploration(self, orch):
        """3 turns without improvement triggers EXPLORATION mode."""
        for i in range(3):
            orch.step()
            orch.record_turn_result(gate_passed=True, metrics_improved=False, anomaly=False)
        assert orch.modes.current_mode == "EXPLORATION"

    def test_exploration_anomaly_reverts_to_validation(self, orch):
        """Anomaly in EXPLORATION triggers reversion to VALIDATION."""
        # Stagnate into EXPLORATION
        for i in range(3):
            orch.step()
            orch.record_turn_result(gate_passed=True, metrics_improved=False, anomaly=False)
        assert orch.modes.current_mode == "EXPLORATION"

        # Anomaly in EXPLORATION
        orch.step()
        orch.record_turn_result(gate_passed=False, metrics_improved=False, anomaly=True)
        assert orch.modes.current_mode == "VALIDATION"

    def test_max_turns_exit(self, orch):
        """Orchestrator exits when max turns reached."""
        orch.turn = 20  # Set to max
        result = orch.step()
        assert "exit" in result
        assert "Turn limit" in result["exit"]

    def test_consecutive_anomaly_exit(self, orch):
        """3 consecutive anomalies triggers EXIT 3."""
        for i in range(3):
            orch.step()
            orch.record_turn_result(gate_passed=False, metrics_improved=False, anomaly=True)
        result = orch.step()
        assert "exit" in result
        assert "anomal" in result["exit"].lower()

    def test_council_blocks_then_clears(self, orch):
        """Council blocks in VALIDATION, clears on next clean signal."""
        orch.step()
        action = orch.record_council_result(
            consensus_issues=["drift detected by openai, xai"],
            drift_flagged=True,
        )
        assert action["blocked"] is True
        assert orch._consecutive_council_drift == 1

        # Clean signal clears drift
        action2 = orch.record_council_result(
            consensus_issues=[],
            drift_flagged=False,
        )
        assert action2["blocked"] is False
        assert orch._consecutive_council_drift == 0

    def test_status_includes_all_fields(self, orch):
        """Status dict has all expected fields after a turn."""
        orch.step()
        metrics = TurnMetrics(turn=1, tokens_total=500, duration_seconds=3.0)
        orch.record_turn_result(gate_passed=True, metrics_improved=True,
                               anomaly=False, metrics=metrics)
        status = orch.status()
        assert "project" in status
        assert "turn" in status
        assert "mode" in status
        assert "stagnation_streak" in status
        assert "council_drift_streak" in status
