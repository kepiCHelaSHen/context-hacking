"""
Gate Checker — Layer 6: sigma-gated statistical verification.

Nothing merges on vibes. Every build runs multi-seed anomaly checks.

Anomaly checks (configurable per project):
  - Each check: metric, operator, threshold
  - All seeds must pass ALL checks
  - Variance check: std across seeds < sigma_threshold

Bound check: all N seeds must pass every threshold.
Variance check: std across seeds < 0.15 (configurable).
Trend check: no metric monotonically worsening across 3 consecutive turns.

2+ seeds fail → ANOMALY
K consecutive ANOMALY → EXIT 3
"""

from __future__ import annotations

import logging
import operator as op
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from context_hacking.core.orchestrator import Config

_log = logging.getLogger(__name__)

_OPERATORS = {
    ">": op.gt,
    ">=": op.ge,
    "<": op.lt,
    "<=": op.le,
    "==": op.eq,
}


@dataclass
class AnomalyCheck:
    """A single threshold check applied to every seed."""

    metric: str
    operator: str
    threshold: float
    description: str = ""

    def evaluate(self, value: float) -> bool:
        fn = _OPERATORS.get(self.operator)
        if fn is None:
            _log.error("Unknown operator: %s", self.operator)
            return False
        return bool(fn(value, self.threshold))


@dataclass
class GateResult:
    """Result of a full gate check across multiple seeds."""

    passed: bool
    bound_failures: list[str] = field(default_factory=list)
    variance_failures: list[str] = field(default_factory=list)
    seed_results: dict[int, dict[str, bool]] = field(default_factory=dict)


class GateChecker:
    """Manages sigma-gated statistical verification."""

    def __init__(self, config: "Config") -> None:
        gate_cfg = config.gate_config
        self.n_seeds: int = gate_cfg.get("seeds", 3)
        self.convergence_seeds: int = gate_cfg.get("convergence_seeds", 30)
        self.sigma_threshold: float = gate_cfg.get("sigma_threshold", 0.15)
        self.max_consecutive_anomalies: int = gate_cfg.get(
            "max_consecutive_anomalies", 3
        )

        # Parse anomaly checks from config
        self.checks: list[AnomalyCheck] = []
        for check_def in gate_cfg.get("anomaly_checks", []):
            self.checks.append(
                AnomalyCheck(
                    metric=check_def["metric"],
                    operator=check_def["operator"],
                    threshold=check_def["threshold"],
                    description=check_def.get("description", ""),
                )
            )

        self._consecutive_anomalies: int = 0
        self._last_result: GateResult | None = None
        self._metric_history: list[dict[str, float]] = []

    @property
    def consecutive_anomalies(self) -> int:
        return self._consecutive_anomalies

    @property
    def last_result(self) -> str:
        if self._last_result is None:
            return "NO_DATA"
        return "PASS" if self._last_result.passed else "FAIL"

    def evaluate(self, seed_metrics: dict[int, dict[str, float]]) -> GateResult:
        """Run all anomaly checks across all seeds.

        Parameters
        ----------
        seed_metrics:
            {seed: {metric_name: value}} for each seed run.

        Returns
        -------
        GateResult with pass/fail and details.
        """
        result = GateResult(passed=True)

        # ── Bound check: every seed must pass every check ──
        for seed, metrics in seed_metrics.items():
            result.seed_results[seed] = {}
            for check in self.checks:
                value = metrics.get(check.metric)
                if value is None:
                    _log.warning(
                        "Metric '%s' missing for seed %d", check.metric, seed
                    )
                    result.seed_results[seed][check.metric] = False
                    result.bound_failures.append(
                        f"Seed {seed}: {check.metric} missing"
                    )
                    result.passed = False
                    continue

                passed = check.evaluate(value)
                result.seed_results[seed][check.metric] = passed
                if not passed:
                    result.bound_failures.append(
                        f"Seed {seed}: {check.metric}={value:.4f} "
                        f"failed {check.operator} {check.threshold}"
                    )
                    result.passed = False

        # ── Variance check: std across seeds for each metric ──
        if len(seed_metrics) >= 2:
            all_metrics = set()
            for m in seed_metrics.values():
                all_metrics.update(m.keys())

            for metric_name in all_metrics:
                values = [
                    m[metric_name]
                    for m in seed_metrics.values()
                    if metric_name in m
                ]
                if len(values) >= 2:
                    std = float(np.std(values))
                    if std > self.sigma_threshold:
                        result.variance_failures.append(
                            f"{metric_name}: std={std:.4f} > {self.sigma_threshold}"
                        )
                        # Variance failure is a WARNING (STOCHASTIC_INSTABILITY)
                        # but does not fail the gate — it forces a Validation turn.
                        _log.warning(
                            "STOCHASTIC_INSTABILITY: %s std=%.4f > %.4f",
                            metric_name, std, self.sigma_threshold,
                        )

        self._last_result = result

        # ── Log ──
        if result.passed:
            _log.info("Gate check PASSED (%d seeds)", len(seed_metrics))
        else:
            _log.warning(
                "Gate check FAILED: %d bound failures",
                len(result.bound_failures),
            )
            for f in result.bound_failures:
                _log.warning("  %s", f)

        return result

    def record_anomaly(self) -> None:
        """Record an anomaly (gate failed)."""
        self._consecutive_anomalies += 1
        _log.warning(
            "Anomaly recorded (%d consecutive)", self._consecutive_anomalies
        )

    def record_pass(self) -> None:
        """Record a passing gate (resets anomaly counter)."""
        self._consecutive_anomalies = 0

    def record_metrics(self, metrics: dict[str, float]) -> None:
        """Record metrics for trend detection."""
        self._metric_history.append(metrics)

    def check_trend_degradation(self) -> list[str]:
        """Check for monotonically worsening metrics across last 3 turns.

        Returns list of metric names showing degradation.
        """
        if len(self._metric_history) < 3:
            return []

        last_3 = self._metric_history[-3:]
        degrading = []

        for metric in last_3[0]:
            values = [m.get(metric) for m in last_3 if metric in m]
            if len(values) < 3:
                continue
            # Check if monotonically worsening (assuming higher = better)
            if values[0] > values[1] > values[2]:
                degrading.append(metric)

        if degrading:
            _log.warning("TREND_DEGRADATION detected: %s", degrading)

        return degrading
