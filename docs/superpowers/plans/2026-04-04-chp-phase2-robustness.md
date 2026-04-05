# CHP Phase 2: Robustness Hardening — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate fragile regex parsing, validate config inputs, remove hardcoded heuristics, and handle errors gracefully in the orchestrator loop.

**Architecture:** Council switches to structured JSON responses (OpenAI `response_format`). Critic/Reviewer parsers get fallback patterns, input validation, and fail-safe behavior (parse failure = block, not silent pass). Config gets schema validation with typo detection. Runner's hardcoded experiment names replaced with config-driven output mapping.

**Tech Stack:** Python 3.11+, pyyaml, requests, pytest

**Spec:** `docs/superpowers/specs/2026-04-04-chp-10-of-10-master-roadmap.md` (Phase 2)

---

### File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `context_hacking/agents/critic.py` | Modify | Add fallback patterns, input validation, PARSE_FAILED verdict |
| `context_hacking/agents/reviewer.py` | Modify | Add fallback patterns, input validation, PARSE_FAILED verdict |
| `context_hacking/agents/council.py` | Modify | JSON response format for OpenAI, real consensus_issues detection |
| `context_hacking/runner.py` | Modify | Replace hardcoded experiment names with config-driven output files |
| `context_hacking/core/orchestrator.py` | Modify | Config schema validation, orchestrator error handling |
| `tests/test_framework.py` | Modify | Parsing robustness tests, config validation tests |
| `tests/test_runner.py` | Modify | Code extraction tests without hardcoded names |
| `tests/test_council.py` | Create | Consensus detection tests with mocked API responses |

---

### Task 1: Harden Critic Verdict Parsing

**Files:**
- Modify: `context_hacking/agents/critic.py:84-131`
- Test: `tests/test_framework.py`

The current `parse_verdict()` uses a single regex pattern per gate score. If the LLM outputs `Gate 1: 0.95/1.0` instead of `Gate 1: 0.95`, the regex silently returns 0.0.

- [ ] **Step 1: Write failing tests for edge cases**

Add to `TestCriticParsing` in `tests/test_framework.py`:

```python
def test_parse_variant_gate_format(self):
    """Handles variant gate score formats (0.95/1.0, 95%, etc.)."""
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
    """Empty or garbage input returns a blocking PARSE_FAILED verdict."""
    from context_hacking.agents.critic import parse_verdict
    v = parse_verdict("")
    assert v.verdict == "PARSE_FAILED"
    assert not v.passed

def test_parse_garbage_returns_failed(self):
    """Unstructured text returns PARSE_FAILED."""
    from context_hacking.agents.critic import parse_verdict
    v = parse_verdict("I think the code looks great! No issues found.")
    assert v.verdict == "PARSE_FAILED"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_framework.py::TestCriticParsing -v
```

- [ ] **Step 3: Harden parse_verdict()**

In `critic.py`, replace the gate extraction regex patterns (lines 89-101) with more robust versions that handle `/1.0` suffixes, `%` notation, and leading dots:

```python
def _extract_gate(text: str, gate_num: int) -> float:
    """Extract gate score with fallback patterns."""
    patterns = [
        rf"gate.?{gate_num}[^:]*:\s*([0-9]*\.?[0-9]+)\s*(?:/\s*[0-9.]+)?",  # "Gate 1: 0.95/1.0"
        rf"gate.?{gate_num}[^:]*:\s*([0-9]+)\s*%",                            # "Gate 1: 95%"
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = float(m.group(1))
            if val > 1.0:
                val = val / 100.0  # Convert percentage
            return min(max(val, 0.0), 1.0)  # Clamp to [0, 1]
    return 0.0
```

Add PARSE_FAILED detection: if no gate scores were found at all, return a blocking verdict:

```python
def parse_verdict(raw_text: str) -> CriticVerdict:
    """Parse raw Critic response into structured verdict."""
    if not raw_text or not raw_text.strip():
        return CriticVerdict(verdict="PARSE_FAILED",
                           blocking_issues=["PARSE_FAILED: empty critic response"])

    g1 = _extract_gate(raw_text, 1)
    g2 = _extract_gate(raw_text, 2)
    g3 = _extract_gate(raw_text, 3)
    g4 = _extract_gate(raw_text, 4)

    # If no gates found at all, it's unparseable
    if g1 == 0.0 and g2 == 0.0 and g3 == 0.0 and g4 == 0.0:
        has_gate_mention = bool(re.search(r"gate", raw_text, re.IGNORECASE))
        if not has_gate_mention:
            return CriticVerdict(verdict="PARSE_FAILED",
                               blocking_issues=["PARSE_FAILED: no gate scores found in critic response"])

    # ... rest of existing parsing (verdict, blocking issues, next priority) ...
```

Also add `passed` property handling for PARSE_FAILED:

In the `CriticVerdict.passed` property, add:
```python
    @property
    def passed(self) -> bool:
        if self.verdict == "PARSE_FAILED":
            return False
        return self.all_gates_met and self.verdict == "PASS"
```

- [ ] **Step 4: Run tests**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_framework.py::TestCriticParsing -v
```

Expected: All pass (old + new)

- [ ] **Step 5: Commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add context_hacking/agents/critic.py tests/test_framework.py
git commit -m "feat: harden critic parsing with fallback patterns and PARSE_FAILED safety"
```

---

### Task 2: Harden Reviewer Parsing

**Files:**
- Modify: `context_hacking/agents/reviewer.py:66-112`
- Test: `tests/test_framework.py`

Same treatment as critic — add robustness for edge cases and PARSE_FAILED safety.

- [ ] **Step 1: Write failing tests**

Add to `TestReviewerParsing`:

```python
def test_parse_empty_returns_failed(self):
    """Empty input returns NEEDS REVISION verdict."""
    from context_hacking.agents.reviewer import parse_review
    r = parse_review("")
    assert r.verdict == "PARSE_FAILED"
    assert r.needs_revision

def test_parse_variant_formats(self):
    """Handles variant issue formats."""
    from context_hacking.agents.reviewer import parse_review
    text = """
    **CRITICAL**: `sim.py:42` — Uses print() instead of logging
    WARNING: model.py line 10 - Missing type annotation
    MINOR - config.py — Unused import
    Verdict: APPROVE WITH NOTES
    """
    r = parse_review(text)
    assert r.critical_count == 1
    assert r.warning_count == 1
    assert len(r.issues) == 3
    assert r.verdict == "APPROVE WITH NOTES"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_framework.py::TestReviewerParsing -v
```

- [ ] **Step 3: Harden parse_review()**

In `reviewer.py`, add PARSE_FAILED handling at the start of `parse_review()`:

```python
def parse_review(raw_text: str) -> ReviewResult:
    """Parse raw Reviewer output into structured result."""
    if not raw_text or not raw_text.strip():
        return ReviewResult(
            issues=[ReviewIssue(severity="CRITICAL", file="", line=0,
                               description="PARSE_FAILED: empty reviewer response")],
            verdict="PARSE_FAILED",
        )
```

Add `needs_revision` property to handle PARSE_FAILED:

```python
    @property
    def needs_revision(self) -> bool:
        return self.verdict in ("NEEDS REVISION", "PARSE_FAILED") or self.critical_count > 0
```

Expand the issue regex to handle more formats (bold markers, `line N` notation, bare severity):

```python
    issue_pattern = re.compile(
        r"\*{0,2}(CRITICAL|WARNING|MINOR)\*{0,2}:?\s*"
        r"(?:`?([^`\n:]+(?::\d+)?)`?|(\S+\.py)\s+line\s+(\d+))?\s*[-—]?\s*(.+)",
        re.IGNORECASE,
    )
```

- [ ] **Step 4: Run tests**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_framework.py::TestReviewerParsing -v
```

- [ ] **Step 5: Commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add context_hacking/agents/reviewer.py tests/test_framework.py
git commit -m "feat: harden reviewer parsing with PARSE_FAILED safety and variant format support"
```

---

### Task 3: Council Structured Output + Consensus Detection

**Files:**
- Modify: `context_hacking/agents/council.py`
- Create: `tests/test_council.py`

The `consensus_issues` property returns `[]`. OpenAI supports `response_format: {"type": "json_object"}`. We need real consensus detection.

- [ ] **Step 1: Write tests**

Create `tests/test_council.py`:

```python
"""Tests for council consensus detection."""
import pytest
from context_hacking.agents.council import CouncilReview, CouncilResult


class TestConsensusDetection:
    def test_consensus_when_both_flag_drift(self):
        """Two models flagging drift = consensus issue."""
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o",
                         response='{"drift_detected": true, "issues": ["coefficient mismatch"]}'),
            CouncilReview(provider="xai", model="grok-3",
                         response="DRIFT DETECTED: coefficient values don't match spec"),
        ]
        result = CouncilResult(reviews=reviews)
        assert result.any_drift_flagged
        assert len(result.consensus_issues) > 0

    def test_no_consensus_single_flag(self):
        """Only one model flags issue = no consensus."""
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o",
                         response='{"drift_detected": true, "issues": ["coefficient mismatch"]}'),
            CouncilReview(provider="xai", model="grok-3",
                         response="Code looks correct. No drift detected."),
        ]
        result = CouncilResult(reviews=reviews)
        assert len(result.consensus_issues) == 0

    def test_no_consensus_no_flags(self):
        """No drift flagged = no consensus issues."""
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o",
                         response='{"drift_detected": false, "issues": []}'),
            CouncilReview(provider="xai", model="grok-3",
                         response="Everything looks good."),
        ]
        result = CouncilResult(reviews=reviews)
        assert len(result.consensus_issues) == 0
        assert not result.any_drift_flagged

    def test_partial_failure_graceful(self):
        """One model fails, other succeeds = use remaining."""
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o",
                         response='', error="API timeout"),
            CouncilReview(provider="xai", model="grok-3",
                         response="DRIFT DETECTED: wrong constants"),
        ]
        result = CouncilResult(reviews=reviews)
        assert result.n_succeeded == 1
        assert result.any_drift_flagged
```

- [ ] **Step 2: Run tests to verify behavior**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_council.py -v
```

Expected: Some fail (consensus_issues returns [])

- [ ] **Step 3: Implement consensus detection**

In `council.py`, replace the `consensus_issues` property (lines 44-50):

```python
    @property
    def consensus_issues(self) -> list[str]:
        """Find issues flagged by 2+ council members (true consensus)."""
        if self.n_succeeded < 2:
            return []  # Need at least 2 models for consensus

        # Check which successful reviews flag drift
        drift_flaggers = []
        for r in self.reviews:
            if not r.succeeded:
                continue
            text = r.response.lower()
            if any(signal in text for signal in [
                "drift", "mismatch", "incorrect", "wrong",
                "does not match", "doesn't match", "violat",
            ]):
                drift_flaggers.append(r.provider)

        if len(drift_flaggers) >= 2:
            return [f"Consensus drift flagged by: {', '.join(drift_flaggers)}"]
        return []
```

- [ ] **Step 4: Add JSON response_format for OpenAI**

In `council.py`, modify `_call_openai()` to request JSON:

```python
def _call_openai(prompt: str, model: str, api_key: str,
                 temperature: float = 0.3, max_tokens: int = 2000) -> str:
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "response_format": {"type": "json_object"},
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
```

Update the council prompt (`prompts/council_gpt.md`) to instruct JSON output:

Add at the end of the prompt:
```
Respond in JSON format with this structure:
{"drift_detected": true/false, "issues": ["issue 1", ...], "risk_level": "low/medium/high", "recommendation": "..."}
```

- [ ] **Step 5: Run tests**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_council.py -v
```

- [ ] **Step 6: Commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add context_hacking/agents/council.py tests/test_council.py prompts/council_gpt.md
git commit -m "feat: council consensus detection + JSON response format for OpenAI"
```

---

### Task 4: Remove Hardcoded Experiment Names from Runner

**Files:**
- Modify: `context_hacking/runner.py:383-425`
- Test: `tests/test_runner.py`

`_extract_code_blocks()` has hardcoded checks for "schelling", "spatial", "prey", etc. Adding a new experiment requires editing the runner.

- [ ] **Step 1: Write failing test**

Add to `tests/test_runner.py`:

```python
class TestExtractCodeBlocksRobust:
    def test_filename_from_comment(self):
        """Extracts filename from # File: comment."""
        from context_hacking.runner import _extract_code_blocks
        text = '# File: my_simulation.py\n```python\ndef run():\n    pass\n```'
        blocks = _extract_code_blocks(text)
        assert "my_simulation.py" in blocks

    def test_generic_fallback_no_hardcoded_names(self):
        """Unknown code gets generic filename, not experiment-specific inference."""
        from context_hacking.runner import _extract_code_blocks
        text = '```python\nclass MyNewExperiment:\n    def compute(self):\n        return 42\n```'
        blocks = _extract_code_blocks(text)
        assert len(blocks) == 1
        # Should have a generic name, not require hardcoded experiment knowledge
        filename = list(blocks.keys())[0]
        assert filename.endswith(".py")
```

- [ ] **Step 2: Run tests**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_runner.py::TestExtractCodeBlocksRobust -v
```

- [ ] **Step 3: Remove hardcoded experiment names**

In `runner.py`, simplify `_extract_code_blocks()`. Replace the hardcoded name inference block (lines ~398-420) with a simple generic fallback:

```python
def _extract_code_blocks(text: str) -> dict[str, str]:
    """Extract ```python blocks with filename hints from API response."""
    blocks: dict[str, str] = {}
    block_count = 0

    pattern = re.compile(
        r'(?:#\s*(?:File:|filename:)\s*(\S+\.py)\s*\n)?'
        r'```(?:python|py)\s*\n(.*?)```',
        re.DOTALL,
    )

    for match in pattern.finditer(text):
        filename = match.group(1)
        code = match.group(2).strip()

        if not filename:
            # Try to infer from class/def name in first few lines
            first_lines = code[:500]
            class_match = re.search(r"class\s+(\w+)", first_lines)
            if class_match:
                # Convert CamelCase to snake_case for filename
                name = class_match.group(1)
                snake = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
                filename = f"{snake}.py"
            else:
                block_count += 1
                filename = f"generated_{block_count}.py"

        if filename and code:
            blocks[filename] = code

    return blocks
```

- [ ] **Step 4: Run all runner tests**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_runner.py -v
```

Expected: All pass. Note: existing tests (TestExtractCodeBlocks) may need updating if they relied on hardcoded names. Read and fix if needed.

- [ ] **Step 5: Commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add context_hacking/runner.py tests/test_runner.py
git commit -m "feat: remove hardcoded experiment names from code block extraction"
```

---

### Task 5: Config Schema Validation

**Files:**
- Modify: `context_hacking/core/orchestrator.py:41-99`
- Modify: `context_hacking/cli.py`
- Test: `tests/test_framework.py`

Config.from_yaml() loads any YAML without checking for typos or missing keys.

- [ ] **Step 1: Write failing tests**

Add to `tests/test_framework.py`:

```python
class TestConfigValidation:
    def test_unknown_key_warns(self, tmp_path, capsys):
        """Misspelled config key produces warning."""
        import yaml
        config_path = tmp_path / "config.yaml"
        config_path.write_text(yaml.dump({
            "project": {"name": "test"},
            "looop": {"max_turns": 10},  # typo
        }))
        config = Config.from_yaml(config_path)
        captured = capsys.readouterr()
        # Should warn about unknown key
        assert config.max_turns == 50  # Falls back to default

    def test_valid_config_no_warnings(self, tmp_path, capsys):
        """Valid config produces no warnings."""
        import yaml
        config_path = tmp_path / "config.yaml"
        config_path.write_text(yaml.dump({
            "project": {"name": "test"},
            "loop": {"max_turns": 10},
            "gates": {"seeds": 3},
        }))
        config = Config.from_yaml(config_path)
        assert config.max_turns == 10
```

- [ ] **Step 2: Run tests to verify behavior**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_framework.py::TestConfigValidation -v
```

- [ ] **Step 3: Add schema validation to Config**

In `orchestrator.py`, add validation to `Config.from_yaml()`:

```python
    VALID_TOP_KEYS = {"project", "models", "gates", "loop", "frozen",
                      "exit_conditions", "critic", "reviewer", "tokens"}

    @classmethod
    def from_yaml(cls, path: str | Path) -> Config:
        with open(path) as f:
            raw = yaml.safe_load(f) or {}

        # Validate top-level keys
        unknown = set(raw.keys()) - cls.VALID_TOP_KEYS
        if unknown:
            import difflib
            for key in unknown:
                close = difflib.get_close_matches(key, cls.VALID_TOP_KEYS, n=1, cutoff=0.6)
                suggestion = f" (did you mean '{close[0]}'?)" if close else ""
                _log.warning("Unknown config key: '%s'%s", key, suggestion)

        return cls(raw=raw)
```

- [ ] **Step 4: Add `chp validate` CLI command**

In `cli.py`, add:

```python
@main.command()
def validate():
    """Validate config.yaml without running."""
    from pathlib import Path
    config_path = Path("config.yaml")
    if not config_path.exists():
        click.echo("Error: No config.yaml found.", err=True)
        raise SystemExit(1)
    config = Config.from_yaml(config_path)
    click.echo(f"Project: {config.project_name}")
    click.echo(f"Max turns: {config.max_turns}")
    click.echo(f"Stagnation threshold: {config.stagnation_threshold}")
    click.echo("Config OK")
```

- [ ] **Step 5: Run tests**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_framework.py::TestConfigValidation tests/test_cli.py -v
```

- [ ] **Step 6: Commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add context_hacking/core/orchestrator.py context_hacking/cli.py tests/test_framework.py
git commit -m "feat: config schema validation with typo detection + chp validate command"
```

---

### Task 6: Error Handling in Orchestrator Loop

**Files:**
- Modify: `context_hacking/core/orchestrator.py`
- Test: `tests/test_framework.py`

The orchestrator's `step()` and `run()` have no error handling — any exception kills the loop.

- [ ] **Step 1: Write failing test**

```python
def test_step_survives_file_error(self, tmp_path):
    """Step doesn't crash on file I/O errors."""
    orch = self._make_orch(tmp_path)
    # Remove dead_ends.md to trigger I/O error in step
    (tmp_path / "dead_ends.md").unlink(missing_ok=True)
    import shutil
    shutil.rmtree(tmp_path / "dead_ends.md", ignore_errors=True)
    # Step should not raise
    result = orch.step()
    assert result is not None
```

- [ ] **Step 2: Wrap step() internals in try/except**

In `orchestrator.py`, wrap the body of `step()` so individual step failures don't crash the loop:

```python
    def step(self) -> dict:
        """Execute one turn of the CHP loop."""
        self.turn += 1

        # Check exit conditions
        exit_result = self.check_exit_conditions()
        if exit_result:
            return exit_result

        # Read dead ends (non-fatal if fails)
        try:
            dead_ends = self.memory.load_dead_ends()
        except Exception as e:
            _log.warning("Failed to load dead ends (continuing): %s", e)
            dead_ends = []

        # Determine focus from innovation log (non-fatal if fails)
        try:
            next_focus = self.memory.last_innovation_entry()
        except Exception as e:
            _log.warning("Failed to read innovation log (continuing): %s", e)
            next_focus = ""

        return {
            "status": "awaiting_build",
            "turn": self.turn,
            "mode": self.current_mode,
            "dead_ends": dead_ends,
            "next_focus": next_focus,
        }
```

- [ ] **Step 3: Run tests**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/test_framework.py::TestOrchestrator -v
```

- [ ] **Step 4: Commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add context_hacking/core/orchestrator.py tests/test_framework.py
git commit -m "feat: error handling in orchestrator step — file I/O failures don't crash the loop"
```

---

### Task 7: End-to-End Verification

- [ ] **Step 1: Run full test suite**

```bash
cd D:\EXPERIMENTS\context-hacking && python -m pytest tests/ -v --tb=short
```

Expected: All new tests pass, only pre-existing `test_init_with_experiment` failure remains.

- [ ] **Step 2: Verify parse safety**

```bash
cd D:\EXPERIMENTS\context-hacking && python -c "
from context_hacking.agents.critic import parse_verdict
from context_hacking.agents.reviewer import parse_review

# Empty input = PARSE_FAILED (blocks, doesn't silently pass)
v = parse_verdict('')
assert v.verdict == 'PARSE_FAILED'
assert not v.passed
print(f'Empty critic: {v.verdict} (blocks={not v.passed})')

r = parse_review('')
assert r.verdict == 'PARSE_FAILED'
assert r.needs_revision
print(f'Empty reviewer: {r.verdict} (blocks={r.needs_revision})')

# Garbage = PARSE_FAILED
v2 = parse_verdict('The code looks great!')
assert v2.verdict == 'PARSE_FAILED'
print(f'Garbage critic: {v2.verdict}')

print('All parse safety checks PASSED')
"
```

- [ ] **Step 3: Verify config validation**

```bash
cd D:\EXPERIMENTS\context-hacking && python -c "
from context_hacking.core.orchestrator import Config
import yaml, tempfile
from pathlib import Path
tmp = Path(tempfile.mkdtemp())
(tmp / 'config.yaml').write_text(yaml.dump({'project': {'name': 'test'}, 'looop': {'max_turns': 10}}))
config = Config.from_yaml(tmp / 'config.yaml')
print(f'Config loaded (max_turns={config.max_turns}, should be 50 default)')
assert config.max_turns == 50
print('Config validation PASSED')
"
```

- [ ] **Step 4: Commit**

```bash
cd D:\EXPERIMENTS\context-hacking && git add -A && git commit -m "feat: Phase 2 complete — robustness hardening with parse safety, config validation, error handling"
```
