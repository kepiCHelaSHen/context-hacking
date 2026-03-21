"""
CHP Experiment Runner — executes the full 9-layer protocol on any experiment.

This module reads the loop template, injects experiment-specific paths,
and drives the build cycle either via:
  1. Claude Code CLI (subprocess: claude --dangerously-skip-permissions)
  2. Anthropic API (direct API call with the loop prompt)
  3. Interactive mode (prints the prompt for manual paste)

Usage:
    from context_hacking.runner import run_experiment
    run_experiment("schelling-segregation", method="claude-cli")
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

_log = logging.getLogger(__name__)

PACKAGE_ROOT = Path(__file__).parent.parent
LOOP_TEMPLATE_PATH = PACKAGE_ROOT / "prompts" / "loop_template.md"


def _load_loop_prompt(experiment_dir: Path) -> str:
    """Load the loop template and inject experiment-specific paths."""
    if not LOOP_TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Loop template not found: {LOOP_TEMPLATE_PATH}")

    template = LOOP_TEMPLATE_PATH.read_text(encoding="utf-8")

    # Get experiment name from directory
    experiment_name = experiment_dir.name

    # Replace placeholders
    prompt = template.replace("{experiment_dir}", str(experiment_dir))
    prompt = template.replace("{experiment_dir}", str(experiment_dir))
    prompt = prompt.replace("{experiment_name}", experiment_name)

    return prompt


def run_experiment(
    experiment_name: str,
    method: str = "auto",
    project_dir: Path | None = None,
) -> None:
    """Run the full CHP loop on an experiment.

    Parameters
    ----------
    experiment_name:
        Name of the experiment (e.g., "schelling-segregation").
    method:
        "claude-cli" — pipe prompt to Claude Code CLI
        "api" — call Anthropic API directly
        "interactive" — write prompt to file for manual use
        "auto" — try claude-cli, fall back to interactive
    project_dir:
        Project root. Defaults to current directory.
    """
    if project_dir is None:
        project_dir = Path.cwd()

    # Find the experiment directory
    experiment_dir = project_dir / "experiments" / experiment_name
    if not experiment_dir.exists():
        # Try directly under project root
        experiment_dir = project_dir
        if not (experiment_dir / "frozen").exists():
            raise FileNotFoundError(
                f"Experiment not found: {experiment_name}. "
                f"Looked in {project_dir / 'experiments' / experiment_name} "
                f"and {project_dir}"
            )

    _log.info("Running CHP loop on: %s", experiment_name)
    _log.info("Experiment dir: %s", experiment_dir)

    # Load and inject the loop prompt
    prompt = _load_loop_prompt(experiment_dir)

    if method == "auto":
        method = _detect_method()

    if method == "claude-cli":
        _run_claude_cli(prompt, experiment_dir)
    elif method == "api":
        _run_api(prompt, experiment_dir)
    elif method == "interactive":
        _run_interactive(prompt, experiment_dir)
    else:
        raise ValueError(f"Unknown method: {method}")


def _detect_method() -> str:
    """Auto-detect the best available execution method."""
    # Check for Claude Code CLI
    try:
        result = subprocess.run(
            ["claude", "--version"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            _log.info("Detected Claude Code CLI: %s", result.stdout.strip())
            return "claude-cli"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Check for Anthropic API key
    if os.environ.get("ANTHROPIC_API_KEY"):
        _log.info("Detected ANTHROPIC_API_KEY — using API method")
        return "api"

    _log.info("No Claude CLI or API key found — falling back to interactive")
    return "interactive"


def _run_claude_cli(prompt: str, experiment_dir: Path) -> None:
    """Execute the loop via Claude Code CLI."""
    # Write prompt to a temp file and pipe it
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write(prompt)
        prompt_path = f.name

    _log.info("Launching Claude Code with loop prompt: %s", prompt_path)
    print(f"\n{'='*60}")
    print(f"CHP Loop starting via Claude Code CLI")
    print(f"Experiment: {experiment_dir.name}")
    print(f"Prompt: {prompt_path}")
    print(f"{'='*60}\n")

    try:
        subprocess.run(
            ["claude", "--dangerously-skip-permissions"],
            input=Path(prompt_path).read_text(encoding="utf-8"),
            text=True,
            cwd=str(experiment_dir.parent.parent),  # project root
        )
    finally:
        try:
            os.unlink(prompt_path)
        except OSError:
            pass


def _run_api(prompt: str, experiment_dir: Path) -> None:
    """Execute the loop via Anthropic API directly."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not set. Set it or use method='claude-cli'."
        )

    try:
        import anthropic
    except ImportError:
        raise ImportError("pip install anthropic — required for API method")

    _log.info("Launching CHP loop via Anthropic API")
    print(f"\n{'='*60}")
    print(f"CHP Loop starting via Anthropic API")
    print(f"Experiment: {experiment_dir.name}")
    print(f"{'='*60}\n")

    client = anthropic.Anthropic(api_key=api_key)

    # Read all context files for the experiment
    context_files = {}
    for name in ["CHAIN_PROMPT.md", "spec.md", "dead_ends.md",
                  "state_vector.md", "innovation_log.md", "config.yaml"]:
        fpath = experiment_dir / name
        if fpath.exists():
            context_files[name] = fpath.read_text(encoding="utf-8")

    # Read frozen spec
    frozen_dir = experiment_dir / "frozen"
    if frozen_dir.exists():
        for fp in frozen_dir.glob("*.md"):
            context_files[f"frozen/{fp.name}"] = fp.read_text(encoding="utf-8")

    # Build the full context message
    context_block = "\n\n".join(
        f"=== {name} ===\n{content}" for name, content in context_files.items()
    )

    full_prompt = f"{prompt}\n\n{'='*60}\nEXPERIMENT CONTEXT FILES\n{'='*60}\n\n{context_block}"

    # Call API with extended thinking for complex builds
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
        messages=[{"role": "user", "content": full_prompt}],
    )

    # Print and save the response
    output_text = response.content[0].text
    print(output_text)

    # Save to the experiment directory
    output_path = experiment_dir / "api_build_output.md"
    output_path.write_text(output_text, encoding="utf-8")
    _log.info("API response saved to: %s", output_path)


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
    print(f"  2. Copy-paste into Claude.ai or Cursor")
    print(f"  3. Set ANTHROPIC_API_KEY and run: chp run --method api")
    print(f"\nThe dashboard will show live progress:")
    print(f"  chp dashboard")
    print()
