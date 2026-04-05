"""CHP Optimizer — Full 9-layer, 16-step turn loop for Tetris AI.

This is the heart of CHP-TETRIS-AI.  It connects the frozen engine,
features, prior errors, and composition into a complete CHP optimization
loop that is driven by three LLM sub-agents (Builder, Critic, Reviewer)
and guarded by the full CHP gate stack.
"""

from __future__ import annotations

import asyncio
import json
import logging
import math
import os
import statistics
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import yaml

_log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Experiment-local imports (frozen/ and composition)
# ---------------------------------------------------------------------------

from tetris_engine import play_game, GameResult  # noqa: E402
from features import FEATURE_NAMES, FEATURE_FNS  # noqa: E402
from prior_errors import KNOWN_TRAPS  # noqa: E402
from composition import (  # noqa: E402
    parse_weights_from_response,
    validate_weights,
    build_evaluate_fn,
    generate_code_display,
)

# ---------------------------------------------------------------------------
# CHP framework imports
# ---------------------------------------------------------------------------

from context_hacking.core.orchestrator import Config  # noqa: E402
from context_hacking.core.modes import ModeManager, VALIDATION, EXPLORATION  # noqa: E402
from context_hacking.core.memory import MemoryManager  # noqa: E402
from context_hacking.core.telemetry import TelemetryStore, TurnMetrics, TurnTimer  # noqa: E402
from context_hacking.agents.critic import parse_verdict, CriticVerdict  # noqa: E402
from context_hacking.agents.reviewer import parse_review, ReviewResult  # noqa: E402
from context_hacking.agents.council import run_council, CouncilResult  # noqa: E402

# ---------------------------------------------------------------------------
# Feature descriptions for the Builder prompt
# ---------------------------------------------------------------------------

FEATURE_DESCRIPTIONS: dict[str, str] = {
    "aggregate_height": "Sum of all column heights.  Lower is generally better.",
    "complete_lines": "Number of fully filled rows ready to clear.",
    "holes": "Empty cells trapped below filled cells.  Catastrophic — must penalize heavily.",
    "bumpiness": "Sum of absolute height differences between adjacent columns.",
    "well_depth": "Total depth of wells (columns lower than both neighbours).",
    "tetris_readiness": "1.0 if any well is >= 4 deep (enables Tetris clears), else 0.0.",
    "column_transitions": "Filled/empty transitions within columns' occupied regions.",
    "row_transitions": "Filled/empty transitions within rows (walls count as filled).",
}


# ============================================================================
# Utility functions
# ============================================================================


def load_env(path: str) -> dict[str, str]:
    """Parse an env file (key=\"value\" format, one per line).

    Strips surrounding quotes.  Skips blank lines and comments (#).
    Returns an empty dict if the file does not exist.
    """
    result: dict[str, str] = {}
    p = Path(path)
    if not p.exists():
        return result

    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        # Strip surrounding quotes
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        result[key] = value
    return result


def check_cv_gate(scores: list[float], threshold: float) -> tuple[bool, float]:
    """Compute coefficient of variation (std / mean).

    Returns (passed, cv).  *passed* is True when cv < threshold.
    Edge case: if mean == 0, returns (False, inf).
    """
    if not scores:
        return (False, float("inf"))

    mean = statistics.mean(scores)
    if mean == 0:
        return (False, float("inf"))

    if len(scores) == 1:
        return (True, 0.0)

    std = statistics.stdev(scores)
    cv = std / abs(mean)
    return (cv < threshold, cv)


def is_improvement(new_mean: float, old_mean: float) -> bool:
    """True if *new_mean* is strictly greater than *old_mean*."""
    return new_mean > old_mean


# ============================================================================
# API call
# ============================================================================


async def call_anthropic(
    system: str, prompt: str, model: str, api_key: str
) -> str:
    """Call the Anthropic Messages API via the official SDK.

    Returns the text content of the first response block.
    Raises on failure after logging the error.
    """
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=api_key)
    message = await client.messages.create(
        model=model,
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


# ============================================================================
# Prompt builders
# ============================================================================


def build_health_check_prompt(agent: str) -> str:
    """Return a 3-line health check prompt for the given agent role."""
    checks = {
        "builder": (
            "Confirm you are active as the Builder agent.\n"
            "What are the 8 Tetris feature weights you must output?\n"
            "What is the Line-Clear Greed Trap and why must you avoid it?"
        ),
        "critic": (
            "Confirm you are active as the Critic (The Pessimist).\n"
            "What is Gate 1 (frozen_compliance) and its threshold?\n"
            "What is your specific mission regarding the frozen specification?"
        ),
        "reviewer": (
            "Confirm you are active as the Reviewer (The Linter).\n"
            "What do you check (weight hygiene) and what do you NOT evaluate?\n"
            "What makes a weight vector invalid?"
        ),
    }
    return checks.get(agent, f"Confirm you are active as the {agent} agent.")


def build_builder_prompt(
    weights: dict[str, float],
    best_score: float,
    dead_ends: list[str],
    innovation_log_tail: str,
    feature_descriptions: dict[str, str],
    mode: str,
) -> str:
    """Assemble the full Builder prompt with runtime context."""
    active_features = [name for name, w in weights.items() if w != 0.0]
    inactive_features = [name for name, w in weights.items() if w == 0.0]

    dead_end_block = "\n".join(f"- {d}" for d in dead_ends) if dead_ends else "None"

    feature_block = "\n".join(
        f"- **{name}**: {desc}" for name, desc in feature_descriptions.items()
    )

    mode_guidance = {
        "VALIDATION": (
            "MODE: VALIDATION -- Make conservative, well-justified changes. "
            "Small deltas from the current weights.  Every change must be "
            "grounded in Tetris heuristic research."
        ),
        "EXPLORATION": (
            "MODE: EXPLORATION -- You may take bigger swings. "
            "Activate inactive features, try bolder weight ratios. "
            "State your hypothesis for why the change should help."
        ),
    }

    return f"""You are the Builder agent in a CHP Tetris optimization loop.

## Current Weights
```json
{json.dumps(weights, indent=2)}
```

## Best Score So Far
{best_score} lines cleared (mean across 10 seeds)

## Dead Ends — DO NOT REPEAT
{dead_end_block}

## Recent Innovation Log
{innovation_log_tail if innovation_log_tail else "No prior turns yet."}

## Feature Descriptions
{feature_block}

## Active Features (weight != 0)
{', '.join(active_features) if active_features else 'NONE — all features are disabled!'}

## Inactive Features (weight == 0)
{', '.join(inactive_features) if inactive_features else 'All features are active.'}

## {mode_guidance.get(mode, f'MODE: {mode}')}

## CRITICAL: Line-Clear Greed Trap
The hole penalty (|holes|) must be 3-5x stronger than the line clear reward (|complete_lines|).
LLMs consistently get this wrong.  Holes are catastrophic; line clears are nice-to-have.

## Output
Respond with a JSON object containing exactly these 8 keys:
aggregate_height, complete_lines, holes, bumpiness, well_depth, tetris_readiness, column_transitions, row_transitions

All values must be finite floats.  Do not omit any key.
"""


def build_critic_prompt(
    weights: dict[str, float],
    old_weights: dict[str, float],
    scores: list[float],
    cv: float,
    prior_traps_detected: list[str],
    mode: str,
) -> str:
    """Assemble the full Critic prompt with runtime context."""
    mean_score = statistics.mean(scores) if scores else 0.0

    trap_block = ""
    if prior_traps_detected:
        trap_block = (
            "\n## WARNING: Known Traps Detected\n"
            + "\n".join(f"- {t}" for t in prior_traps_detected)
            + "\n"
        )

    mode_instruction = {
        "VALIDATION": (
            "MODE: VALIDATION -- You are a HARD BLOCKER.  If any blocking gate "
            "fails, the weights MUST be rejected."
        ),
        "EXPLORATION": (
            "MODE: EXPLORATION -- You are ADVISORY ONLY.  Flag issues but do not "
            "block acceptance.  The loop is exploring."
        ),
    }

    return f"""You are the Critic (The Pessimist) in a CHP Tetris optimization loop.
Assume the weights are worse until the data proves otherwise.

## Proposed Weights
```json
{json.dumps(weights, indent=2)}
```

## Previous Weights
```json
{json.dumps(old_weights, indent=2)}
```

## Game Results (10 seeds)
Scores (lines cleared): {scores}
Mean: {mean_score:.1f}
Coefficient of Variation: {cv:.4f}
{trap_block}
## {mode_instruction.get(mode, f'MODE: {mode}')}

## Gate Scoring
Score each gate from 0.0 to 1.0:
- Gate 1 (frozen_compliance): >= 1.0 required (BLOCKING). Were frozen files untouched? Is the weight format valid?
- Gate 2 (architecture): >= 0.85 target. Do weights make structural sense?
- Gate 3 (scientific_validity): >= 0.85 target. Do weights align with Tetris research?
- Gate 4 (drift_check): >= 0.85 target. Is the change from previous weights justified?

## Line-Clear Greed Trap Check
Check: Is |complete_lines| > |holes| while |holes| < 2.0?  If so, flag it.

## Output Format
gate_1_frozen_compliance: <score>
gate_2_architecture: <score>
gate_3_scientific_validity: <score>
gate_4_drift_check: <score>

blocking_issues:
- <list or NONE>

nonblocking_issues:
- <list or NONE>

verdict: PASS or NEEDS_IMPROVEMENT

next_turn_priority: <recommendation>
"""


def build_reviewer_prompt(weights: dict[str, float]) -> str:
    """Assemble the Reviewer (hygiene-only) prompt."""
    return f"""You are the Reviewer (The Linter) in a CHP Tetris optimization loop.
Your job is weight hygiene validation ONLY.  You do NOT evaluate scientific validity or architecture.

## Weight Vector to Review
```json
{json.dumps(weights, indent=2)}
```

## Hygiene Checks
1. All 8 required keys present: aggregate_height, complete_lines, holes, bumpiness, well_depth, tetris_readiness, column_transitions, row_transitions
2. No unknown/extra keys
3. All values are valid finite numbers (no NaN, no Infinity)
4. No extremely large magnitudes (|value| > 1000 is suspicious)
5. Types are numeric (int or float)

## Output Format
issues:
- [CRITICAL|WARNING|MINOR]: <description>

verdict: APPROVE | APPROVE WITH NOTES | NEEDS REVISION
"""


# ============================================================================
# TurnState
# ============================================================================


@dataclass
class TurnState:
    """Mutable state carried across turns."""

    turn: int = 0
    best_weights: dict = field(default_factory=dict)
    best_score: float = 0.0
    weights_history: list[dict] = field(default_factory=list)
    config: dict = field(default_factory=dict)
    api_key: str = ""
    env_keys: dict = field(default_factory=dict)
    stop_requested: bool = False


# ============================================================================
# run_turn — The Full 16-Step CHP Turn Cycle
# ============================================================================


async def run_turn(
    state: TurnState,
    broadcast_fn: Callable[..., Any],
    modes: ModeManager,
    memory: MemoryManager,
    telemetry: TelemetryStore,
) -> dict[str, Any]:
    """Execute one full 16-step CHP turn.

    Returns a dict with turn results including whether new weights were
    accepted, the exit condition (if any), and all intermediate data.
    """
    state.turn += 1
    turn = state.turn
    mode = modes.current_mode
    _log.info("=" * 60)
    _log.info("TURN %d — MODE: %s", turn, mode)
    _log.info("=" * 60)

    metrics = TurnMetrics(turn=turn, mode=mode)
    timer = TurnTimer(metrics)

    cfg = state.config
    model_cfg = cfg.get("models", {})
    gate_cfg = cfg.get("gates", {})
    loop_cfg = cfg.get("loop", {})
    exit_cfg = cfg.get("exit_conditions", {})

    builder_model = model_cfg.get("builder", "claude-sonnet-4-20250514")
    critic_model = model_cfg.get("critic", "claude-sonnet-4-20250514")
    reviewer_model = model_cfg.get("reviewer", "claude-sonnet-4-20250514")

    cv_threshold = gate_cfg.get("cv_threshold", 0.15)
    num_seeds = gate_cfg.get("seeds", 10)
    max_anomalies = gate_cfg.get("max_consecutive_anomalies", 3)

    science_target = exit_cfg.get("science_target_lines", 10000)
    auto_tag = loop_cfg.get("auto_tag", True)

    consecutive_anomalies = 0
    accepted = False
    exit_reason: str | None = None
    new_weights: dict | None = None
    scores: list[float] = []
    new_mean = 0.0
    cv = 0.0
    anomaly = False

    with timer:
        # ------------------------------------------------------------------
        # STEP 1 — Health checks (Layer 8)
        # ------------------------------------------------------------------
        _log.info("Step 1: Health checks")
        agents = ["builder", "critic", "reviewer"]
        for agent_name in agents:
            try:
                hc_prompt = build_health_check_prompt(agent_name)
                system = f"You are the {agent_name} agent.  Answer the health check."
                hc_response = await call_anthropic(
                    system=system,
                    prompt=hc_prompt,
                    model=builder_model,
                    api_key=state.api_key,
                )
                passed = len(hc_response) > 20  # basic sanity
                broadcast_fn({
                    "type": "health_check",
                    "agent": agent_name,
                    "passed": passed,
                })
                if not passed:
                    _log.error("Health check FAILED for %s", agent_name)
                    broadcast_fn({
                        "type": "turn_complete",
                        "turn": turn,
                        "accepted": False,
                        "reason": f"Health check failed: {agent_name}",
                    })
                    telemetry.add_turn(metrics)
                    return {"turn": turn, "accepted": False, "reason": f"health_check_failed:{agent_name}"}
            except Exception as e:
                _log.error("Health check error for %s: %s", agent_name, e)
                broadcast_fn({
                    "type": "health_check",
                    "agent": agent_name,
                    "passed": False,
                })
                broadcast_fn({
                    "type": "turn_complete",
                    "turn": turn,
                    "accepted": False,
                    "reason": f"Health check error: {agent_name}: {e}",
                })
                telemetry.add_turn(metrics)
                return {"turn": turn, "accepted": False, "reason": f"health_check_error:{agent_name}"}

        # ------------------------------------------------------------------
        # STEP 2 — Dead end check (Layer 5)
        # ------------------------------------------------------------------
        _log.info("Step 2: Dead end check")
        dead_ends = memory.load_dead_ends()
        _log.info("Dead ends to avoid: %s", dead_ends)

        # ------------------------------------------------------------------
        # STEP 3 — Context load (Layer 5)
        # ------------------------------------------------------------------
        _log.info("Step 3: Context load")
        state_vector = memory.read_state_vector()
        innovation_tail = memory.last_innovation_entry()

        # ------------------------------------------------------------------
        # STEP 4 — Council review (Layer 4) — VALIDATION only, before build
        # ------------------------------------------------------------------
        _log.info("Step 4: Council review")
        council_result: CouncilResult | None = None
        if mode == VALIDATION:
            council_cfg = model_cfg.get("council", [])
            has_openai = bool(state.env_keys.get("OPENAI_API_KEY"))
            has_xai = bool(state.env_keys.get("XAI_API_KEY"))
            if has_openai or has_xai:
                try:
                    innovation_log = memory.read_full_log()
                    council_result = run_council(innovation_log, council_cfg)
                    broadcast_fn({
                        "type": "council_result",
                        "n_succeeded": council_result.n_succeeded,
                        "drift_flagged": council_result.any_drift_flagged,
                    })
                except Exception as e:
                    _log.warning("Council review failed: %s", e)
            else:
                _log.warning("Council skipped — missing API keys (OPENAI_API_KEY / XAI_API_KEY)")

        # ------------------------------------------------------------------
        # STEP 5 — Builder (Layer 2)
        # ------------------------------------------------------------------
        _log.info("Step 5: Builder")
        old_weights = dict(state.best_weights)
        try:
            builder_prompt = build_builder_prompt(
                weights=old_weights,
                best_score=state.best_score,
                dead_ends=dead_ends,
                innovation_log_tail=innovation_tail,
                feature_descriptions=FEATURE_DESCRIPTIONS,
                mode=mode,
            )
            builder_system = (
                "You are the Builder agent for a Tetris AI weight optimizer. "
                "Output a JSON weight object with exactly 8 keys."
            )
            builder_response = await call_anthropic(
                system=builder_system,
                prompt=builder_prompt,
                model=builder_model,
                api_key=state.api_key,
            )
            new_weights = parse_weights_from_response(builder_response)
            if new_weights is None:
                _log.error("Builder output could not be parsed into valid weights")
                broadcast_fn({
                    "type": "turn_complete",
                    "turn": turn,
                    "accepted": False,
                    "reason": "Builder output parse failure",
                })
                telemetry.add_turn(metrics)
                return {"turn": turn, "accepted": False, "reason": "builder_parse_failure"}
        except Exception as e:
            _log.error("Builder API call failed: %s — retrying once", e)
            await asyncio.sleep(5)
            try:
                builder_response = await call_anthropic(
                    system=builder_system,
                    prompt=builder_prompt,
                    model=builder_model,
                    api_key=state.api_key,
                )
                new_weights = parse_weights_from_response(builder_response)
                if new_weights is None:
                    telemetry.add_turn(metrics)
                    return {"turn": turn, "accepted": False, "reason": "builder_parse_failure_retry"}
            except Exception as e2:
                _log.error("Builder retry also failed: %s", e2)
                telemetry.add_turn(metrics)
                return {"turn": turn, "accepted": False, "reason": f"builder_api_failure:{e2}"}

        # ------------------------------------------------------------------
        # STEP 6 — Frozen validation (Layer 3)
        # ------------------------------------------------------------------
        _log.info("Step 6: Frozen validation")
        if not validate_weights(new_weights):
            _log.error("Gate 1 FAILURE: invalid weight structure")
            metrics.gate_1_frozen = 0.0
            broadcast_fn({
                "type": "turn_complete",
                "turn": turn,
                "accepted": False,
                "reason": "Gate 1: frozen validation failed",
            })
            telemetry.add_turn(metrics)
            exit_reason = "EXIT 4: Gate 1 failed (frozen violation)"
            return {"turn": turn, "accepted": False, "reason": "gate1_failure", "exit": exit_reason}

        # ------------------------------------------------------------------
        # STEP 7 — Run games (Layer 6)
        # ------------------------------------------------------------------
        _log.info("Step 7: Run games across %d seeds", num_seeds)
        evaluate_fn = build_evaluate_fn(new_weights)
        scores = []
        game_failures = 0
        for seed in range(num_seeds):
            try:
                result = play_game(evaluate_fn, seed)
                scores.append(float(result.lines_cleared))
            except Exception as e:
                _log.error("Game seed %d failed: %s", seed, e)
                scores.append(0.0)
                game_failures += 1

        new_mean = statistics.mean(scores) if scores else 0.0
        cv = 0.0
        if len(scores) > 1:
            _, cv = check_cv_gate(scores, cv_threshold)

        metrics.seeds_run = num_seeds
        metrics.seeds_passed = num_seeds - game_failures

        # >50% game failures = anomaly
        if game_failures > num_seeds / 2:
            anomaly = True
            metrics.anomaly = True

        broadcast_fn({
            "type": "game_results",
            "scores": scores,
            "mean": new_mean,
            "cv": cv,
        })

        # ------------------------------------------------------------------
        # STEP 8 — Sigma gate (Layer 6)
        # ------------------------------------------------------------------
        _log.info("Step 8: Sigma gate")
        sigma_passed, sigma_cv = check_cv_gate(scores, cv_threshold)
        seed_status = ["pass" if s > 0 else "fail" for s in scores]

        if not sigma_passed:
            anomaly = True
            metrics.anomaly = True
            metrics.stochastic_instability = True

        broadcast_fn({
            "type": "sigma_gate",
            "passed": sigma_passed,
            "cv": sigma_cv,
            "threshold": cv_threshold,
            "seeds": seed_status,
        })

        # ------------------------------------------------------------------
        # STEP 9 — Critic (Layers 1, 2)
        # ------------------------------------------------------------------
        _log.info("Step 9: Critic")
        # Check prior errors (known traps)
        prior_traps: list[str] = []
        for trap in KNOWN_TRAPS:
            if trap["detect"](new_weights):
                prior_traps.append(trap["name"])
                _log.warning("Trap detected: %s", trap["name"])

        try:
            critic_prompt = build_critic_prompt(
                weights=new_weights,
                old_weights=old_weights,
                scores=scores,
                cv=sigma_cv,
                prior_traps_detected=prior_traps,
                mode=mode,
            )
            critic_system = (
                "You are the Critic (The Pessimist).  Assume the weights are worse "
                "until the data proves otherwise.  Score all 4 gates."
            )
            critic_response = await call_anthropic(
                system=critic_system,
                prompt=critic_prompt,
                model=critic_model,
                api_key=state.api_key,
            )
            verdict = parse_verdict(critic_response)
        except Exception as e:
            _log.error("Critic API call failed: %s — retrying once", e)
            await asyncio.sleep(5)
            try:
                critic_response = await call_anthropic(
                    system=critic_system,
                    prompt=critic_prompt,
                    model=critic_model,
                    api_key=state.api_key,
                )
                verdict = parse_verdict(critic_response)
            except Exception as e2:
                _log.error("Critic retry also failed: %s", e2)
                verdict = CriticVerdict(verdict="NEEDS_IMPROVEMENT")

        metrics.gate_1_frozen = verdict.gate_1_frozen
        metrics.gate_2_architecture = verdict.gate_2_architecture
        metrics.gate_3_scientific = verdict.gate_3_scientific
        metrics.gate_4_drift = verdict.gate_4_drift
        metrics.critic_verdict = verdict.verdict

        blocking = verdict.blocking_issues or []
        broadcast_fn({
            "type": "critic_verdict",
            "gates": {
                "frozen": verdict.gate_1_frozen,
                "architecture": verdict.gate_2_architecture,
                "scientific": verdict.gate_3_scientific,
                "drift": verdict.gate_4_drift,
            },
            "blocking": blocking,
            "verdict": verdict.verdict,
        })

        # ------------------------------------------------------------------
        # STEP 10 — Reviewer (Layer 2)
        # ------------------------------------------------------------------
        _log.info("Step 10: Reviewer")
        try:
            reviewer_prompt_text = build_reviewer_prompt(new_weights)
            reviewer_system = (
                "You are the Reviewer (The Linter).  Check weight hygiene only."
            )
            reviewer_response = await call_anthropic(
                system=reviewer_system,
                prompt=reviewer_prompt_text,
                model=reviewer_model,
                api_key=state.api_key,
            )
            review = parse_review(reviewer_response)
        except Exception as e:
            _log.error("Reviewer failed: %s", e)
            review = ReviewResult(verdict="APPROVE")

        broadcast_fn({
            "type": "reviewer_verdict",
            "issues": [
                {"severity": i.severity, "description": i.description}
                for i in review.issues
            ],
            "verdict": review.verdict,
        })

        # ------------------------------------------------------------------
        # STEP 11 — Compare
        # ------------------------------------------------------------------
        _log.info("Step 11: Compare")
        improved = is_improvement(new_mean, state.best_score)

        # Determine if critic blocks acceptance
        critic_blocks = modes.critic_is_blocker and (
            verdict.has_blocking or not verdict.all_gates_met
        )

        reviewer_blocks = review.needs_revision

        if improved and not critic_blocks and not reviewer_blocks:
            accepted = True
            state.best_weights = dict(new_weights)
            state.best_score = new_mean
            state.weights_history.append(dict(new_weights))
            _log.info(
                "ACCEPTED: new mean %.1f > old %.1f",
                new_mean, state.best_score if not improved else state.best_score,
            )
        else:
            accepted = False
            reasons = []
            if not improved:
                reasons.append(f"no improvement ({new_mean:.1f} <= {state.best_score:.1f})")
            if critic_blocks:
                reasons.append("critic blocked")
            if reviewer_blocks:
                reasons.append("reviewer needs revision")
            _log.info("REJECTED: %s", ", ".join(reasons))

        # ------------------------------------------------------------------
        # STEP 12 — Mode check (Layer 7)
        # ------------------------------------------------------------------
        _log.info("Step 12: Mode check")
        old_mode = modes.current_mode
        modes.record_turn(metrics_improved=improved, anomaly=anomaly)
        new_mode = modes.current_mode
        if old_mode != new_mode:
            broadcast_fn({
                "type": "mode_change",
                "from": old_mode,
                "to": new_mode,
                "turn": turn,
            })

        # ------------------------------------------------------------------
        # STEP 13 — Record (Layers 5, 8)
        # ------------------------------------------------------------------
        _log.info("Step 13: Record")
        # Innovation log
        log_content = (
            f"### Weights\n```json\n{json.dumps(new_weights, indent=2)}\n```\n\n"
            f"### Results\nMean: {new_mean:.1f}, CV: {cv:.4f}\n"
            f"Accepted: {accepted}\n\n"
            f"### What next turn should focus on\n"
            f"{verdict.next_priority if verdict.next_priority else 'Continue optimizing.'}\n"
        )
        memory.append_innovation_log(turn, modes.current_mode, log_content)

        # State vector (every N turns)
        sv_interval = cfg.get("loop", {}).get("state_vector_interval", 3)
        if turn % sv_interval == 0:
            memory.write_state_vector(
                turn,
                modes.current_mode,
                winning_params=json.dumps(state.best_weights) if state.best_weights else "none",
                metric_status=f"best={state.best_score:.1f}",
                next_focus=verdict.next_priority or "continue",
            )

        # Telemetry
        telemetry.add_turn(metrics)

        # ------------------------------------------------------------------
        # STEP 14 — Broadcast turn_complete
        # ------------------------------------------------------------------
        _log.info("Step 14: Broadcast turn_complete")
        broadcast_fn({
            "type": "turn_complete",
            "turn": turn,
            "accepted": accepted,
            "best_score": state.best_score,
            "new_mean": new_mean,
            "cv": cv,
            "mode": modes.current_mode,
            "weights": new_weights if accepted else state.best_weights,
        })

        # ------------------------------------------------------------------
        # STEP 15 — Git tag (Layer 9)
        # ------------------------------------------------------------------
        if auto_tag and accepted:
            _log.info("Step 15: Git tag")
            try:
                import subprocess
                tag_name = f"chp-turn-{turn}-pass"
                subprocess.run(
                    ["git", "tag", tag_name],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                _log.info("Git tag created: %s", tag_name)
            except Exception as e:
                _log.warning("Git tag failed: %s", e)

        # ------------------------------------------------------------------
        # STEP 16 — Exit check (Layer 9)
        # ------------------------------------------------------------------
        _log.info("Step 16: Exit check")

        # EXIT 1: Science target reached
        if new_mean >= science_target and sigma_passed:
            exit_reason = f"EXIT 1: science target reached ({new_mean:.1f} >= {science_target})"

        # EXIT 2: Stagnation + exploration exhausted
        if (
            modes.stagnation_streak >= cfg.get("loop", {}).get("stagnation_threshold", 3)
            and modes.exploration_streak >= cfg.get("loop", {}).get("max_consecutive_exploration", 2)
        ):
            exit_reason = "EXIT 2: stagnation + exploration exhausted"

        # EXIT 3: Consecutive anomalies
        # Track via telemetry
        recent_anomalies = 0
        for t in reversed(telemetry.turns):
            if t.anomaly:
                recent_anomalies += 1
            else:
                break
        if recent_anomalies >= max_anomalies:
            exit_reason = f"EXIT 3: {recent_anomalies} consecutive anomalies"

        # EXIT 4: Gate 1 failure (already handled above in step 6)

        # EXIT 5: STOP file or stop_requested
        if state.stop_requested or Path("STOP").exists():
            exit_reason = "EXIT 5: STOP requested"

    # End of timer context

    result = {
        "turn": turn,
        "accepted": accepted,
        "best_score": state.best_score,
        "new_mean": new_mean,
        "cv": cv,
        "mode": modes.current_mode,
        "anomaly": anomaly,
        "weights": new_weights,
    }
    if exit_reason:
        result["exit"] = exit_reason
    return result


# ============================================================================
# run_loop — Main Loop
# ============================================================================


async def run_loop(config_path: str, broadcast_fn: Callable[..., Any]) -> None:
    """Main optimization loop.

    1. Load config.yaml
    2. Load api.env from project root
    3. Initialize ModeManager, MemoryManager, TelemetryStore
    4. Initialize TurnState with baseline weights
    5. Loop: call run_turn() until exit or max_turns
    6. On exit, broadcast final message.
    """
    # 1. Load config
    config = Config.from_yaml(config_path)
    raw_cfg = config.raw

    # 2. Load env keys
    project_root = Path(config_path).parent
    env_path = project_root / "api.env"
    # Also check the repo root
    if not env_path.exists():
        env_path = Path("api.env")
    env_keys = load_env(str(env_path))

    api_key = env_keys.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY", ""))
    if not api_key:
        _log.error("No ANTHROPIC_API_KEY found in api.env or environment")
        broadcast_fn({"type": "exit", "reason": "missing_api_key", "turn": 0})
        return

    # Inject env keys into environment for council
    for k, v in env_keys.items():
        os.environ[k] = v

    # 3. Initialize managers
    modes = ModeManager(config)
    memory = MemoryManager(config)
    telemetry = TelemetryStore.load()
    telemetry.project_name = config.project_name

    # 4. Initialize TurnState
    weights_path = project_root / "weights.json"
    baseline_weights = {}
    if weights_path.exists():
        baseline_weights = json.loads(weights_path.read_text(encoding="utf-8"))
    else:
        _log.warning("No weights.json found — using zero weights")
        baseline_weights = {name: 0.0 for name in FEATURE_NAMES}

    state = TurnState(
        best_weights=baseline_weights,
        best_score=0.0,
        weights_history=[dict(baseline_weights)],
        config=raw_cfg,
        api_key=api_key,
        env_keys=env_keys,
    )

    max_turns = raw_cfg.get("loop", {}).get("max_turns", 20)

    # 5. Loop
    _log.info("Starting CHP optimization loop (max %d turns)", max_turns)
    for _ in range(max_turns):
        result = await run_turn(state, broadcast_fn, modes, memory, telemetry)

        if "exit" in result:
            _log.info("EXIT: %s at turn %d", result["exit"], result["turn"])
            broadcast_fn({
                "type": "exit",
                "reason": result["exit"],
                "turn": result["turn"],
            })
            return

    # Reached max turns without explicit exit
    broadcast_fn({
        "type": "exit",
        "reason": f"max_turns ({max_turns}) reached",
        "turn": state.turn,
    })
    _log.info("Loop complete: max turns reached (%d)", max_turns)
