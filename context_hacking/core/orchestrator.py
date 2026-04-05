"""
Orchestrator — the main CHP loop with mode switching.

Implements the full turn cycle:
  STEP 1:  Check exit conditions (5 kill-switches)
  STEP 2:  Subagent health checks
  STEP 3:  Choose mode (Validation / Exploration)
  STEP 4:  Dead end check (read dead_ends.md, avoid repeats)
  STEP 5:  Determine what to build (from innovation log + state vector)
  STEP 6:  Council review (Validation: before build; Exploration: after)
  STEP 7:  Grounding (Validation: citation; Exploration: hypothesis)
  STEP 8:  BUILD via Builder subagent
  STEP 9:  Self-critique
  STEP 10: Critic review (hard blocker in Validation, advisory in Exploration)
  STEP 11: Code Reviewer (every new file)
  STEP 12: Council (post-build in Exploration)
  STEP 13: Multi-seed anomaly detection
  STEP 14: Metric improvement tracking
  STEP 15: Commit and log
  STEP 16: Session memory update
  LOOP back to STEP 1.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from context_hacking.core.gates import GateChecker
from context_hacking.core.memory import MemoryManager
from context_hacking.core.modes import ModeManager
from context_hacking.core.telemetry import TelemetryStore

_log = logging.getLogger(__name__)


@dataclass
class Config:
    """CHP configuration loaded from config.yaml."""

    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: str | Path) -> Config:
        with open(path) as f:
            raw = yaml.safe_load(f)
        return cls(raw=raw)

    @property
    def project_name(self) -> str:
        return self.raw.get("project", {}).get("name", "unnamed")

    @property
    def max_turns(self) -> int:
        return self.raw.get("loop", {}).get("max_turns", 50)

    @property
    def stagnation_threshold(self) -> int:
        return self.raw.get("loop", {}).get("stagnation_threshold", 5)

    @property
    def max_consecutive_exploration(self) -> int:
        return self.raw.get("loop", {}).get("max_consecutive_exploration", 3)

    @property
    def state_vector_interval(self) -> int:
        return self.raw.get("loop", {}).get("state_vector_interval", 5)

    @property
    def context_reset_interval(self) -> int:
        return self.raw.get("loop", {}).get("context_reset_interval", 15)

    @property
    def auto_tag(self) -> bool:
        return self.raw.get("loop", {}).get("auto_tag", True)

    @property
    def frozen_paths(self) -> list[str]:
        return self.raw.get("frozen", {}).get("paths", ["frozen/"])

    @property
    def exit_conditions(self) -> dict[str, bool]:
        return self.raw.get("exit_conditions", {})

    @property
    def gate_config(self) -> dict[str, Any]:
        return self.raw.get("gates", {})

    @property
    def critic_config(self) -> dict[str, Any]:
        return self.raw.get("critic", {})

    @property
    def model_config(self) -> dict[str, Any]:
        return self.raw.get("models", {})


class Orchestrator:
    """The main CHP loop — build, critique, fix, verify, commit, repeat."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.turn: int = 0
        self.gates = GateChecker(config)
        self.modes = ModeManager(config)
        self.memory = MemoryManager(config)
        self.telemetry = TelemetryStore.load()
        self._exit_reason: str | None = None

        _log.info("CHP Orchestrator initialized: %s", config.project_name)

    @property
    def current_mode(self) -> str:
        return self.modes.current_mode

    @property
    def dead_ends(self) -> list[str]:
        return self.memory.dead_ends

    def status(self) -> dict[str, Any]:
        """Return current loop status as a dict."""
        return {
            "project": self.config.project_name,
            "turn": self.turn,
            "max_turns": self.config.max_turns,
            "mode": self.current_mode,
            "stagnation_streak": self.modes.stagnation_streak,
            "dead_ends": len(self.memory.dead_ends),
            "exit_reason": self._exit_reason,
            "last_gate_result": self.gates.last_result,
        }

    def check_exit_conditions(self) -> str | None:
        """Check all 5 kill-switches. Returns exit reason or None."""
        ec = self.config.exit_conditions

        # EXIT 5: Human stop (check first — highest priority)
        if ec.get("human_stop", True):
            stop_file = Path("STOP")
            if stop_file.exists():
                return "EXIT 5: Human STOP file detected"

        # EXIT 2: Performance gate
        if ec.get("performance_gate", True):
            total_stag = self.modes.stagnation_streak
            if total_stag >= self.config.stagnation_threshold:
                if self.modes.exploration_streak >= self.config.max_consecutive_exploration:
                    return (
                        f"EXIT 2: No improvement for {total_stag} turns "
                        f"and {self.modes.exploration_streak} Exploration turns exhausted"
                    )

        # EXIT 3: Unresolvable anomaly
        if ec.get("unresolvable_anomaly", True):
            if self.gates.consecutive_anomalies >= self.config.gate_config.get(
                "max_consecutive_anomalies", 3
            ):
                return (
                    f"EXIT 3: {self.gates.consecutive_anomalies} consecutive anomalies"
                )

        # EXIT 1 and EXIT 4 are checked by the critic / findings doc
        # and set externally via self.set_exit()

        # Turn limit
        if self.turn >= self.config.max_turns:
            return f"Turn limit reached ({self.config.max_turns})"

        return None

    def set_exit(self, reason: str) -> None:
        """Set an exit reason externally (for EXIT 1 / EXIT 4)."""
        self._exit_reason = reason

    def step(self) -> dict[str, Any]:
        """Execute one turn of the loop. Returns turn result dict."""
        self.turn += 1
        _log.info("=" * 60)
        _log.info("TURN %d — MODE: %s", self.turn, self.current_mode)
        _log.info("=" * 60)

        # STEP 1: Check exit conditions
        exit_reason = self.check_exit_conditions()
        if exit_reason:
            self._exit_reason = exit_reason
            _log.warning("EXIT: %s", exit_reason)
            return {"turn": self.turn, "exit": exit_reason}

        # STEP 4: Dead end check
        dead_ends = self.memory.load_dead_ends()
        _log.info("Dead ends avoided: %s", dead_ends if dead_ends else "NONE")

        # STEP 5: Read last innovation log entry for context
        last_entry = self.memory.last_innovation_entry()
        _log.info("Last turn focus: %s", last_entry)

        # Steps 2-3, 6-16 are delegated to the agent framework
        # (Claude Code, Cursor, or custom agent runner).
        # The orchestrator manages STATE — agents manage EXECUTION.

        result = {
            "turn": self.turn,
            "mode": self.current_mode,
            "dead_ends_avoided": dead_ends,
            "last_entry": last_entry,
            "status": "awaiting_build",
        }

        return result

    def record_turn_result(
        self,
        gate_passed: bool,
        metrics_improved: bool,
        anomaly: bool,
        metrics: "TurnMetrics | None" = None,
    ) -> None:
        """Record the outcome of a turn after build + review + verification."""
        # Update gate tracker
        if anomaly:
            self.gates.record_anomaly()
        else:
            self.gates.record_pass()

        # Update mode manager
        self.modes.record_turn(
            metrics_improved=metrics_improved,
            anomaly=anomaly,
        )

        # State vector
        if self.turn % self.config.state_vector_interval == 0:
            self.memory.write_state_vector(self.turn, self.current_mode)

        # Telemetry
        if metrics is not None:
            self.telemetry.add_turn(metrics)

        # Auto git tag
        if self.config.auto_tag and gate_passed and not anomaly:
            self._git_tag(f"chp-turn-{self.turn}-pass")

        _log.info(
            "Turn %d recorded: gate=%s, improved=%s, anomaly=%s, mode=%s",
            self.turn, gate_passed, metrics_improved, anomaly, self.current_mode,
        )

    def run(self) -> None:
        """Run the loop until an exit condition is met."""
        while self._exit_reason is None:
            result = self.step()
            if "exit" in result:
                break
            # In automated mode, the build/review/verify cycle would run here.
            # In interactive mode (Claude Code / Cursor), step() returns and
            # the human + agent complete the turn, then call record_turn_result().
            _log.info(
                "Turn %d step complete. Call record_turn_result() after build.",
                self.turn,
            )
            break  # In non-automated mode, break after each step

    def _git_tag(self, tag_name: str) -> None:
        """Create a git tag on the current HEAD."""
        try:
            import git
            repo = git.Repo(".")
            repo.create_tag(tag_name)
            _log.info("Git tag created: %s", tag_name)
        except Exception as e:
            _log.warning("Git tag failed: %s", e)
