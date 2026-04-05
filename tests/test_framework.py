"""
CHP Framework Tests — tests for the framework itself, not the experiments.

These verify that the orchestrator, gates, modes, memory, and CLI work correctly.
"""

import tempfile
from pathlib import Path

import numpy as np
import pytest
import yaml


# ── Config ───────────────────────────────────────────────────────────────────

class TestConfig:
    def test_load_from_yaml(self, tmp_path):
        from context_hacking.core.orchestrator import Config
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump({
            "project": {"name": "test-project"},
            "loop": {"max_turns": 10, "stagnation_threshold": 3},
            "gates": {"seeds": 3, "sigma_threshold": 0.15, "anomaly_checks": []},
        }))
        config = Config.from_yaml(cfg_file)
        assert config.project_name == "test-project"
        assert config.max_turns == 10
        assert config.stagnation_threshold == 3


class TestConfigValidation:
    def test_unknown_key_logged(self, tmp_path):
        """Misspelled config key gets logged as warning."""
        from context_hacking.core.orchestrator import Config
        config_path = tmp_path / "config.yaml"
        config_path.write_text(yaml.dump({
            "project": {"name": "test"},
            "looop": {"max_turns": 10},
        }))
        # 'looop' is not a valid key, so max_turns falls back to default
        config = Config.from_yaml(config_path)
        assert config.max_turns == 50  # Falls back to default since 'looop' not recognized

    def test_valid_config_loads(self, tmp_path):
        """Valid config loads without issues."""
        from context_hacking.core.orchestrator import Config
        config_path = tmp_path / "config.yaml"
        config_path.write_text(yaml.dump({
            "project": {"name": "test"},
            "loop": {"max_turns": 10},
            "gates": {"seeds": 3},
        }))
        config = Config.from_yaml(config_path)
        assert config.max_turns == 10


# ── Modes ────────────────────────────────────────────────────────────────────

class TestModeManager:
    def _make_config(self):
        from context_hacking.core.orchestrator import Config
        return Config(raw={
            "loop": {"stagnation_threshold": 3, "max_consecutive_exploration": 2},
        })

    def test_starts_in_validation(self):
        from context_hacking.core.modes import ModeManager
        mm = ModeManager(self._make_config())
        assert mm.current_mode == "VALIDATION"

    def test_switches_to_exploration_on_stagnation(self):
        from context_hacking.core.modes import ModeManager
        mm = ModeManager(self._make_config())
        for _ in range(3):
            mm.record_turn(metrics_improved=False, anomaly=False)
        assert mm.current_mode == "EXPLORATION"

    def test_returns_to_validation_on_anomaly(self):
        from context_hacking.core.modes import ModeManager
        mm = ModeManager(self._make_config())
        mm.force_mode("EXPLORATION")
        mm.record_turn(metrics_improved=False, anomaly=True)
        assert mm.current_mode == "VALIDATION"

    def test_returns_after_max_exploration(self):
        from context_hacking.core.modes import ModeManager
        mm = ModeManager(self._make_config())
        mm.force_mode("EXPLORATION")
        mm.record_turn(metrics_improved=True, anomaly=False)
        mm.record_turn(metrics_improved=True, anomaly=False)
        assert mm.current_mode == "VALIDATION"

    def test_critic_blocks_in_validation(self):
        from context_hacking.core.modes import ModeManager
        mm = ModeManager(self._make_config())
        assert mm.critic_is_blocker is True

    def test_critic_advisory_in_exploration(self):
        from context_hacking.core.modes import ModeManager
        mm = ModeManager(self._make_config())
        mm.force_mode("EXPLORATION")
        assert mm.critic_is_blocker is False

    def test_reversion_only_in_exploration(self):
        from context_hacking.core.modes import ModeManager
        mm = ModeManager(self._make_config())
        assert mm.reversion_active is False
        mm.force_mode("EXPLORATION")
        assert mm.reversion_active is True

    def test_stagnation_resets_on_improvement(self):
        from context_hacking.core.modes import ModeManager
        mm = ModeManager(self._make_config())
        mm.record_turn(metrics_improved=False, anomaly=False)
        mm.record_turn(metrics_improved=False, anomaly=False)
        assert mm.stagnation_streak == 2
        mm.record_turn(metrics_improved=True, anomaly=False)
        assert mm.stagnation_streak == 0


# ── Gates ────────────────────────────────────────────────────────────────────

class TestGateChecker:
    def _make_config(self):
        from context_hacking.core.orchestrator import Config
        return Config(raw={
            "gates": {
                "seeds": 3,
                "sigma_threshold": 0.15,
                "max_consecutive_anomalies": 3,
                "anomaly_checks": [
                    {"metric": "accuracy", "operator": ">", "threshold": 0.80},
                    {"metric": "loss", "operator": "<", "threshold": 0.50},
                ],
            },
        })

    def test_all_pass(self):
        from context_hacking.core.gates import GateChecker
        gc = GateChecker(self._make_config())
        result = gc.evaluate({
            1: {"accuracy": 0.90, "loss": 0.30},
            2: {"accuracy": 0.85, "loss": 0.40},
            3: {"accuracy": 0.88, "loss": 0.35},
        })
        assert result.passed is True
        assert len(result.bound_failures) == 0

    def test_bound_failure(self):
        from context_hacking.core.gates import GateChecker
        gc = GateChecker(self._make_config())
        result = gc.evaluate({
            1: {"accuracy": 0.70, "loss": 0.30},  # accuracy fails
            2: {"accuracy": 0.85, "loss": 0.40},
        })
        assert result.passed is False
        assert len(result.bound_failures) > 0

    def test_variance_warning(self):
        from context_hacking.core.gates import GateChecker
        gc = GateChecker(self._make_config())
        result = gc.evaluate({
            1: {"accuracy": 0.90, "loss": 0.10},
            2: {"accuracy": 0.50, "loss": 0.40},  # huge variance
            3: {"accuracy": 0.85, "loss": 0.35},
        })
        # Variance check is a warning, not a failure
        assert len(result.variance_failures) > 0

    def test_consecutive_anomaly_tracking(self):
        from context_hacking.core.gates import GateChecker
        gc = GateChecker(self._make_config())
        assert gc.consecutive_anomalies == 0
        gc.record_anomaly()
        assert gc.consecutive_anomalies == 1
        gc.record_anomaly()
        assert gc.consecutive_anomalies == 2
        gc.record_pass()
        assert gc.consecutive_anomalies == 0

    def test_trend_degradation_detection(self):
        from context_hacking.core.gates import GateChecker
        gc = GateChecker(self._make_config())
        gc.record_metrics({"accuracy": 0.90})
        gc.record_metrics({"accuracy": 0.85})
        gc.record_metrics({"accuracy": 0.80})
        degrading = gc.check_trend_degradation()
        assert "accuracy" in degrading


# ── Memory ───────────────────────────────────────────────────────────────────

class TestMemoryManager:
    def _make_mm(self, tmp_path):
        from context_hacking.core.orchestrator import Config
        from context_hacking.core.memory import MemoryManager
        config = Config(raw={
            "project": {
                "innovation_log": str(tmp_path / "log.md"),
                "dead_ends": str(tmp_path / "dead.md"),
                "state_vector": str(tmp_path / "sv.md"),
            },
        })
        return MemoryManager(config)

    def test_add_and_read_dead_end(self, tmp_path):
        mm = self._make_mm(tmp_path)
        # Create the file first
        (tmp_path / "dead.md").write_text("# Dead Ends\n")
        mm.add_dead_end("Test failure", "Tried X", "Got Y", "Because Z")
        ends = mm.load_dead_ends()
        assert "Test failure" in ends

    def test_append_innovation_log(self, tmp_path):
        mm = self._make_mm(tmp_path)
        (tmp_path / "log.md").write_text("# Log\n")
        mm.append_innovation_log(1, "VALIDATION", "### What was built\nStuff")
        text = (tmp_path / "log.md").read_text()
        assert "Turn 1" in text

    def test_state_vector_roundtrip(self, tmp_path):
        mm = self._make_mm(tmp_path)
        mm.write_state_vector(5, "EXPLORATION", milestone="3 complete")
        sv = mm.read_state_vector()
        assert sv["TURN"] == "5"
        assert sv["MODE"] == "EXPLORATION"

    def test_state_vector_roundtrip_with_streaks(self, tmp_path):
        """State vector round-trips streak fields for crash recovery."""
        mm = self._make_mm(tmp_path)
        mm.write_state_vector(
            turn=7,
            mode="EXPLORATION",
            stagnation_streak="3",
            exploration_streak="2",
            consecutive_anomalies="0",
        )
        restored = mm.read_state_vector()
        assert restored["TURN"] == "7"
        assert restored["MODE"] == "EXPLORATION"
        assert restored["STAGNATION_STREAK"] == "3"
        assert restored["EXPLORATION_STREAK"] == "2"
        assert restored["CONSECUTIVE_ANOMALIES"] == "0"

    def test_empty_dead_ends(self, tmp_path):
        mm = self._make_mm(tmp_path)
        ends = mm.load_dead_ends()
        assert ends == []


# ── Orchestrator ─────────────────────────────────────────────────────────────

class TestOrchestrator:
    def _make_orch(self, tmp_path):
        from context_hacking.core.orchestrator import Config, Orchestrator
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump({
            "project": {
                "name": "test",
                "innovation_log": str(tmp_path / "log.md"),
                "dead_ends": str(tmp_path / "dead.md"),
                "state_vector": str(tmp_path / "sv.md"),
            },
            "loop": {"max_turns": 5, "stagnation_threshold": 3,
                     "max_consecutive_exploration": 2, "state_vector_interval": 2},
            "gates": {"seeds": 3, "sigma_threshold": 0.15,
                      "max_consecutive_anomalies": 3, "anomaly_checks": []},
            "exit_conditions": {"human_stop": True, "performance_gate": True,
                                "unresolvable_anomaly": True},
        }))
        (tmp_path / "log.md").write_text("# Log\n")
        (tmp_path / "dead.md").write_text("# Dead\n")
        (tmp_path / "sv.md").write_text("TURN: 0\n")

        config = Config.from_yaml(cfg_file)
        return Orchestrator(config)

    def test_initial_state(self, tmp_path):
        orch = self._make_orch(tmp_path)
        assert orch.turn == 0
        assert orch.current_mode == "VALIDATION"

    def test_step_increments_turn(self, tmp_path):
        orch = self._make_orch(tmp_path)
        result = orch.step()
        assert result["turn"] == 1

    def test_exit_on_max_turns(self, tmp_path):
        orch = self._make_orch(tmp_path)
        for _ in range(5):
            orch.step()
        result = orch.step()
        assert "exit" in result

    def test_human_stop(self, tmp_path):
        orch = self._make_orch(tmp_path)
        # Create STOP file
        (Path.cwd() / "STOP").write_text("stop")
        try:
            reason = orch.check_exit_conditions()
            assert reason is not None
            assert "STOP" in reason
        finally:
            (Path.cwd() / "STOP").unlink(missing_ok=True)

    def test_status_dict(self, tmp_path):
        orch = self._make_orch(tmp_path)
        status = orch.status()
        assert "project" in status
        assert "turn" in status
        assert "mode" in status
        assert status["project"] == "test"

    def test_orchestrator_has_telemetry(self, tmp_path):
        """Orchestrator creates a TelemetryStore on init."""
        from context_hacking.core.telemetry import TELEMETRY_PATH
        TELEMETRY_PATH.unlink(missing_ok=True)
        orch = self._make_orch(tmp_path)
        assert hasattr(orch, 'telemetry')
        assert orch.telemetry is not None
        assert orch.telemetry.total_turns == 0

    def test_record_turn_persists_telemetry(self, tmp_path):
        """record_turn_result saves telemetry."""
        from context_hacking.core.telemetry import TELEMETRY_PATH
        TELEMETRY_PATH.unlink(missing_ok=True)
        orch = self._make_orch(tmp_path)
        from context_hacking.core.telemetry import TurnMetrics
        metrics = TurnMetrics(turn=1, tokens_total=500, duration_seconds=10.0)
        orch.record_turn_result(gate_passed=True, metrics_improved=True, anomaly=False, metrics=metrics)
        assert orch.telemetry.total_turns == 1

    def test_step_survives_missing_files(self, tmp_path):
        """Step doesn't crash when memory files are missing."""
        orch = self._make_orch(tmp_path)
        # Delete dead_ends.md to trigger potential I/O issue
        dead_ends_path = tmp_path / "dead.md"
        if dead_ends_path.exists():
            dead_ends_path.unlink()
        # Step should not raise
        result = orch.step()
        assert result is not None
        assert "turn" in result

    def test_emergency_state_dump(self, tmp_path):
        """Emergency dump writes state vector with current turn."""
        orch = self._make_orch(tmp_path)
        orch.turn = 5
        orch.emergency_state_dump()
        state = orch.memory.read_state_vector()
        assert state["TURN"] == "5"
        assert state["MILESTONE"] == "EMERGENCY_DUMP"


# ── Critic Parsing ───────────────────────────────────────────────────────────

class TestCriticParsing:
    def test_parse_pass_verdict(self):
        from context_hacking.agents.critic import parse_verdict
        text = """
        gate_1_frozen: 1.0
        gate_2_arch: 0.95
        gate_3_sci: 0.90
        gate_4_drift: 0.92
        verdict: PASS
        next_turn_priority: do something
        """
        v = parse_verdict(text)
        assert v.passed is True
        assert v.gate_1_frozen == 1.0
        assert v.gate_3_scientific == 0.90

    def test_parse_needs_improvement(self):
        from context_hacking.agents.critic import parse_verdict
        text = "gate_1_frozen: 0.8\nverdic: NEEDS_IMPROVEMENT"
        v = parse_verdict(text)
        assert v.passed is False

    def test_parse_variant_gate_format(self):
        """Handles variant gate score formats."""
        from context_hacking.agents.critic import parse_verdict
        text = """
        Gate 1 (frozen_compliance): 1.0/1.0
        Gate 2 (architecture): 90%
        Gate 3 (scientific_validity): 0.85
        Gate 4 (drift_check): .9
        Verdict: PASS
        """
        v = parse_verdict(text)
        assert v.gate_1_frozen == 1.0
        assert v.gate_2_architecture == 0.9
        assert v.gate_3_scientific == 0.85
        assert v.gate_4_drift == 0.9

    def test_parse_empty_returns_failed(self):
        from context_hacking.agents.critic import parse_verdict
        v = parse_verdict("")
        assert v.verdict == "PARSE_FAILED"
        assert not v.passed

    def test_parse_garbage_returns_failed(self):
        from context_hacking.agents.critic import parse_verdict
        v = parse_verdict("I think the code looks great! No issues found.")
        assert v.verdict == "PARSE_FAILED"

    def test_health_check_validation(self):
        from context_hacking.agents.critic import validate_health_check
        assert validate_health_check("Gate 1 is frozen compliance, must = 1.0. "
                                      "My mission is to find violations of the frozen spec.")
        assert not validate_health_check("I am a helpful assistant.")


# ── Reviewer Parsing ─────────────────────────────────────────────────────────

class TestReviewerParsing:
    def test_parse_issues(self):
        from context_hacking.agents.reviewer import parse_review
        text = """
        CRITICAL: file.py:42 — missing type annotation
        WARNING: file.py:100 — hardcoded value
        MINOR: file.py:200 — inconsistent naming
        APPROVE WITH NOTES
        """
        r = parse_review(text)
        assert r.critical_count == 1
        assert r.warning_count == 1
        assert r.verdict == "APPROVE WITH NOTES"

    def test_parse_empty_returns_failed(self):
        from context_hacking.agents.reviewer import parse_review
        r = parse_review("")
        assert r.verdict == "PARSE_FAILED"
        assert r.needs_revision

    def test_parse_variant_formats(self):
        from context_hacking.agents.reviewer import parse_review
        text = """
        **CRITICAL**: `sim.py:42` — Uses print() instead of logging
        WARNING: model.py line 10 - Missing type annotation
        MINOR - Unused import in config.py
        Verdict: APPROVE WITH NOTES
        """
        r = parse_review(text)
        assert r.critical_count == 1
        assert r.warning_count == 1
        assert len(r.issues) >= 2
        assert r.verdict == "APPROVE WITH NOTES"
