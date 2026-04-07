"""
CHP Command Line Interface.

Commands:
  chp init <name>  — Create a new CHP project skeleton
  chp run          — Launch the orchestrator loop
  chp status       — Show current turn, mode, gates, dead ends
  chp export-paper — Generate a structured paper appendix
  chp cursor       — Generate .cursorrules + skills/ for Cursor integration
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()

# Path to the package's bundled templates
PACKAGE_ROOT = Path(__file__).parent
REPO_ROOT = PACKAGE_ROOT.parent
TEMPLATE_DIR = REPO_ROOT


@click.group()
@click.version_option(package_name="context-hacking")
def main() -> None:
    """Context Hacking Protocol — anti-drift framework for LLM science."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


@main.command()
@click.argument("name")
@click.option("--experiment", type=click.Choice(
    ["schelling", "spatial-pd", "lotka-volterra", "sir",
     "ml-hyperparam", "lorenz", "quantum-grover", "izhikevich", "blockchain"],
    case_sensitive=False,
), help="Initialize with a built-in showcase experiment")
@click.option("--existing", is_flag=True, help="Init in existing project directory")
@click.option("--cursor", is_flag=True, help="Also generate Cursor rules")
def init(name: str, experiment: str | None, existing: bool, cursor: bool) -> None:
    """Create a new CHP project skeleton."""
    target = Path(name) if not existing else Path(".")

    if not existing:
        target.mkdir(parents=True, exist_ok=True)

    # Copy template files
    templates = [
        "config.yaml",
        "CHAIN_PROMPT.md",
        "innovation_log.md",
        "dead_ends.md",
        "state_vector.md",
    ]
    for t in templates:
        src = TEMPLATE_DIR / t
        dst = target / t
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)

    # Create directories
    for d in ["frozen", "prompts", ".chp"]:
        (target / d).mkdir(parents=True, exist_ok=True)

    # Copy prompt templates
    prompts_src = TEMPLATE_DIR / "prompts"
    if prompts_src.exists():
        for p in prompts_src.glob("*.md"):
            dst = target / "prompts" / p.name
            if not dst.exists():
                shutil.copy2(p, dst)

    # Copy experiment if specified
    if experiment:
        exp_map = {
            "schelling": "schelling-segregation",
            "spatial-pd": "spatial-prisoners-dilemma",
            "lotka-volterra": "lotka-volterra",
            "sir": "sir-epidemic",
            "ml-hyperparam": "ml-hyperparam-search",
            "lorenz": "lorenz-attractor",
            "quantum-grover": "quantum-grover",
            "izhikevich": "izhikevich-neurons",
            "blockchain": "blockchain-consensus",
        }
        exp_name = exp_map.get(experiment, experiment)
        exp_src = REPO_ROOT / ".archive" / "experiment-old" / exp_name
        if exp_src.exists():
            exp_dst = target / "experiments" / exp_name
            shutil.copytree(exp_src, exp_dst, dirs_exist_ok=True)
            console.print(f"[green]Experiment loaded:[/green] {exp_name}")
        else:
            console.print(f"[yellow]Experiment template not found:[/yellow] {exp_name}")

    # Cursor rules
    if cursor:
        _generate_cursor_rules(target)

    # .gitignore
    gitignore = target / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(".chp/\n__pycache__/\n*.pyc\n.env\n")

    console.print(f"[bold green]CHP project initialized:[/bold green] {target.resolve()}")
    console.print("Next steps:")
    console.print("  1. Edit config.yaml with your project details")
    console.print("  2. Edit CHAIN_PROMPT.md with your design decisions")
    console.print("  3. Put your frozen code in frozen/")
    console.print("  4. Run: chp run")


@main.command()
@click.option("--experiment", default=None,
              help="Run a specific experiment (e.g., schelling-segregation)")
@click.option("--method", type=click.Choice(["auto", "claude-cli", "api", "interactive"]),
              default="auto", help="Execution method for the loop")
@click.option("--all-experiments", is_flag=True,
              help="Run all 9 built-in experiments sequentially")
@click.option("--dashboard", is_flag=True,
              help="Launch live WebSocket dashboard (for CHP-TETRIS-AI)")
@click.option("--resume", is_flag=True, default=False,
              help="Resume from last state_vector.md checkpoint")
@click.option("--dry-run", is_flag=True, default=False,
              help="Show execution plan without running (no API calls)")
@click.option("--verbose", is_flag=True, default=False,
              help="Enable debug-level logging")
def run(
    experiment: str | None, method: str, all_experiments: bool,
    dashboard: bool, resume: bool, dry_run: bool, verbose: bool,
) -> None:
    """Launch the CHP loop — builds, critiques, tests, and reports autonomously."""
    if verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)
        click.echo("Verbose mode: debug logging enabled")

    if dry_run:
        from pathlib import Path

        from context_hacking.core.orchestrator import Config
        config_path = Path("config.yaml")
        if config_path.exists():
            config = Config.from_yaml(config_path)
        else:
            config = None

        click.echo("=== CHP Dry Run — Execution Plan ===")
        click.echo(f"Project: {config.project_name if config else 'unknown'}")
        click.echo(f"Max turns: {config.max_turns if config else 50}")
        click.echo(f"Stagnation threshold: {config.stagnation_threshold if config else 5}")
        click.echo(f"Method: {method}")
        click.echo()
        click.echo("16-Step Turn Cycle:")
        click.echo("  1. Check exit conditions (5 kill-switches)")
        click.echo("  2. Subagent health checks (3-line confirmations)")
        click.echo("  3. Choose mode (VALIDATION or EXPLORATION)")
        click.echo("  4. Dead end check (read dead_ends.md)")
        click.echo("  5. Determine build target (from innovation log)")
        click.echo("  6. Council review (before build in Validation)")
        click.echo("  7. Grounding (citation or hypothesis)")
        click.echo("  8. BUILD via Builder agent")
        click.echo("  9. Self-critique (Builder reviews own work)")
        click.echo("  10. Critic review (hard blocker in Validation)")
        click.echo("  11. Code Reviewer (hygiene check)")
        click.echo("  12. Council (post-build review in Exploration)")
        click.echo("  13. Multi-seed anomaly detection (sigma-gates)")
        click.echo("  14. Metric improvement tracking")
        click.echo("  15. Commit and log (innovation log + state vector)")
        click.echo("  16. Session memory update")
        click.echo()
        click.echo("No API calls made. Exiting.")
        return

    resume_state = None
    if resume:
        from pathlib import Path as _Path
        state_path = _Path("state_vector.md")
        if not state_path.exists():
            click.echo("Error: No state_vector.md found. Cannot resume.", err=True)
            raise SystemExit(1)
        from context_hacking.core.memory import MemoryManager
        from context_hacking.core.orchestrator import Config
        config_path = _Path("config.yaml")
        if config_path.exists():
            config = Config.from_yaml(config_path)
            mm = MemoryManager(config)
        else:
            click.echo("Error: No config.yaml found. Cannot resume.", err=True)
            raise SystemExit(1)
        resume_state = mm.read_state_vector()
        start_turn = int(resume_state.get("TURN", "0")) + 1
        mode = resume_state.get('MODE', 'VALIDATION')
        click.echo(f"Resuming from turn {start_turn} (mode: {mode})")

    if dashboard and experiment:
        exp_dir = Path.cwd() / "experiments" / experiment
        server_module = exp_dir / "server.py"
        if server_module.exists():
            import subprocess
            import sys
            port = 8080
            # Try to read port from experiment config
            config_path = exp_dir / "config.yaml"
            if config_path.exists():
                import yaml
                with open(config_path) as f:
                    cfg = yaml.safe_load(f) or {}
                port = cfg.get("dashboard", {}).get("port", 8080)

            console.print(f"[bold green]Launching CHP Dashboard[/bold green] on port {port}")
            console.print(f"  Experiment: {experiment}")
            console.print(f"  Dashboard:  http://localhost:{port}")
            console.print()

            import webbrowser
            webbrowser.open(f"http://localhost:{port}")

            subprocess.run(
                [sys.executable, "-m", "uvicorn", "server:app",
                 "--host", "127.0.0.1", "--port", str(port)],
                cwd=str(exp_dir),
            )
            return

    from context_hacking.runner import run_experiment

    config_path = Path("config.yaml")
    if not config_path.exists():
        console.print("[red]config.yaml not found.[/red] Run 'chp init' first.")
        raise SystemExit(1)

    if all_experiments:
        exp_names = [
            "schelling-segregation", "spatial-prisoners-dilemma",
            "lotka-volterra", "sir-epidemic", "ml-hyperparam-search",
            "lorenz-attractor", "quantum-grover", "izhikevich-neurons",
            "blockchain-consensus",
        ]
        console.print(f"[bold]Running ALL {len(exp_names)} experiments[/bold]")
        for i, name in enumerate(exp_names, 1):
            console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
            console.print(f"[bold cyan]  [{i}/{len(exp_names)}] {name}[/bold cyan]")
            console.print(f"[bold cyan]{'='*60}[/bold cyan]\n")
            try:
                run_experiment(name, method=method)
            except Exception as e:
                console.print(f"[red]FAILED: {name} — {e}[/red]")
        console.print(f"\n[bold green]All {len(exp_names)} experiments complete.[/bold green]")
        return

    if experiment:
        # Run specific experiment through the full loop
        console.print(f"[bold]CHP Loop starting:[/bold] {experiment}")
        console.print(f"  Method: {method}")
        console.print()
        run_experiment(experiment, method=method, resume_state=resume_state)
        return

    # Default: detect experiment from config.yaml and run it
    import yaml
    with open(config_path) as f:
        cfg = yaml.safe_load(f) or {}
    project_name = cfg.get("project", {}).get("name", "")

    if project_name and project_name != "my-project":
        console.print(f"[bold]CHP Loop starting:[/bold] {project_name}")
        console.print(f"  Method: {method}")
        console.print()
        run_experiment(project_name, method=method, resume_state=resume_state)
    else:
        # Fallback: just do one orchestrator step (original behavior)
        from context_hacking.core.orchestrator import Config, Orchestrator
        config = Config.from_yaml(config_path)
        orch = Orchestrator(config)
        console.print(f"[bold]CHP Loop starting:[/bold] {config.project_name}")
        console.print(f"  Max turns: {config.max_turns}")
        console.print(f"  Mode: {orch.current_mode}")
        console.print()
        result = orch.step()
        if "exit" in result:
            console.print(f"[bold red]EXIT:[/bold red] {result['exit']}")
        else:
            console.print(f"[bold]Turn {result['turn']}[/bold] — Mode: {result['mode']}")
            console.print(f"  Dead ends avoided: {result['dead_ends_avoided'] or 'none'}")
            console.print()
            console.print(
                "[dim]Tip: use --experiment <name> to run the"
                " full autonomous loop.[/dim]"
            )


@main.command()
def status() -> None:
    """Show current CHP status."""
    from context_hacking.core.memory import MemoryManager
    from context_hacking.core.orchestrator import Config

    config_path = Path("config.yaml")
    if not config_path.exists():
        console.print("[red]config.yaml not found.[/red] Run 'chp init' first.")
        raise SystemExit(1)

    config = Config.from_yaml(config_path)
    memory = MemoryManager(config)

    # Read state vector
    sv = memory.read_state_vector()
    dead_ends = memory.load_dead_ends()
    last_focus = memory.last_innovation_entry()

    table = Table(title=f"CHP Status: {config.project_name}")
    table.add_column("Field", style="bold")
    table.add_column("Value")

    table.add_row("Turn", sv.get("TURN", "0"))
    table.add_row("Mode", sv.get("MODE", "VALIDATION"))
    table.add_row("Milestone", sv.get("MILESTONE", "not started"))
    table.add_row("Open flags", sv.get("OPEN_FLAGS", "none"))
    table.add_row("Dead ends", str(len(dead_ends)))
    table.add_row("Last tag", sv.get("LAST_PASSING_TAG", "none"))
    table.add_row("Next focus", sv.get("NEXT_TURN_FOCUS", last_focus or "begin"))

    console.print(table)

    if dead_ends:
        console.print("\n[bold]Dead ends:[/bold]")
        for de in dead_ends:
            console.print(f"  [red]x[/red] {de}")


@main.command(name="export-paper")
def export_paper() -> None:
    """Generate a structured paper appendix from CHP artifacts."""
    from context_hacking.core.memory import MemoryManager
    from context_hacking.core.orchestrator import Config

    config = Config.from_yaml("config.yaml")
    memory = MemoryManager(config)

    output = Path("paper_appendix.md")
    sections = []

    sections.append("# CHP Paper Appendix — Automated Build Log\n")
    sections.append(f"Project: {config.project_name}\n")

    # Innovation log
    log = memory.read_full_log()
    sections.append("## Full Innovation Log\n")
    sections.append(log)

    # Dead ends
    de_path = Path("dead_ends.md")
    if de_path.exists():
        sections.append("\n## Dead Ends\n")
        sections.append(de_path.read_text(encoding="utf-8"))

    # State vector
    sv = memory.read_state_vector()
    sections.append("\n## Final State Vector\n")
    for k, v in sv.items():
        sections.append(f"- **{k}**: {v}")

    output.write_text("\n".join(sections), encoding="utf-8")
    console.print(f"[green]Paper appendix exported:[/green] {output}")


@main.command()
def cursor() -> None:
    """Generate Cursor rules for CHP integration."""
    _generate_cursor_rules(Path("."))
    console.print("[green]Cursor rules generated.[/green]")


@main.command(name="install-skills")
@click.option("--global", "global_install", is_flag=True,
              help="Install to ~/.claude/skills/ (all projects)")
def install_skills(global_install: bool) -> None:
    """Install CHP skills for Claude Code (/chp-run, /chp-critic, etc)."""
    skills_src = REPO_ROOT / "claude-code-skills"
    if not skills_src.exists():
        console.print("[red]Skills directory not found.[/red]")
        raise SystemExit(1)

    if global_install:
        target = Path.home() / ".claude" / "skills"
    else:
        target = Path(".claude") / "skills"

    target.mkdir(parents=True, exist_ok=True)

    installed = 0
    for skill_file in skills_src.glob("chp-*.md"):
        dst = target / skill_file.name
        shutil.copy2(skill_file, dst)
        installed += 1
        console.print(f"  Installed: [cyan]/{skill_file.stem}[/cyan]")

    scope = "globally (~/.claude/skills/)" if global_install else f"locally ({target})"
    console.print(f"\n[bold green]{installed} CHP skills installed {scope}[/bold green]")
    console.print("\nAvailable commands in Claude Code:")
    console.print("  /chp-init      Initialize a new CHP project")
    console.print("  /chp-run       Execute one build turn")
    console.print("  /chp-critic    Adversarial review (4 gates)")
    console.print("  /chp-reviewer  Code hygiene check")
    console.print("  /chp-status    Show current status")
    console.print("  /chp-gates     Run sigma-gated verification")


@main.command()
@click.option("--port", default=8501, help="Streamlit server port")
def dashboard(port: int) -> None:
    """Launch the live Streamlit dashboard."""
    import subprocess
    import sys

    config_path = Path("config.yaml")
    if not config_path.exists():
        console.print("[red]config.yaml not found.[/red] Run 'chp init' first.")
        raise SystemExit(1)

    # Find the dashboard app.py
    app_path = REPO_ROOT / "dashboard" / "app.py"
    if not app_path.exists():
        console.print(f"[red]Dashboard not found at {app_path}[/red]")
        raise SystemExit(1)

    try:
        import streamlit  # noqa: F401
    except ImportError:
        console.print(
            "[red]Streamlit not installed.[/red] "
            "Run: pip install context-hacking[dashboard]"
        )
        raise SystemExit(1)

    console.print(f"[bold green]Launching CHP Dashboard[/bold green] on port {port}")
    console.print(f"  Dashboard: {app_path}")
    console.print(f"  Project:   {config_path.resolve().parent}")
    console.print(f"  URL:       http://localhost:{port}")
    console.print()

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(app_path),
         "--server.port", str(port),
         "--server.headless", "true",
         "--browser.gatherUsageStats", "false"],
        cwd=str(Path.cwd()),
    )


@main.command()
def validate() -> None:
    """Validate config.yaml without running."""
    from pathlib import Path as _Path

    from context_hacking.core.orchestrator import Config
    config_path = _Path("config.yaml")
    if not config_path.exists():
        click.echo("Error: No config.yaml found.", err=True)
        raise SystemExit(1)
    config = Config.from_yaml(config_path)
    click.echo(f"Project: {config.project_name}")
    click.echo(f"Max turns: {config.max_turns}")
    click.echo(f"Stagnation threshold: {config.stagnation_threshold}")
    click.echo("Config OK")


def _generate_cursor_rules(target: Path) -> None:
    """Generate .cursorrules and skills/ for Cursor/Claude Code integration."""
    rules_dir = TEMPLATE_DIR / "cursor-rules"

    # .cursorrules
    cursorrules_src = rules_dir / ".cursorrules"
    if cursorrules_src.exists():
        shutil.copy2(cursorrules_src, target / ".cursorrules")
    else:
        # Generate default
        (target / ".cursorrules").write_text(
            "# Context Hacking Protocol — Cursor Rules\n"
            "# Auto-generated by chp cursor\n\n"
            "Before writing any code:\n"
            "1. Read CHAIN_PROMPT.md — this is the single source of truth\n"
            "2. Read dead_ends.md — do NOT repeat logged failures\n"
            "3. Check frozen/ — do NOT modify any file in frozen paths\n"
            "4. After writing code, argue AGAINST your own implementation\n"
            "5. Run the test suite before claiming anything works\n"
            "6. Every coefficient must trace to a source file and line number\n",
            encoding="utf-8",
        )

    # Skills folder
    skills_dir = target / "skills"
    skills_dir.mkdir(exist_ok=True)

    (skills_dir / "critic.md").write_text(
        "# CHP Critic Skill\n"
        "When reviewing code, adopt The Pessimist mindset:\n"
        "- Assume the build failed until proven otherwise\n"
        "- Argue AGAINST the science before scoring it\n"
        "- Check Gate 1 (frozen compliance) first — must be 1.0\n"
        "- Check for circular imports, unseeded randomness, bare print()\n"
        "- Classify issues as BLOCKING or NON-BLOCKING\n",
        encoding="utf-8",
    )

    (skills_dir / "gates.md").write_text(
        "# CHP Gates Skill\n"
        "Before approving any merge:\n"
        "- Run the test suite across 3 seeds minimum\n"
        "- Check all sigma-gates defined in config.yaml\n"
        "- Verify std across seeds < 0.15 for all primary metrics\n"
        "- If any gate fails, the build is BLOCKED\n"
        "- Log the failure and suggest next steps\n",
        encoding="utf-8",
    )

    (skills_dir / "mode.md").write_text(
        "# CHP Mode Skill\n"
        "Check the current mode before every build:\n"
        "- VALIDATION: strict. Every claim needs a citation. Critic blocks.\n"
        "- EXPLORATION: loose. State a hypothesis. Critic is advisory.\n"
        "- If stuck for 5+ turns: suggest switching to Exploration.\n"
        "- If Exploration breaks something: suggest Reversion Protocol.\n"
        "- Read state_vector.md for current mode and context.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
