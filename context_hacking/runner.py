"""
CHP Experiment Runner — executes the full 9-layer protocol autonomously.

This module manages a multi-turn conversation with the Anthropic API,
driving the Builder/Critic/Reviewer cycle for each milestone in an experiment.

Each turn:
  1. Send context (frozen spec, dead ends, state vector, current milestone)
  2. Receive code from the Builder
  3. Write code to disk
  4. Run tests
  5. Send test results back for Critic review
  6. Receive gate scores + fixes
  7. Update innovation log + state vector
  8. Loop to next milestone

Methods:
  "api"         — Anthropic API multi-turn loop (autonomous)
  "claude-cli"  — Pipe single prompt to Claude Code CLI
  "interactive" — Write prompt file for manual use

Usage:
    from context_hacking.runner import run_experiment
    run_experiment("schelling-segregation", method="api")
"""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

_log = logging.getLogger(__name__)

PACKAGE_ROOT = Path(__file__).parent.parent
LOOP_TEMPLATE_PATH = PACKAGE_ROOT / "prompts" / "loop_template.md"


# ── Retry helper ────────────────────────────────────────────────────────────

def _api_call_with_retry(call_fn, max_retries: int = 3,
                         base_delay: float = 1.0, **kwargs):
    """Call a function with exponential backoff on transient errors.

    Args:
        call_fn: callable that accepts **kwargs
        max_retries: max attempts
        base_delay: initial delay in seconds (doubled each retry)
        **kwargs: passed through to call_fn

    Returns:
        Result from call_fn on success

    Raises:
        Last exception if all retries exhausted
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            return call_fn(**kwargs)
        except (ConnectionError, TimeoutError, OSError) as e:
            last_error = e
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                _log.warning("API error (attempt %d/%d), retrying in %.0fs: %s",
                             attempt + 1, max_retries, delay, e)
                time.sleep(delay)
            else:
                _log.error("API error after %d attempts: %s", max_retries, e)
    raise last_error


# ── Context window management ───────────────────────────────────────────────

def _estimate_tokens(messages: list[dict]) -> int:
    """Estimate token count from messages. ~4 chars per token heuristic."""
    total_chars = sum(len(m.get("content", "")) for m in messages)
    return total_chars // 4


def _maybe_summarize_messages(messages: list[dict],
                               max_tokens: int = 150_000,
                               keep_recent: int = 6) -> list[dict]:
    """If messages exceed max_tokens, summarize older turns.

    Keeps the first message (system context) and last keep_recent messages.
    Replaces middle messages with a synopsis.
    """
    estimated = _estimate_tokens(messages)
    if estimated <= max_tokens:
        return messages

    if len(messages) <= keep_recent + 1:
        return messages

    first = messages[0]
    recent = messages[-keep_recent:]
    middle = messages[1:-keep_recent]

    turns_summarized = len(middle) // 2
    synopsis_parts = []
    for i in range(0, len(middle), 2):
        user_msg = middle[i].get("content", "")
        synopsis_parts.append(f"- Turn: {user_msg[:100]}...")

    synopsis = (f"[CONTEXT SUMMARY: {turns_summarized} earlier turns summarized to save context]\n"
                + "\n".join(synopsis_parts[:20]))

    summary_msg = {"role": "user", "content": synopsis}
    return [first, summary_msg] + recent


# ── Context loading ──────────────────────────────────────────────────────────

def _load_experiment_context(experiment_dir: Path) -> dict[str, str]:
    """Read all experiment context files into a dict."""
    files: dict[str, str] = {}
    for name in ["CHAIN_PROMPT.md", "spec.md", "dead_ends.md",
                  "state_vector.md", "innovation_log.md", "config.yaml"]:
        fpath = experiment_dir / name
        if fpath.exists():
            files[name] = fpath.read_text(encoding="utf-8")

    frozen_dir = experiment_dir / "frozen"
    if frozen_dir.exists():
        for fp in frozen_dir.glob("*.md"):
            files[f"frozen/{fp.name}"] = fp.read_text(encoding="utf-8")

    return files


def _build_system_prompt(experiment_dir: Path) -> str:
    """Build the system prompt with full experiment context."""
    context = _load_experiment_context(experiment_dir)
    exp_name = experiment_dir.name

    parts = [
        f"You are the CHP (Context Hacking Protocol) autonomous builder for "
        f"the '{exp_name}' experiment.\n",
        "You play THREE roles in sequence each turn:\n"
        "1. BUILDER: Write code that matches the frozen spec exactly.\n"
        "2. CRITIC: Score 4 gates (frozen=1.0, architecture>=0.85, "
        "scientific>=0.85, drift>=0.85). Argue AGAINST the science before scoring.\n"
        "3. REVIEWER: Check code hygiene only (PEP8, no print, seeded rng).\n",
        "RULES:\n"
        "- Every coefficient must match the frozen spec EXACTLY.\n"
        "- All randomness via seeded numpy.random.Generator.\n"
        "- No print() — use logging.\n"
        "- Read dead_ends.md before each turn — do NOT repeat logged failures.\n"
        "- When you encounter the EXPECTED FALSE POSITIVE (described in spec.md), "
        "catch it, fix it, and log it clearly.\n",
        "CONTEXT FILES:\n",
    ]

    for name, content in context.items():
        parts.append(f"\n=== {name} ===\n{content}\n")

    parts.append(
        f"\nWORKING DIRECTORY: {experiment_dir}\n"
        f"Write all code files to this directory.\n"
        f"Run tests with: python -m pytest {experiment_dir}/tests/ -v\n"
    )

    return "\n".join(parts)


# ── Multi-turn API loop ──────────────────────────────────────────────────────

def _run_api_loop(experiment_dir: Path, max_turns: int = 8, resume_state: dict | None = None) -> None:
    """Execute the full CHP loop via Anthropic API multi-turn conversation."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not set. "
            "Set it in your environment or use --method interactive."
        )

    try:
        import anthropic
    except ImportError:
        raise ImportError("pip install anthropic — required for API method")

    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = _build_system_prompt(experiment_dir)
    exp_name = experiment_dir.name
    messages: list[dict[str, str]] = []

    # Read spec to find milestones
    spec_path = experiment_dir / "spec.md"
    spec_text = spec_path.read_text(encoding="utf-8") if spec_path.exists() else ""
    milestones = re.findall(r"^\d+\.\s+(.+?)(?:\s*—|\s*$)", spec_text, re.MULTILINE)

    # Initialize telemetry
    from context_hacking.core.telemetry import TelemetryStore, TurnMetrics, TurnTimer
    telemetry = TelemetryStore.load()
    telemetry.project_name = exp_name
    telemetry.start_time = time.strftime("%Y-%m-%d %H:%M")

    # Determine starting turn (resume support)
    start_turn = 1
    if resume_state:
        start_turn = int(resume_state.get("TURN", "0")) + 1

    _log.info("Starting CHP loop: %s (%d milestones detected)", exp_name, len(milestones))
    print(f"\n{'='*60}")
    print(f"CHP Autonomous Loop — {exp_name}")
    print(f"Milestones: {len(milestones)}")
    print(f"Max turns: {max_turns}")
    if start_turn > 1:
        print(f"Resuming from turn: {start_turn}")
    print(f"{'='*60}\n")

    try:
      for turn in range(start_turn, max_turns + 1):
        # ── Build the turn prompt ────────────────────────────────────
        if turn == 1:
            user_msg = (
                f"Begin Turn 1. Read the frozen spec and dead ends carefully.\n"
                f"Build Milestone 1 from spec.md.\n"
                f"Write the code to {experiment_dir}/.\n"
                f"After writing code, critique it as The Pessimist (score 4 gates).\n"
                f"Then review it as The Linter.\n"
                f"End with: what the next turn should focus on."
            )
        else:
            # Read updated state
            sv_text = ""
            sv_path = experiment_dir / "state_vector.md"
            if sv_path.exists():
                sv_text = sv_path.read_text(encoding="utf-8")

            log_text = ""
            log_path = experiment_dir / "innovation_log.md"
            if log_path.exists():
                # Last 2000 chars of log
                full_log = log_path.read_text(encoding="utf-8")
                log_text = full_log[-2000:]

            user_msg = (
                f"Turn {turn}.\n\n"
                f"Current state:\n{sv_text}\n\n"
                f"Recent log:\n{log_text}\n\n"
                f"Continue building the next milestone from spec.md.\n"
                f"Write code, then critique (4 gates), then review.\n"
                f"If tests fail, fix and re-run.\n"
                f"Update innovation_log.md and state_vector.md.\n"
                f"End with: what the next turn should focus on."
            )

        messages.append({"role": "user", "content": user_msg})

        # ── Summarize if approaching context limit ──────────────────
        messages = _maybe_summarize_messages(messages, max_tokens=150_000)

        # ── Initialize turn metrics ────────────────────────────────
        metrics = TurnMetrics(turn=turn, timestamp=time.strftime("%Y-%m-%d %H:%M"),
                              mode="EXPLORATION" if "EXPLORATION" in user_msg.upper() else "VALIDATION")

        # ── Call API ─────────────────────────────────────────────────
        print(f"--- Turn {turn}/{max_turns} ---")
        _log.info("Turn %d: sending to API...", turn)

        with TurnTimer(metrics):
            try:
                response = _api_call_with_retry(
                    client.messages.create,
                    max_retries=3,
                    model="claude-sonnet-4-20250514",
                    max_tokens=16000,
                    system=system_prompt,
                    messages=messages,
                )
                reply = response.content[0].text
                _log.info("Turn %d: received %d chars in %.1fs", turn, len(reply), metrics.duration_seconds)

                # Record token usage
                if hasattr(response, "usage"):
                    metrics.tokens_input = getattr(response.usage, "input_tokens", 0)
                    metrics.tokens_output = getattr(response.usage, "output_tokens", 0)
                    metrics.tokens_total = metrics.tokens_input + metrics.tokens_output
            except Exception as e:
                _log.error("API error on turn %d: %s", turn, e)
                print(f"API ERROR: {e}")
                break

        messages.append({"role": "assistant", "content": reply})

        # ── Extract and write code blocks ────────────────────────────
        code_blocks = _extract_code_blocks(reply)
        total_lines = 0
        for filename, code in code_blocks.items():
            filepath = experiment_dir / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(code, encoding="utf-8")
            lines = code.count("\n") + 1
            total_lines += lines
            print(f"  Wrote: {filepath.name} ({len(code)} chars, {lines} lines)")
            _log.info("Wrote %s (%d chars)", filepath, len(code))
        metrics.files_written = len(code_blocks)
        metrics.lines_written = total_lines

        # ── Run tests if any code was written ────────────────────────
        test_dir = experiment_dir / "tests"
        if code_blocks and test_dir.exists():
            print(f"  Running tests...")
            test_result = _run_tests(experiment_dir)
            metrics.tests_passed = test_result["passed"]
            metrics.tests_failed = test_result["failed"]
            metrics.tests_skipped = test_result.get("skipped", 0)
            metrics.tests_passed_first_try = test_result["failed"] == 0

            if test_result["failed"] > 0:
                messages.append({
                    "role": "user",
                    "content": (
                        f"Test results: {test_result['passed']} passed, "
                        f"{test_result['failed']} failed.\n"
                        f"Output:\n{test_result['output'][-3000:]}\n\n"
                        f"Fix the failing tests and continue."
                    ),
                })
                print(f"  Tests: {test_result['passed']} passed, {test_result['failed']} FAILED")
            else:
                print(f"  Tests: {test_result['passed']} passed, 0 failed")

        # ── Parse critic scores from reply ───────────────────────────
        from context_hacking.agents.critic import parse_verdict
        verdict = parse_verdict(reply)
        metrics.gate_1_frozen = verdict.gate_1_frozen
        metrics.gate_2_architecture = verdict.gate_2_architecture
        metrics.gate_3_scientific = verdict.gate_3_scientific
        metrics.gate_4_drift = verdict.gate_4_drift
        metrics.critic_verdict = verdict.verdict
        metrics.blocking_issues_found = len(verdict.blocking_issues or [])

        # ── Detect false positive ────────────────────────────────────
        if "FALSE POSITIVE" in reply.upper():
            metrics.false_positive_caught = True
            fp_match = re.search(r"FALSE POSITIVE[^:]*:\s*(.{10,200})", reply, re.IGNORECASE)
            metrics.false_positive_description = fp_match.group(1).strip() if fp_match else "see log"

        # ── Dead ends ────────────────────────────────────────────────
        de_path = experiment_dir / "dead_ends.md"
        if de_path.exists():
            metrics.dead_ends_checked = len(_dead_ends_from_file(de_path))
        if "DEAD END" in reply.upper() and "DO NOT REPEAT" in reply.upper():
            metrics.new_dead_ends_logged = 1

        # ── Record telemetry ─────────────────────────────────────────
        telemetry.add_turn(metrics)
        print(f"  Telemetry: {metrics.tokens_total} tokens, {metrics.lines_written} lines, "
              f"gate3={metrics.gate_3_scientific:.2f}, "
              f"{'FP CAUGHT' if metrics.false_positive_caught else 'no FP'}")

        # ── Check for completion ─────────────────────────────────────
        if _check_completion(reply):
            print(f"\n{'='*60}")
            print(f"EXPERIMENT COMPLETE at turn {turn}")
            print(f"{'='*60}")
            _log.info("Experiment %s complete at turn %d", exp_name, turn)
            break

        # ── Update state vector ──────────────────────────────────────
        _update_state_vector(experiment_dir, turn, reply)

        print()

    # ── Write final report if not already written ────────────────────
    report_path = experiment_dir / "REPORT.md"
    if not report_path.exists():
        _write_completion_log(experiment_dir, turn, messages)

    print(f"\nExperiment {exp_name} complete. See {experiment_dir}/")


def _extract_code_blocks(text: str) -> dict[str, str]:
    """Extract ```python blocks with filename hints from API response."""
    blocks: dict[str, str] = {}

    # Pattern: ```python or ```py followed by code
    pattern = re.compile(
        r'(?:#\s*(?:File:|filename:)\s*(\S+\.py)\s*\n)?'
        r'```(?:python|py)\s*\n(.*?)```',
        re.DOTALL,
    )

    for match in pattern.finditer(text):
        filename = match.group(1)
        code = match.group(2).strip()

        if not filename:
            # Try to infer filename from code
            if "class SchellingGrid" in code or "def run_simulation" in code:
                if "schelling" in code.lower() or "segregation" in code.lower():
                    filename = "schelling.py"
                elif "spatial" in code.lower() or "payoff" in code.lower():
                    filename = "spatial_pd.py"
                elif "prey" in code.lower() or "predator" in code.lower():
                    filename = "lotka_volterra.py"
                elif "SIR" in code or "infected" in code.lower():
                    filename = "sir_model.py"
                elif "lorenz" in code.lower():
                    filename = "lorenz.py"
                elif "grover" in code.lower() or "oracle" in code.lower():
                    filename = "grover.py"
                elif "izhikevich" in code.lower() or "membrane" in code.lower():
                    filename = "izhikevich.py"
                elif "consensus" in code.lower() or "pbft" in code.lower():
                    filename = "consensus.py"
                elif "hyperparam" in code.lower() or "bayesian" in code.lower():
                    filename = "hyperparam_search.py"
                else:
                    filename = f"generated_{hash(code) % 10000}.py"

        if filename and code:
            blocks[filename] = code

    return blocks


def _run_tests(experiment_dir: Path) -> dict[str, Any]:
    """Run pytest on the experiment's test directory."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(experiment_dir / "tests"), "-v",
             "--tb=short", "-x"],
            capture_output=True, text=True, timeout=120,
            cwd=str(experiment_dir),
            env={**os.environ, "PYTHONPATH": str(experiment_dir)},
        )
        output = result.stdout + result.stderr

        # Count passed/failed
        passed = len(re.findall(r"PASSED", output))
        failed = len(re.findall(r"FAILED", output))
        skipped = len(re.findall(r"SKIPPED", output))

        return {
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "output": output,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"passed": 0, "failed": 1, "skipped": 0,
                "output": "TIMEOUT: tests took > 120s", "returncode": -1}
    except Exception as e:
        return {"passed": 0, "failed": 1, "skipped": 0,
                "output": str(e), "returncode": -1}


def _dead_ends_from_file(path: Path) -> list[str]:
    """Read dead ends file and return list of titles."""
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    return re.findall(r"^## DEAD END \d+ — (.+)$", text, re.MULTILINE)


def _check_completion(reply: str) -> bool:
    """Check if the API response indicates experiment completion."""
    completion_signals = [
        "EXPERIMENT COMPLETE",
        "EXIT — EXPERIMENT COMPLETE",
        "all milestones delivered",
        "ALL MILESTONES COMPLETE",
        "REPORT.md",
    ]
    reply_upper = reply.upper()
    return any(s.upper() in reply_upper for s in completion_signals)


def _update_state_vector(experiment_dir: Path, turn: int, reply: str) -> None:
    """Update state_vector.md from the API response."""
    sv_path = experiment_dir / "state_vector.md"
    # Extract mode and milestone from reply
    mode = "VALIDATION"
    if "EXPLORATION" in reply.upper():
        mode = "EXPLORATION"
    if "COMPLETE" in reply.upper():
        mode = "DONE"

    milestone_match = re.search(r"[Mm]ilestone\s+(\d+)", reply)
    milestone = f"Milestone {milestone_match.group(1)}" if milestone_match else f"Turn {turn}"

    sv_path.write_text(
        f"# State Vector\n\n"
        f"TURN: {turn}\n"
        f"MILESTONE: {milestone}\n"
        f"MODE: {mode}\n"
        f"LAST_PASSING_TAG: chp-turn-{turn}\n"
        f"NEXT_TURN_FOCUS: see innovation log\n",
        encoding="utf-8",
    )


def _write_completion_log(
    experiment_dir: Path, final_turn: int, messages: list[dict],
) -> None:
    """Write a summary to innovation_log.md from the conversation."""
    log_path = experiment_dir / "innovation_log.md"
    summary = f"\n\n---\n\n## Completion Summary\n\n"
    summary += f"Completed in {final_turn} turns via Anthropic API.\n"
    summary += f"Total messages: {len(messages)}\n"

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(summary)


# ── CLI-based runner (single prompt) ─────────────────────────────────────────

def _load_loop_prompt(experiment_dir: Path) -> str:
    """Load the loop template and inject experiment-specific paths."""
    if not LOOP_TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Loop template not found: {LOOP_TEMPLATE_PATH}")

    template = LOOP_TEMPLATE_PATH.read_text(encoding="utf-8")
    experiment_name = experiment_dir.name

    prompt = template.replace("{experiment_dir}", str(experiment_dir))
    prompt = prompt.replace("{experiment_name}", experiment_name)

    return prompt


def _run_claude_cli(prompt: str, experiment_dir: Path) -> None:
    """Execute the loop via Claude Code CLI."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write(prompt)
        prompt_path = f.name

    print(f"\n{'='*60}")
    print(f"CHP Loop via Claude Code CLI")
    print(f"Experiment: {experiment_dir.name}")
    print(f"Prompt: {prompt_path}")
    print(f"{'='*60}\n")

    try:
        subprocess.run(
            ["claude", "--dangerously-skip-permissions"],
            input=Path(prompt_path).read_text(encoding="utf-8"),
            text=True,
            cwd=str(experiment_dir.parent.parent),
        )
    finally:
        try:
            os.unlink(prompt_path)
        except OSError:
            pass


def _run_interactive(prompt: str, experiment_dir: Path) -> None:
    """Write the prompt to a file for manual use."""
    prompt_path = experiment_dir / "loop_prompt_ready.md"
    prompt_path.write_text(prompt, encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"CHP Loop Prompt Generated")
    print(f"{'='*60}")
    print(f"\nExperiment: {experiment_dir.name}")
    print(f"Prompt saved to: {prompt_path}")
    print(f"\nTo run the full loop, use one of:")
    print(f"  1. Claude Code:")
    print(f"     claude --dangerously-skip-permissions < {prompt_path}")
    print(f"  2. Set ANTHROPIC_API_KEY and run: chp run --method api")
    print(f"  3. Copy-paste into Claude.ai or Cursor")
    print(f"\nThe dashboard will show live progress:")
    print(f"  chp dashboard")


# ── Public API ───────────────────────────────────────────────────────────────

def run_experiment(
    experiment_name: str,
    method: str = "auto",
    project_dir: Path | None = None,
    resume_state: dict | None = None,
) -> None:
    """Run the full CHP loop on an experiment.

    Parameters
    ----------
    experiment_name:
        Name of the experiment (e.g., "schelling-segregation").
    method:
        "api"         — Anthropic API multi-turn loop (autonomous)
        "claude-cli"  — Pipe single prompt to Claude Code CLI
        "interactive" — Write prompt file for manual use
        "auto"        — Try API, fall back to claude-cli, then interactive
    project_dir:
        Project root. Defaults to current directory.
    resume_state:
        Dict from state_vector.md for crash recovery. If provided,
        the API loop starts from TURN+1.
    """
    if project_dir is None:
        project_dir = Path.cwd()

    # Find the experiment directory
    experiment_dir = project_dir / "experiments" / experiment_name
    if not experiment_dir.exists():
        experiment_dir = project_dir
        if not (experiment_dir / "frozen").exists():
            raise FileNotFoundError(
                f"Experiment not found: {experiment_name}. "
                f"Looked in {project_dir / 'experiments' / experiment_name}"
            )

    _log.info("Running CHP loop on: %s (method=%s)", experiment_name, method)

    if method == "auto":
        if os.environ.get("ANTHROPIC_API_KEY"):
            method = "api"
        else:
            try:
                subprocess.run(["claude", "--version"], capture_output=True, timeout=5)
                method = "claude-cli"
            except (FileNotFoundError, subprocess.TimeoutExpired):
                method = "interactive"
        _log.info("Auto-detected method: %s", method)

    if method == "api":
        _run_api_loop(experiment_dir, resume_state=resume_state)
    elif method == "claude-cli":
        prompt = _load_loop_prompt(experiment_dir)
        _run_claude_cli(prompt, experiment_dir)
    elif method == "interactive":
        prompt = _load_loop_prompt(experiment_dir)
        _run_interactive(prompt, experiment_dir)
    else:
        raise ValueError(f"Unknown method: {method}. Use: api, claude-cli, interactive")
