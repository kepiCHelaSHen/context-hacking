# CHP Phase 1: Core Framework Completion — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the CHP orchestrator loop fully autonomous with telemetry, crash recovery, and dual-mode execution (CLI + API).

**Architecture:** The runner drives execution (sending prompts, receiving responses). The orchestrator governs state (mode, gates, memory, telemetry). For `--method api`, runner calls orchestrator.step() which updates state, then runner sends the appropriate agent prompts via Anthropic API. For `--method cli`, runner pipes prompts through Claude Code CLI. Both paths share the same orchestrator state management.

**Tech Stack:** Python 3.11+, anthropic SDK, click CLI, pytest, pyyaml

**Spec:** `docs/superpowers/specs/2026-04-04-chp-10-of-10-master-roadmap.md` (Phase 1)

---

### File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `context_hacking/core/orchestrator.py` | Modify | Add TelemetryStore integration, emergency state dump |
| `context_hacking/core/telemetry.py` | Modify | Add `load()` classmethod for resume, validate JSON on save |
| `context_hacking/core/memory.py` | Modify | Make state_vector machine-parseable with structured YAML frontmatter |
| `context_hacking/runner.py` | Modify | Add retry logic, context window management, improve error handling |
| `context_hacking/cli.py` | Modify | Add `--resume` flag to `run` command |
| `tests/test_framework.py` | Modify | Add telemetry wiring tests, crash recovery tests |
| `tests/test_runner.py` | Modify | Add retry logic tests, context window tests |
| `tests/test_cli.py` | Modify | Add --resume tests |

---

### Task 1: Wire TelemetryStore into Orchestrator

**Files:**
- Modify: `context_hacking/core/orchestrator.py`
- Modify: `context_hacking/core/telemetry.py`
- Test: `tests/test_framework.py`

The orchestrator's `__init__` (line 103) creates GateChecker, ModeManager, MemoryManager but NOT TelemetryStore. The `step()` method (line 177) and `record_turn_result()` (line 213) don't track metrics. The runner already creates TurnMetrics (line 127-130 of runner.py), but it's not persisted through the orchestrator.

- [ ] **Step 1: Write failing test — telemetry store created on init**

Add to `tests/test_framework.py` in `TestOrchestrator`:

```python
def test_orchestrator_has_telemetry(self, config_file):
    """Orchestrator creates a TelemetryStore on init."""
    config = Config.from_yaml(config_file)
    orch = Orchestrator(config)
    assert hasattr(orch, 'telemetry')
    assert orch.telemetry is not None
    assert orch.telemetry.total_turns == 0
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_framework.py::TestOrchestrator::test_orchestrator_has_telemetry -v
```

Expected: FAIL — `AttributeError: 'Orchestrator' object has no attribute 'telemetry'`

- [ ] **Step 3: Add TelemetryStore to orchestrator init**

In `context_hacking/core/orchestrator.py`, add import at top:

```python
from context_hacking.core.telemetry import TelemetryStore
```

In `Orchestrator.__init__()` (after line ~115 where memory is created), add:

```python
        # Telemetry — persists per-turn, survives crashes
        # TelemetryStore uses module-level TELEMETRY_PATH (.chp/telemetry.json)
        self.telemetry = TelemetryStore.load()
```

Note: `TelemetryStore.save()` and `load()` use a module-level `TELEMETRY_PATH` constant — no path parameter needed.

- [ ] **Step 4: Run test to verify it passes**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_framework.py::TestOrchestrator::test_orchestrator_has_telemetry -v
```

Expected: PASS

- [ ] **Step 5: Write failing test — record_turn_result persists telemetry**

```python
def test_record_turn_persists_telemetry(self, config_file):
    """record_turn_result saves telemetry to disk."""
    config = Config.from_yaml(config_file)
    orch = Orchestrator(config)

    from context_hacking.core.telemetry import TurnMetrics
    metrics = TurnMetrics(turn=1, tokens_total=500, duration_seconds=10.0)
    orch.record_turn_result(gate_passed=True, metrics_improved=True, anomaly=False, metrics=metrics)

    assert orch.telemetry.total_turns == 1
```

- [ ] **Step 6: Run test to verify it fails**

Expected: FAIL — `record_turn_result() got unexpected keyword argument 'metrics'`

- [ ] **Step 7: Modify record_turn_result to accept and persist metrics**

The existing signature is `record_turn_result(self, gate_passed: bool, metrics_improved: bool, anomaly: bool) -> None`. Add `metrics` parameter without breaking existing callers:

```python
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

        # Auto git tag
        if self.config.auto_tag and gate_passed and not anomaly:
            self._git_tag(f"chp-turn-{self.turn}-pass")

        # Persist telemetry (new)
        if metrics is not None:
            self.telemetry.add_turn(metrics)

        _log.info(
            "Turn %d recorded: gate=%s, improved=%s, anomaly=%s, mode=%s",
            self.turn, gate_passed, metrics_improved, anomaly, self.current_mode,
        )
```

Note: `TelemetryStore.add_turn()` already calls `self.save()` internally, so no separate save call needed.

- [ ] **Step 9: Run all telemetry tests**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_framework.py::TestOrchestrator -v
```

Expected: All pass

- [ ] **Step 10: Commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add context_hacking/core/orchestrator.py context_hacking/core/telemetry.py tests/test_framework.py
git commit -m "feat: wire TelemetryStore into orchestrator with per-turn persistence"
```

---

### Task 2: Machine-Readable State Vector for Crash Recovery

**Files:**
- Modify: `context_hacking/core/memory.py`
- Test: `tests/test_framework.py`

The current `write_state_vector()` writes human-readable markdown. The `read_state_vector()` parses it back via regex on `KEY: value` lines. This works but we need it to be robust enough for crash recovery — the parsed dict must faithfully round-trip.

- [ ] **Step 1: Write failing test — state vector round-trip with all fields**

Add to `tests/test_framework.py` in `TestMemoryManager`:

```python
def test_state_vector_roundtrip_full(self, config_file):
    """State vector round-trips all fields needed for resume."""
    config = Config.from_yaml(config_file)
    mm = MemoryManager(config)
    mm.write_state_vector(
        turn=7,
        mode="EXPLORATION",
        milestone="Phase 2: Calibration",
        failures="tolerance_drift, grid_update, rng_seed",
        winning_params="tolerance=0.30, grid=50x50",
        metric_status="segregation_index=0.72",
        open_flags="none",
        last_tag="v0.3.1",
        next_focus="Calibrate tolerance sweep",
        grounding="aligned",
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
```

Note: `write_state_vector()` uses kwargs: `failures`, `winning_params`, `last_tag`, `next_focus`, `grounding` (not the full English names). The **kwargs approach means adding new keys (stagnation_streak, etc.) just requires updating the `fields` dict in the method body.

- [ ] **Step 2: Run test to verify it fails**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_framework.py::TestMemoryManager::test_state_vector_roundtrip_full -v
```

Expected: FAIL — `write_state_vector()` doesn't accept streak/anomaly kwargs, or they're not written/parsed.

- [ ] **Step 3: Extend write_state_vector to include orchestrator state**

In `memory.py`, modify the `fields` dict inside `write_state_vector()` to add the three new streak fields. The method already uses `**kwargs: str`, so just add three lines to the existing `fields` dict (after the `SCIENCE_GROUNDING` line):

```python
            "STAGNATION_STREAK": kwargs.get("stagnation_streak", "0"),
            "EXPLORATION_STREAK": kwargs.get("exploration_streak", "0"),
            "CONSECUTIVE_ANOMALIES": kwargs.get("consecutive_anomalies", "0"),
```

The rest of the method (header lines, iteration, write) stays unchanged.

- [ ] **Step 4: Run test to verify it passes**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_framework.py::TestMemoryManager -v
```

Expected: All pass (including existing tests — verify no regression)

- [ ] **Step 5: Commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add context_hacking/core/memory.py tests/test_framework.py
git commit -m "feat: extend state vector with streak counters for crash recovery"
```

---

### Task 3: Add --resume Flag to CLI and Orchestrator

**Files:**
- Modify: `context_hacking/cli.py`
- Modify: `context_hacking/core/orchestrator.py`
- Modify: `context_hacking/runner.py`
- Test: `tests/test_cli.py`

- [ ] **Step 1: Write failing test — CLI accepts --resume flag**

Add to `tests/test_cli.py`:

```python
class TestResume:
    def test_resume_flag_exists(self, runner):
        """run command accepts --resume flag."""
        result = runner.invoke(main, ["run", "--help"])
        assert "--resume" in result.output

    def test_resume_without_state_vector_errors(self, runner, tmp_path):
        """--resume without state_vector.md produces error."""
        import os
        os.chdir(tmp_path)
        result = runner.invoke(main, ["run", "--resume"])
        assert result.exit_code != 0 or "No state_vector" in result.output or "not found" in result.output
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_cli.py::TestResume -v
```

Expected: FAIL — `--resume` not recognized

- [ ] **Step 3: Add --resume flag to CLI run command**

In `cli.py`, modify the `run` command (around line 120):

```python
@main.command()
@click.option("--experiment", "-e", help="Built-in experiment to run")
@click.option("--method", type=click.Choice(["auto", "claude-cli", "api", "interactive"]),
              default="auto", help="Execution method")
@click.option("--resume", is_flag=True, default=False,
              help="Resume from last state_vector.md checkpoint")
@click.option("--all-experiments", is_flag=True, default=False, help="Run all built-in experiments")
@click.option("--dashboard", is_flag=True, default=False, help="Launch Streamlit dashboard alongside")
def run(experiment, method, resume, all_experiments, dashboard):
    """Launch the CHP loop."""
```

Add resume logic at the start of the run function body:

```python
    if resume:
        state_path = Path("state_vector.md")
        if not state_path.exists():
            click.echo("Error: No state_vector.md found. Cannot resume.", err=True)
            raise SystemExit(1)
        from context_hacking.core.memory import MemoryManager
        mm = MemoryManager(base_dir=Path("."))
        state = mm.read_state_vector()
        start_turn = int(state.get("TURN", "0")) + 1
        click.echo(f"Resuming from turn {start_turn} (mode: {state.get('MODE', 'VALIDATION')})")
        # Pass resume state to runner
        run_experiment(experiment or ".", method=method, resume_state=state)
        return
```

- [ ] **Step 4: Add resume_state parameter to run_experiment**

In `runner.py`, modify `run_experiment()` signature (around line 494):

```python
def run_experiment(name: str, method: str = "auto",
                   resume_state: dict | None = None) -> None:
```

Pass `resume_state` through to `_run_api_loop()`:

```python
    if method == "api":
        _run_api_loop(experiment_dir, config, resume_state=resume_state)
```

In `_run_api_loop()`, add resume handling at the start:

```python
def _run_api_loop(experiment_dir: Path, config: dict,
                  resume_state: dict | None = None) -> None:
    # ...existing setup...
    
    start_turn = 1
    if resume_state:
        start_turn = int(resume_state.get("TURN", "0")) + 1
        logger.info(f"Resuming from turn {start_turn}")
    
    for turn in range(start_turn, max_turns + 1):
        # ...existing loop body...
```

- [ ] **Step 5: Run tests**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_cli.py -v
```

Expected: All pass

- [ ] **Step 6: Commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add context_hacking/cli.py context_hacking/runner.py tests/test_cli.py
git commit -m "feat: add --resume flag for crash recovery from state_vector.md"
```

---

### Task 4: API Retry Logic with Exponential Backoff

**Files:**
- Modify: `context_hacking/runner.py`
- Test: `tests/test_runner.py`

The current `_run_api_loop()` makes Anthropic API calls (line ~136 of runner.py) with no retry logic. A single timeout kills the run.

- [ ] **Step 1: Write failing test — retry helper**

Add to `tests/test_runner.py`:

```python
from unittest.mock import patch, MagicMock
import anthropic

class TestRetryLogic:
    def test_retry_on_api_error(self):
        """API call retries on transient error."""
        from context_hacking.runner import _api_call_with_retry

        call_count = 0
        def flaky_call(**kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise anthropic.APIConnectionError(request=MagicMock())
            return MagicMock(content=[MagicMock(text="success")])

        result = _api_call_with_retry(flaky_call, max_retries=3, system="test", messages=[])
        assert call_count == 3
        assert result is not None

    def test_retry_exhausted_raises(self):
        """API call raises after max retries exhausted."""
        from context_hacking.runner import _api_call_with_retry

        def always_fail(**kwargs):
            raise anthropic.APIConnectionError(request=MagicMock())

        with pytest.raises(anthropic.APIConnectionError):
            _api_call_with_retry(always_fail, max_retries=3, system="test", messages=[])
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_runner.py::TestRetryLogic -v
```

Expected: FAIL — `ImportError: cannot import name '_api_call_with_retry'`

- [ ] **Step 3: Implement retry helper in runner.py**

Add to `runner.py`:

```python
import time
import anthropic

def _api_call_with_retry(call_fn, max_retries: int = 3,
                         base_delay: float = 1.0, **kwargs):
    """Call an API function with exponential backoff on transient errors.
    
    Args:
        call_fn: callable that accepts **kwargs and returns API response
        max_retries: max number of attempts
        base_delay: initial delay in seconds (doubled each retry)
        **kwargs: passed through to call_fn
    
    Returns:
        API response on success
    
    Raises:
        Last exception if all retries exhausted
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            return call_fn(**kwargs)
        except (anthropic.APIConnectionError, anthropic.RateLimitError,
                anthropic.APITimeoutError) as e:
            last_error = e
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                logger.warning(f"API error (attempt {attempt + 1}/{max_retries}), "
                             f"retrying in {delay:.0f}s: {e}")
                time.sleep(delay)
            else:
                logger.error(f"API error after {max_retries} attempts: {e}")
    raise last_error
```

- [ ] **Step 4: Wire retry into _run_api_loop**

Replace direct `client.messages.create()` calls in `_run_api_loop()` with:

```python
        response = _api_call_with_retry(
            client.messages.create,
            max_retries=3,
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages,
        )
```

- [ ] **Step 5: Run tests**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_runner.py -v
```

Expected: All pass

- [ ] **Step 6: Commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add context_hacking/runner.py tests/test_runner.py
git commit -m "feat: add exponential backoff retry for API calls in runner"
```

---

### Task 5: Context Window Management

**Files:**
- Modify: `context_hacking/runner.py`
- Test: `tests/test_runner.py`

When the messages list grows too large, the API call will fail. We need to detect this and summarize older turns.

- [ ] **Step 1: Write failing test — token estimation**

Add to `tests/test_runner.py`:

```python
class TestContextWindow:
    def test_estimate_tokens(self):
        """Token estimation returns reasonable count."""
        from context_hacking.runner import _estimate_tokens
        messages = [
            {"role": "user", "content": "Hello world"},
            {"role": "assistant", "content": "Hi there, how can I help?"},
        ]
        tokens = _estimate_tokens(messages)
        assert 5 < tokens < 50  # ~4 chars per token heuristic

    def test_summarize_old_turns(self):
        """Summarization compresses messages when over threshold."""
        from context_hacking.runner import _maybe_summarize_messages
        # Create messages that exceed threshold
        messages = []
        for i in range(50):
            messages.append({"role": "user", "content": f"Turn {i}: " + "x" * 1000})
            messages.append({"role": "assistant", "content": f"Response {i}: " + "y" * 1000})
        
        result = _maybe_summarize_messages(messages, max_tokens=10000)
        # Should be shorter than original
        assert len(result) < len(messages)
        # Last few messages preserved
        assert result[-1]["content"] == messages[-1]["content"]
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_runner.py::TestContextWindow -v
```

Expected: FAIL — functions don't exist

- [ ] **Step 3: Implement context window management**

Add to `runner.py`:

```python
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
        return messages  # Can't summarize further
    
    # Keep first message + last keep_recent
    first = messages[0]
    recent = messages[-keep_recent:]
    middle = messages[1:-keep_recent]
    
    # Build synopsis from middle messages
    turns_summarized = len(middle) // 2
    synopsis_parts = []
    for i in range(0, len(middle), 2):
        user_msg = middle[i].get("content", "")[:200]
        synopsis_parts.append(f"- Turn: {user_msg[:100]}...")
    
    synopsis = (f"[CONTEXT SUMMARY: {turns_summarized} earlier turns summarized to save context]\n"
                + "\n".join(synopsis_parts[:20]))  # Cap at 20 entries
    
    summary_msg = {"role": "user", "content": synopsis}
    
    result = [first, summary_msg] + recent
    logger.info(f"Context window management: {len(messages)} messages -> {len(result)} "
                f"(~{_estimate_tokens(result)} tokens, was ~{estimated})")
    return result
```

- [ ] **Step 4: Wire into _run_api_loop**

Before each API call in the loop, add:

```python
        messages = _maybe_summarize_messages(messages, max_tokens=150_000)
```

- [ ] **Step 5: Run tests**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_runner.py -v
```

Expected: All pass

- [ ] **Step 6: Commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add context_hacking/runner.py tests/test_runner.py
git commit -m "feat: context window management with automatic summarization at 150K tokens"
```

---

### Task 6: Emergency State Dump on Crash

**Files:**
- Modify: `context_hacking/runner.py`
- Modify: `context_hacking/core/orchestrator.py`
- Test: `tests/test_runner.py`

If anything crashes mid-run, we need to dump state so --resume can pick up.

- [ ] **Step 1: Write failing test**

```python
class TestEmergencyDump:
    def test_emergency_state_dump(self, tmp_path):
        """Emergency dump writes state vector on crash."""
        from context_hacking.core.orchestrator import Orchestrator, Config
        import yaml
        
        config_path = tmp_path / "config.yaml"
        config_path.write_text(yaml.dump({"project": {"name": "test"}}))
        (tmp_path / "state_vector.md").touch()
        (tmp_path / "innovation_log.md").touch()
        (tmp_path / "dead_ends.md").touch()
        
        config = Config.from_yaml(config_path)
        orch = Orchestrator(config)
        orch.turn = 5
        orch.emergency_state_dump()
        
        state = (tmp_path / "state_vector.md").read_text()
        assert "TURN: 5" in state
```

- [ ] **Step 2: Run test to verify it fails**

Expected: FAIL — no `emergency_state_dump` method

- [ ] **Step 3: Implement emergency_state_dump in orchestrator**

Add to `Orchestrator` class:

```python
    def emergency_state_dump(self) -> None:
        """Emergency state dump — called on unhandled exceptions."""
        try:
            self.memory.write_state_vector(
                turn=self.turn,
                mode=self.modes.current_mode,
                milestone="EMERGENCY_DUMP",
                open_flags="crashed — use --resume to continue",
                stagnation_streak=str(self.modes.stagnation_streak),
                exploration_streak=str(self.modes.exploration_streak),
                consecutive_anomalies=str(self.gates.consecutive_anomalies),
            )
            _log.error("Emergency state dumped at turn %d", self.turn)
        except Exception as e:
            _log.error("Failed to write emergency state: %s", e)
```

- [ ] **Step 4: Wire top-level try/except in runner**

In `_run_api_loop()`, wrap the main loop:

```python
    try:
        for turn in range(start_turn, max_turns + 1):
            # ...existing loop body...
    except KeyboardInterrupt:
        logger.info("Run interrupted by user")
        orchestrator.emergency_state_dump()
    except Exception as e:
        logger.error(f"Unhandled error at turn {orchestrator.turn}: {e}")
        orchestrator.emergency_state_dump()
        raise
```

- [ ] **Step 5: Run tests**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/ -v
```

Expected: All pass

- [ ] **Step 6: Commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add context_hacking/core/orchestrator.py context_hacking/runner.py tests/
git commit -m "feat: emergency state dump on crash for --resume recovery"
```

---

### Task 7: End-to-End Verification

- [ ] **Step 1: Run full test suite**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/ -v --tb=short
```

Expected: All tests pass

- [ ] **Step 2: Verify CLI --resume flag appears**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m context_hacking.cli run --help
```

Expected: Shows `--resume` flag in help output

- [ ] **Step 3: Verify telemetry wiring**

```bash
cd D:\EXPERIMENTS\context-hacking && python -c "
from context_hacking.core.orchestrator import Orchestrator, Config
from context_hacking.core.telemetry import TurnMetrics
import yaml, tempfile
from pathlib import Path

# Create minimal config
tmp = Path(tempfile.mkdtemp())
(tmp / 'config.yaml').write_text(yaml.dump({'project': {'name': 'test'}}))
(tmp / 'state_vector.md').touch()
(tmp / 'innovation_log.md').touch()
(tmp / 'dead_ends.md').touch()

config = Config.from_yaml(tmp / 'config.yaml')
orch = Orchestrator(config)
metrics = TurnMetrics(turn=1, tokens_total=1000, duration_seconds=5.0)
orch.record_turn_result(improved=True, anomaly=False, metrics=metrics)
print(f'Telemetry turns: {orch.telemetry.total_turns}')
print(f'Total tokens: {orch.telemetry.total_tokens}')
assert orch.telemetry.total_turns == 1
assert orch.telemetry.total_tokens == 1000
print('Phase 1 telemetry wiring: PASS')
"
```

- [ ] **Step 4: Verify retry helper**

```bash
cd D:\EXPERIMENTS\context-hacking && python -c "
from context_hacking.runner import _api_call_with_retry, _estimate_tokens, _maybe_summarize_messages
print('_api_call_with_retry: importable')
print(f'Token estimate for 1000 chars: {_estimate_tokens([{\"content\": \"x\" * 1000}])}')
msgs = [{'role': 'user', 'content': 'x' * 1000}] * 100
result = _maybe_summarize_messages(msgs, max_tokens=5000)
print(f'Summarized {len(msgs)} msgs -> {len(result)} msgs')
print('Phase 1 context management: PASS')
"
```

- [ ] **Step 5: Final commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add -A
git commit -m "feat: Phase 1 complete — core framework with telemetry, crash recovery, retry logic"
```
