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
PACKAGE_ROOT = Path(__file__).parent.parent
TEMPLATE_DIR = PACKAGE_ROOT


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
    ["schelling", "spatial-pd", "lotka-volterra", "sir"],
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
        }
        exp_name = exp_map.get(experiment, experiment)
        exp_src = TEMPLATE_DIR / "experiments" / exp_name
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
def run() -> None:
    """Launch the CHP orchestrator loop."""
    from context_hacking.core.orchestrator import Config, Orchestrator

    config_path = Path("config.yaml")
    if not config_path.exists():
        console.print("[red]config.yaml not found.[/red] Run 'chp init' first.")
        raise SystemExit(1)

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
        console.print(f"  Status: {result['status']}")
        console.print()
        console.print("[dim]Complete the build, then call 'chp status' to check gates.[/dim]")


@main.command()
def status() -> None:
    """Show current CHP status."""
    from context_hacking.core.orchestrator import Config, Orchestrator
    from context_hacking.core.memory import MemoryManager

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
