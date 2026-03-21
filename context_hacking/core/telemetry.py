"""
CHP Telemetry — Protocol Health Metrics

Tracks per-turn performance stats that show the loop learning over time:
  - Token consumption per turn
  - Drift rate (coefficients matching frozen spec)
  - Critic gate score trends
  - Dead ends hit vs avoided
  - Time per turn
  - Test pass rate (first try vs after fix)
  - Build efficiency (lines of code per turn)
  - Self-correction events (false positives caught)

All data stored in .chp/telemetry.json (gitignored).
Dashboard reads this for the Protocol Health panel.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

_log = logging.getLogger(__name__)

TELEMETRY_PATH = Path(".chp") / "telemetry.json"


@dataclass
class TurnMetrics:
    """Metrics captured for a single turn."""

    turn: int = 0
    timestamp: str = ""
    mode: str = "VALIDATION"

    # Token efficiency
    tokens_input: int = 0
    tokens_output: int = 0
    tokens_total: int = 0

    # Time
    duration_seconds: float = 0.0

    # Drift detection
    coefficients_checked: int = 0
    coefficients_matched: int = 0
    drift_rate: float = 0.0  # 1 - (matched / checked)

    # Critic gates
    gate_1_frozen: float = 0.0
    gate_2_architecture: float = 0.0
    gate_3_scientific: float = 0.0
    gate_4_drift: float = 0.0
    critic_verdict: str = ""  # PASS or NEEDS_IMPROVEMENT

    # Tests
    tests_passed: int = 0
    tests_failed: int = 0
    tests_skipped: int = 0
    tests_passed_first_try: bool = False  # passed without fix cycle

    # Dead ends
    dead_ends_checked: int = 0
    dead_ends_avoided: int = 0  # known dead ends that were NOT repeated
    new_dead_ends_logged: int = 0

    # Build output
    files_written: int = 0
    lines_written: int = 0

    # Self-correction
    false_positive_caught: bool = False
    false_positive_description: str = ""
    blocking_issues_found: int = 0
    blocking_issues_fixed: int = 0

    # Anomaly check
    seeds_run: int = 0
    seeds_passed: int = 0
    anomaly: bool = False
    stochastic_instability: bool = False


@dataclass
class TelemetryStore:
    """Persistent store of all turn metrics."""

    turns: list[TurnMetrics] = field(default_factory=list)
    project_name: str = ""
    start_time: str = ""

    def add_turn(self, metrics: TurnMetrics) -> None:
        self.turns.append(metrics)
        self.save()
        _log.info("Telemetry: Turn %d recorded (%d total)", metrics.turn, len(self.turns))

    def save(self) -> None:
        TELEMETRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "project_name": self.project_name,
            "start_time": self.start_time,
            "turns": [asdict(t) for t in self.turns],
        }
        TELEMETRY_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @classmethod
    def load(cls) -> TelemetryStore:
        if not TELEMETRY_PATH.exists():
            return cls()
        try:
            data = json.loads(TELEMETRY_PATH.read_text(encoding="utf-8"))
            store = cls(
                project_name=data.get("project_name", ""),
                start_time=data.get("start_time", ""),
            )
            for t in data.get("turns", []):
                store.turns.append(TurnMetrics(**{
                    k: v for k, v in t.items() if k in TurnMetrics.__dataclass_fields__
                }))
            return store
        except Exception as e:
            _log.warning("Failed to load telemetry: %s", e)
            return cls()

    # ── Aggregate stats ──────────────────────────────────────────────────

    @property
    def total_turns(self) -> int:
        return len(self.turns)

    @property
    def total_tokens(self) -> int:
        return sum(t.tokens_total for t in self.turns)

    @property
    def total_lines_written(self) -> int:
        return sum(t.lines_written for t in self.turns)

    @property
    def total_duration_minutes(self) -> float:
        return sum(t.duration_seconds for t in self.turns) / 60

    @property
    def mean_drift_rate(self) -> float:
        rates = [t.drift_rate for t in self.turns if t.coefficients_checked > 0]
        return sum(rates) / len(rates) if rates else 0.0

    @property
    def false_positives_caught(self) -> int:
        return sum(1 for t in self.turns if t.false_positive_caught)

    @property
    def total_dead_ends_avoided(self) -> int:
        return sum(t.dead_ends_avoided for t in self.turns)

    @property
    def first_try_pass_rate(self) -> float:
        tested = [t for t in self.turns if t.tests_passed + t.tests_failed > 0]
        if not tested:
            return 0.0
        return sum(1 for t in tested if t.tests_passed_first_try) / len(tested)

    @property
    def mean_gate_scores(self) -> dict[str, float]:
        scores: dict[str, list[float]] = {
            "Gate 1": [], "Gate 2": [], "Gate 3": [], "Gate 4": [],
        }
        for t in self.turns:
            if t.gate_1_frozen > 0:
                scores["Gate 1"].append(t.gate_1_frozen)
                scores["Gate 2"].append(t.gate_2_architecture)
                scores["Gate 3"].append(t.gate_3_scientific)
                scores["Gate 4"].append(t.gate_4_drift)
        return {
            k: sum(v) / len(v) if v else 0.0 for k, v in scores.items()
        }

    @property
    def tokens_per_line(self) -> float:
        if self.total_lines_written == 0:
            return 0.0
        return self.total_tokens / self.total_lines_written

    @property
    def anomaly_rate(self) -> float:
        if not self.turns:
            return 0.0
        return sum(1 for t in self.turns if t.anomaly) / len(self.turns)

    def trend(self, metric: str, window: int = 5) -> list[float]:
        """Get the last N values of a metric for trend plotting."""
        values = []
        for t in self.turns[-window:]:
            val = getattr(t, metric, None)
            if val is not None and isinstance(val, (int, float)):
                values.append(float(val))
        return values

    def summary(self) -> dict[str, Any]:
        """Return a summary dict for dashboard display."""
        return {
            "total_turns": self.total_turns,
            "total_tokens": self.total_tokens,
            "total_lines": self.total_lines_written,
            "tokens_per_line": round(self.tokens_per_line, 1),
            "duration_minutes": round(self.total_duration_minutes, 1),
            "mean_drift_rate": round(self.mean_drift_rate, 4),
            "false_positives_caught": self.false_positives_caught,
            "dead_ends_avoided": self.total_dead_ends_avoided,
            "first_try_pass_rate": round(self.first_try_pass_rate, 2),
            "anomaly_rate": round(self.anomaly_rate, 2),
            "mean_gates": self.mean_gate_scores,
        }


# ── Timer context manager ────────────────────────────────────────────────────

class TurnTimer:
    """Context manager that times a turn and records duration."""

    def __init__(self, metrics: TurnMetrics) -> None:
        self.metrics = metrics
        self._start: float = 0.0

    def __enter__(self) -> TurnTimer:
        self._start = time.time()
        return self

    def __exit__(self, *args: Any) -> None:
        self.metrics.duration_seconds = time.time() - self._start
