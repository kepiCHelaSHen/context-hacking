# Installing CHP Skills for Claude Code

## Quick Install (user-level — works in all projects)

```bash
# Copy all CHP skills to your Claude Code user skills directory
cp claude-code-skills/chp-*.md ~/.claude/skills/
```

## Project-Level Install (only this project)

```bash
# Copy to project-level skills
mkdir -p .claude/skills
cp claude-code-skills/chp-*.md .claude/skills/
```

## Or use the CLI

```bash
chp cursor
```

This copies the skills + generates .cursorrules for Cursor integration.

## Available Skills

| Command | What it does |
|---------|-------------|
| `/chp-init` | Initialize a new CHP project in current directory |
| `/chp-run` | Execute one full build turn (read context, build, critique, test, log) |
| `/chp-critic` | Adversarial review — score 4 gates, argue against the science |
| `/chp-reviewer` | Code hygiene review — PEP8, determinism, no print() |
| `/chp-status` | Show current turn, mode, gates, dead ends, next focus |
| `/chp-gates` | Run sigma-gated verification across N seeds |

## Usage

1. Open Claude Code in your project directory
2. Type `/chp-init` to set up the project
3. Type `/chp-run` to start building
4. After each turn, type `/chp-run` again for the next turn
5. Use `/chp-critic` for extra review, `/chp-gates` for verification
6. Type `/chp-status` to check where you are

## The Full Loop

```
/chp-init          → creates project structure
/chp-run           → Turn 1: builds Milestone 1
/chp-run           → Turn 2: builds Milestone 2, catches false positive
/chp-run           → Turn 3: fixes false positive, exploration mode
/chp-gates         → runs 30-seed convergence battery
/chp-run           → Turn 4: final report
/chp-status        → shows DONE
```

That's it. No pip install. No API key. Just Claude Code skills.
